"""
Tools for assigning a problem space to a given model.
"""
import json
from abc import abstractmethod
from typing import Any, List, Mapping

import dolfin as fem
import ufl.algebra  # type: ignore

import mtnlion.formula
from mtnlion.domain import Domain
from mtnlion.element import ElementSpace
from mtnlion.formula import FormMap
from mtnlion.model import Model


# TODO: generate domain markers
class ProblemSpace:
    """
    Manages the mesh, function space, trial function vector, and test function vector.
    """

    def __init__(self, mesh: fem.mesh, element_space: ElementSpace) -> None:
        """
        Create an object to manage a given problem space.

        :param mesh: Mesh on which the problem will be evaluated
        :param element_space: Elements defining the function space
        """
        self.element_space = element_space
        self.mesh = mesh

        self.mixed_element = fem.MixedElement(self.element_space.elements)
        self.function_space = fem.FunctionSpace(self.mesh, self.mixed_element)
        self.function_subspace = self._get_subspaces()

        self.trial = fem.TrialFunction(self.function_space)
        self.test = fem.TestFunction(self.function_space)

    def _get_subspaces(self) -> List[fem.FiniteElement]:
        """
        Fetch the subspaces in the mixed element function space
        """
        return [self.function_space.sub(i).collapse() for i in range(len(self.element_space.elements))]

    def function(self) -> fem.Function:
        """
        Create a FEniCS function defined in the mixed element function space
        """
        return fem.Function(self.function_space)

    def assign(self, to_fenics: fem.Function, from_domain: Mapping[Any, Domain]) -> None:
        """
        Assign a mixed element function from a Domain based variable.

        :param to_fenics: Function to assign
        :param from_domain: Domain variable to assign from
        """
        for name, domains in from_domain.items():
            for domain, funcs in domains.items():
                if isinstance(funcs, list):
                    for index, func in zip(self.element_space.mapping[name][domain], funcs):
                        fem.assign(to_fenics.sub(index), func)
                else:
                    fem.assign(to_fenics.sub(self.element_space.mapping[name][domain]), funcs)

    def split(self, function: fem.Function) -> Mapping[Any, Domain]:
        """
        Split a FEniCS function into a domain structure.

        :param function: FEniCS function
        """
        funcs = fem.split(function)

        return {
            name: Domain(
                {
                    domain: [funcs[index] for index in indices] if isinstance(indices, list) else funcs[indices]
                    for domain, indices in domains.items()
                }
            )
            for name, domains in self.element_space.mapping.items()
        }


class ProblemSpaceAssembler(ProblemSpace):
    """
    Handles the assembly of the FFL form from the definition of the model as it relates to the problem space.
    """

    # TODO: fix pylint error
    # pylint: disable=too-many-arguments

    def __init__(self, model: Model, mesh: fem.Mesh, element_space: ElementSpace, dx: fem.Measure, ds: fem.Measure):
        """
        Initialize a problem space.

        :param model: The FEM model
        :param mesh: Solution mesh
        :param element_space: Elements defining the function space
        :param dx: Main dimension measure
        :param ds: Boundary measure
        """
        super(ProblemSpaceAssembler, self).__init__(mesh, element_space)

        self.model = model
        self.dx = dx  # pylint: disable=invalid-name
        self.ds = ds  # pylint: disable=invalid-name
        self.u_data_vec = [self.function() for _ in range(model.delta_t_order + 1)]
        self.u_data = [self.split(f) for f in self.u_data_vec]
        self.v_data = self.split(self.test)

    def _instantiate(self, form_map: FormMap) -> Domain[str, ufl.algebra.Expr]:
        """
        Instantiate the formula defined in the FormMap (create the FFL expression).

        :param form_map: A mapping between formula and formulation
        """
        form = form_map.formula

        # Search problem space for trial functions
        kwargs = {k: self.u_data[0][k] for k in form.args.get_trial_functions()}

        # search problem space for test functions
        kwargs.update({k: self.v_data[form.trial_functions[i]] for i, k in enumerate(form.args.get_test_functions())})

        # Instantiate time derivatives
        if self.model.delta_t_formula is not None:
            kwargs.update(
                {
                    k: self._instantiate(
                        FormMap(self.model.delta_t_formula.select_trial(form.args.get_trial_functions()[i]), name=k)
                    )
                    for i, k in enumerate(form.args.get_time_derivatives())
                }
            )

        # Find any known quantities and populate the function arguments
        kwargs.update(
            {k: self.model.hyper_params[k] for k in form.args.names if k in self.model.hyper_params}  # type: ignore
        )

        # Handle time derivatives
        kwargs.update(
            {
                k.name: [self.u_data[i][form.trial_functions[0]] for i in range(form.order + 1)]
                for k in form.args
                if isinstance(form, mtnlion.formula.Rothes)
            }
        )

        # Check for domain measure
        kwargs.update({k.name: self.dx for k in form.args if k.name == "dx"})

        args = [k for k in form.args if k.name not in kwargs.keys()]

        for k in args:
            if k.name in self.model.forms.names:
                self._instantiate(self.model.forms.fetch_map(k.name))
                kwargs.update({k.name: self.model.forms.fetch_formulation(k.name)})
            else:
                raise NotImplementedError("{} not defined".format(k.name))

        form_map.formulation = form(**kwargs)
        return form_map.formulation

    @staticmethod
    @abstractmethod
    def _assemble_boundary(bound, ds):  # pylint: disable=invalid-name
        pass

    def __str__(self):
        def replace(string, mapping):
            for old, new in mapping.items():
                string = string.replace(old, new)
            return string

        forms = {
            form.name: {domain: str(form.formulation[domain]) for domain in form.domains} for form in self.model.forms
        }

        u_names = {str(func): "u_{}".format(i) for i, func in enumerate(self.u_data_vec)}
        v_name = {str(self.test): "v"}
        indices = {
            "[{}]".format(index): "{{{}[{}]}}".format(name, domain)
            for name, domains in self.element_space.mapping.items()
            for domain, index in domains.items()
            if not isinstance(index, list)
        }
        indices.update(
            {
                "[{}]".format(index): "{{{}<{}>[{}]}}".format(name, i, domain)
                for name, domains in self.element_space.mapping.items()
                for domain, indices in domains.items()
                if isinstance(indices, list)
                for i, index in enumerate(indices)
            }
        )

        for name, domains in forms.items():
            for domain, string in domains.items():
                string = replace(string, u_names)
                string = replace(string, v_name)
                string = replace(string, indices)
                forms[name][domain] = [string]

        return json.dumps(forms, sort_keys=True, indent=4)

    def formulate(self) -> fem.Form:
        """
        Formulate the model equations on the problem space.
        """
        for form_map in self.model.forms:
            if form_map.formulation is None:
                self._instantiate(form_map)

        vec = [
            form.formulation.sum() * self.dx for form in self.model.forms if form.test_functions and not form.boundary
        ]
        vec += [self._assemble_boundary(form.formulation, self.ds).sum() for form in self.model.forms if form.boundary]

        return sum(vec)
