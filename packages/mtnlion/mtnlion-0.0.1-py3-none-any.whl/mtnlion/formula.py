"""
Collection of classes for defining formulae.
"""
import copy
import inspect
from abc import abstractmethod
from typing import Any, List, Mapping, Optional, Union

import mtnlion.domain
from mtnlion.domain import Domain


class Argument:
    """
    Metadata for an argument in the _form_ overrides from Formulas
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, name: str, trial_function: bool, test_function: bool, time_derivative: bool) -> None:
        """
        Create an argument that defines the attributes.

        :param name: Name of the argument
        :param trial_function: True if argument is a trial function
        :param test_function: True if argument is a test function
        :param time_derivative: True if argument is a time derivative
        """
        self.name = name
        self.trial_function = trial_function
        self.test_function = test_function
        self.time_derivative = time_derivative

    def __repr__(self) -> str:
        return self.name


class Arguments(list):
    """
    List of arguments for a given formula. Provides convenience functions for listing data.
    """

    def get_trial_functions(self) -> List[str]:
        """
        Retrieve the names of arguments that are trial functions
        """
        return [a.name for a in self if a.trial_function]

    def get_test_functions(self) -> List[str]:
        """
        Retrieve the names of arguments that are test functions
        """
        return [a.name for a in self if a.test_function]

    def get_time_derivatives(self) -> List[str]:
        """
        Retrieve the names of arguments that are time derivatives
        """
        return [a.name for a in self if a.time_derivative]

    @property
    def names(self) -> List[str]:
        """
        Return the names of the arguments in this list
        """
        return [arg.name for arg in self]


class Formula:
    """
    Base class for defining new formulas for use in a model.
    """

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments

    def __init__(
        self,
        domains: Optional[List[str]] = None,
        trial_functions: Optional[List[str]] = None,
        test_functions: Optional[List[str]] = None,
        time_derivatives: Optional[List[str]] = None,
        pass_domain: bool = False,
        boundary: bool = False,
        name_overrides: Optional[Mapping[str, str]] = None,
        name: Optional[str] = None,
    ) -> None:
        """
        Base class for defining formulas in order to generate FFL expressions

        :param domains: List of domains the formula is defined in
        :param trial_functions: List of the argument names that are trial functions
        :param test_functions: List of the argument names that are test functions
        :param time_derivatives: List of the argument names that are time derivatives
        :param pass_domain: Boolean flag to indicate if the "domain" variable will become an argument
        :param boundary: Boolean flag to indicate formula is a boundary condition
        :param name_overrides: Mapping to rename arguments
        :param name: Name of the formula
        """

        self.domains = self._set(domains, [])
        self.pass_domain = pass_domain
        self.trial_functions = self._set(trial_functions, [])
        self.test_functions = self._set(test_functions, [])
        self.time_derivatives = self._set(time_derivatives, [])
        self.name_overrides = self._set(name_overrides, {})
        self.boundary = boundary
        self.name = self._set(name, type(self).__name__)
        self.args = Arguments(self._form_args())

    def _form_args(self) -> List[Argument]:
        """
        Generate a list of arguments with metadata from the arguments defined in the overridden _form_method.
        """
        args = [
            arg
            for arg in inspect.getfullargspec(self._form_)[0]
            if arg not in ["self", "domain"] + list(self.name_overrides.values())
        ]
        args += list(self.name_overrides.keys())

        trials = [a in self.trial_functions for a in args]
        tests = [a in self.test_functions for a in args]
        dts = [a in self.time_derivatives for a in args]

        set_args = [Argument(name, trials[i], tests[i], dts[i]) for i, name in enumerate(args)]

        return set_args

    @staticmethod
    def _set(data: Union[None, Any], default: Any) -> Any:
        """
        Helper method to set data to default if data is None.
        """
        return default if data is None else data

    @abstractmethod
    def _form_(self, *args, **kwargs):
        """
        Override this method to define the FFL form
        """

    def select_trial(self, trial_name: str):
        """
        Create a new formula based on the current object replacing all of the trial functions with the one named.

        TODO: This doesn't belong here
        """
        trial_function = next(filter(lambda x: x == trial_name, self.trial_functions), None)
        if trial_function is None:
            raise ValueError("Trial function {} not defined in time stepping scheme.".format(trial_name))
        new_cls = copy.copy(self)
        new_cls.trial_functions = [trial_function]
        return new_cls

    def __call__(self, *args: Any, **kwargs: Any) -> Domain[str, Any]:
        """
        Call _form_ for the specified domains using the given arguments.
        """
        # TODO: see if subclass's signature can be used in place here
        _kwargs = {k: v for k, v in kwargs.items() if k not in self.name_overrides}
        _kwargs.update({v: kwargs[k] for k, v in self.name_overrides.items()})

        return mtnlion.domain.DomainFunction(self._form_, self.domains, self.pass_domain)(*args, **_kwargs)


class FormulaDAE(Formula):
    """
    Simplified formula, DAEs do not necessarily require trial functions. Just need a name.
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, name: str, **kwargs) -> None:
        """
        Create a DAE with the specified name.
        """
        super(FormulaDAE, self).__init__(name=name, **kwargs)

    @abstractmethod
    def _form_(self, *args, **kwargs):
        """
        Override this method to define the FFL form
        """


class FormMap:
    """
    A mapping between formula specifications (unformulated) and the formulated FFL representation.
    """

    def __init__(self, formula: Formula, formulation: Optional[Any] = None, name: Optional[str] = None) -> None:
        if not isinstance(formula, Formula):
            raise AttributeError("Only Formula types are permitted for formulas")

        self.formula = formula
        self.formulation = formulation

        if name is not None:
            self.name = name

    @property
    def name(self) -> str:
        """
        Name of the formula
        """
        return self.formula.name

    @name.setter
    def name(self, name: str) -> None:
        """
        Name of the formula
        """
        self.formula.name = name

    @property
    def domains(self) -> List[str]:
        """
        Domains that the formula is defined in
        """
        return self.formula.domains

    @property
    def boundary(self) -> bool:
        """
        True if the formula is a boundary
        """
        return self.formula.boundary

    @property
    def test_functions(self) -> List[str]:
        """
        List of test functions in the formula
        """
        return self.formula.test_functions

    @property
    def trial_functions(self) -> List[str]:
        """
        List of trial functions in the formula
        """
        return self.formula.trial_functions

    def __repr__(self) -> str:
        """
        Nice printout for the formula, indicates if it has been formulated
        """
        return "{}: {}".format(self.formula.name, "formulated" if self.formulation is not None else "unformulated")


class FormMaps(list):
    """
    A collection of FormMap's with convenience functions.
    """

    @property
    def names(self) -> List[str]:
        """
        Return a list of formula names
        """
        return [form.name for form in self]

    def fetch_map(self, name: str) -> FormMap:
        """
        Return the form map for a given formula name
        """
        return next(filter(lambda x: x.name == name, self))

    def fetch_formula(self, name: str) -> Formula:
        """
        Return the formula given a formula name
        """
        return self.fetch_map(name).formula

    def fetch_formulation(self, name: str) -> Any:
        """
        Return the formulation corresponding to a formula name
        """
        return self.fetch_map(name).formulation


class TrialFunction:
    """
    A container defining relevant trial function metadata.
    """

    # pylint: disable=too-many-arguments

    def __init__(
        self,
        name: str,
        domains: List[str],
        element: Optional[Any] = None,
        boundary: Optional[bool] = False,
        num_functions: int = 1,
    ):
        """
        Define relevant metadata for a given trial function.

        :param name: Name of the trial function
        :param domains: Domains where the trial function is defined
        :param element: Elements that map to this trial function
        :param boundary: Boolean indicating if this trial function exists on a boundary
        :param num_functions: Number of elements required to represent this trial function
        """
        self.name = name
        self.domains = domains
        self.boundary = boundary
        self._element = element
        self._num_functions = num_functions

    @property
    def element(self) -> Optional[Domain[str, List[Any]]]:
        """
        Retrieve a mapping of elements for this trial function
        """
        if self._element is not None:
            return Domain({domain: [element] * self.num_functions for domain, element in self._element.items()})

        return None

    @element.setter
    def element(self, value: Domain[str, List[Any]]) -> None:
        """
        Set a mapping of elements for this trial function
        """
        self._element = value

    @property
    def num_functions(self) -> int:
        """
        Get the number of functions required to represent this trial function
        """
        return self._num_functions

    @num_functions.setter
    def num_functions(self, value: int):
        """
        Set the number of functions required to represent this trial function
        """
        self._num_functions = value

    def __repr__(self) -> str:
        """
        Pretty print the trial function information
        """
        return "{}: boundary={}, element={}, num_functions={}".format(
            self.name, self.boundary, self._element, self.num_functions
        )


class TrialFunctions(list):
    """
    A collection of TrialFunction's
    """


class LagrangeMultiplier(Formula):
    """
    Formula defining a Lagrange multiplier.

    TODO: This doesn't belong here
    """

    # pylint: disable=arguments-differ
    # pylint: disable=too-few-public-methods

    def __init__(self, domains: List[str], lm_name: str, trial_name: str):
        super(LagrangeMultiplier, self).__init__(
            domains=domains,
            trial_functions=[lm_name, trial_name],
            name_overrides={lm_name: "lm", trial_name: "u"},
            test_functions=["mu", "v"],
            boundary=True,
        )

    def _form_(self, lm, mu, u, v):
        return lm * v + u * mu


class Rothes(Formula):
    """
    Base formula for defining Rothe's based time stepping.
    """

    # pylint: disable=arguments-differ
    # pylint: disable=too-few-public-methods

    def __init__(self, trial_functions: List[str], delta_t: float, order: int = 1, **kwargs):
        self.delta_t = delta_t
        self.order = order
        super(Rothes, self).__init__(trial_functions=trial_functions, **kwargs)

    @abstractmethod
    def _form_(self, u_list):
        pass
