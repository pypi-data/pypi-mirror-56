"""
Provides a class interface for defining FEM models.
"""
from abc import abstractmethod
from typing import Any, Dict, Optional, Union

from mtnlion.domain import Domain
from mtnlion.formula import FormMap, FormMaps, Formula, Rothes, TrialFunctions


class Model:
    """
    Abstract class for defining FEM models.
    """

    def __init__(
        self, hyper_params: Union[Domain[str, Any], Dict[str, Any]], time_integration: Optional[Formula] = None
    ):
        """
        Instantiate the model constructor.

        TODO: hyper_params probably shouldn't be here
        :param hyper_params: Parameters required by the model
        :param time_integration: Formula defining the time integration
        """
        self.forms = FormMaps([FormMap(form) for form in self._formulas()])
        self.hyper_params = hyper_params
        self.trial_functions = TrialFunctions(self._trial_functions())

        if time_integration is None:
            self.delta_t_formula = None
        else:
            self.set_dt(time_integration)

        self.delta_t_order = 1
        self._update_trial_boundary()

    def set_dt(self, time_integration):
        """
        Set the formula for time integration

        :param time_integration: Formula for time integration
        """
        if isinstance(time_integration, Rothes):
            self.delta_t_order = time_integration.order
            self.delta_t_formula = time_integration

    def add_formula(self, *forms):
        """
        Add a formulae to the model
        :param forms: formulae to add
        """
        self.forms += [FormMap(form) for form in forms]

    def _update_trial_boundary(self):
        """
        Update the trial function metadata for boundaries
        """
        is_boundary = [
            all([form.boundary for form in self.forms if k.name in form.trial_functions]) for k in self.trial_functions
        ]
        for trial, boundary in zip(self.trial_functions, is_boundary):
            trial.boundary = boundary

    def set_elements(self, trial_function_map):
        """
        Manually set the elements for the model

        :param trial_function_map: Mapping of functions to elements
        """
        # TODO: implement
        raise NotImplementedError("This function has not been implemented")

    def set_dim_elements(self, element):
        """
        Set the elements for the non-boundary trial functions

        :param element: element to apply to all non-boundary trial functions
        """
        for trial_function in self.trial_functions:
            if not trial_function.boundary:
                trial_function.element = Domain({domain: element for domain in trial_function.domains})

    def set_boundary_elements(self, element):
        """
        Set the elements for all the boundary trial functions.

        :param element: element to apply to all boundary trial functions
        """
        for trial_function in self.trial_functions:
            if trial_function.boundary:
                trial_function.element = Domain({"any": element})

    @abstractmethod
    def _formulas(self):
        pass

    @abstractmethod
    def _trial_functions(self):
        pass
