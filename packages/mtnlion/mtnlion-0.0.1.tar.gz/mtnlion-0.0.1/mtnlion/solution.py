"""
Tools for access and storage of simulation solutions.
"""
import collections
from typing import Dict, List, Mapping, Optional

import dolfin as fem
import numpy as np
import ufl.algebra  # type: ignore

import mtnlion.tools.helpers
from mtnlion.domain import Domain
from mtnlion.problem_space import ProblemSpaceAssembler
from mtnlion.tools.helpers import interp_time2, set_domain_data


class Solution:
    """
    This class provides an interface for converting FEniCS functions into numpy-based solutions
    """

    # TODO: fix pylint
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=no-member

    def __init__(self, problem_space: ProblemSpaceAssembler, save_list: List[str], dae_space: fem.FunctionSpace):
        """
        Initialize the storage object using the problem space, a list of functions to save, and the function space for
        any DAEs.

        :param problem_space: The problem space
        :param save_list: List of functions to save
        :param dae_space: Function space for DAEs
        """

        self.dae_space = dae_space
        self.problem_space = problem_space
        self.available_daes = {
            form.name: form.formulation for form in self.problem_space.model.forms if len(form.test_functions) == 0
        }
        self.trial_functions = {
            k: domain for k, domain in self.problem_space.element_space.mapping.items() if k in save_list
        }
        self.daes = {k: domain for k, domain in self.available_daes.items() if k in save_list}
        self.solutions: Optional[Mapping[str, Domain[str, np.ndarray]]] = None
        self.num_time_steps = 0
        self.mesh = np.squeeze(self.problem_space.mesh.coordinates())
        self.time = np.empty(0)
        self.iterations = 0

    def _init_solution(self, length: int) -> None:
        """
        Initialize the solution storage. If called after the solution storage has been initialized, the length will be
        appended to the solution.

        :param length: Length of the solution (usually time)
        """
        self.num_time_steps = length
        if self.solutions is None:
            self.time = np.empty((length,), dtype=np.float)
            save_list = collections.ChainMap(self.trial_functions, self.daes)
            self.solutions = {
                name: set_domain_data(
                    *mtnlion.tools.helpers.create_solution_matrices(
                        length, len(self.problem_space.mesh.coordinates()), len(domains)
                    )
                )
                for name, domains in save_list.items()
            }
        else:
            self.time = np.append(self.time, np.empty((self.time.shape[0],), dtype=np.float), axis=0)
            for name, domains in self.solutions.items():
                for domain, value in domains.items():
                    self.solutions[name][domain] = np.append(
                        mtnlion.tools.helpers.create_solution_matrices(length - value.shape[0], value.shape[1], 1)[0],
                        self.solutions[name][domain],
                        axis=0,
                    )

    def get_1d(self, function: fem.Function, all_funcs=False) -> Dict[str, Domain[str, np.ndarray]]:
        """
        Retrieve the one dimensional values from the given mixed element space function.

        :param function:
        :param all_funcs:
        :return:
        """
        # funcs = function.split(True)

        if all_funcs:
            save_list = list(self.problem_space.element_space.mapping)
        else:
            save_list = list(self.trial_functions)

        return {
            name: Domain(
                {
                    domain: [
                        mtnlion.tools.helpers.get_1d(
                            function.sub(index, True), self.problem_space.function_subspace[index]
                        )
                        for index in indices
                    ]
                    if isinstance(indices, list)
                    else mtnlion.tools.helpers.get_1d(
                        function.sub(indices, True), self.problem_space.function_subspace[indices]
                    )
                    if domain != "any"
                    else function.sub(indices, True).vector().get_local()
                    for domain, indices in domains.items()
                }
            )
            for name, domains in self.problem_space.element_space.mapping.items()
            if name in save_list
        }

    def project(self, function: Mapping[str, Domain[str, ufl.algebra.Expr]]):
        """
        Project an expression onto the DAE space

        :param function: Non mixed-element function
        """
        result = {
            name: mtnlion.tools.helpers.get_1d(fem.project(data, self.dae_space), self.dae_space)
            for name, data in function.items()
        }
        return result

    def set_solution_time_steps(self, num_time_steps: int) -> None:
        """
        Initialize the solution storage for the specified number of iterations

        :param num_time_steps: number of iterations in the simulation
        """
        self._init_solution(num_time_steps)

    def save_solution(self, iteration: int, time: float):
        """
        Save the state of the solution vector given the iteration and current time.

        :param iteration: current simulation iteration
        :param time: time at the same iteration
        """
        if self.solutions is None:
            raise RuntimeError("Solutions not initialized!")

        self.time[iteration] = time
        self.iterations = max(self.iterations, iteration)
        solutions = self.get_1d(self.problem_space.u_data_vec[0])
        solutions.update({k: self.project(domain) for k, domain in self.daes.items()})

        for name, domains in self.solutions.items():
            domains[iteration, :] = solutions[name]

    @staticmethod
    def interp_time(time: np.ndarray, domain: Mapping[str, Domain[str, np.ndarray]]):
        """
        Create an interpolation function for each of the solutions in storage
        :param time: The times at which to
        :param domain: Data to interpolate
        :return: Interpolation functions for the solution
        """
        return {name: interp_time2(time, domains) for name, domains in domain.items()}
