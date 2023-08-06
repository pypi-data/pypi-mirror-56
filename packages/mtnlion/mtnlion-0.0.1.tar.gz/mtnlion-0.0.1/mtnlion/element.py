"""
Element mapping utilities
"""
import copy
from typing import Any, List, Mapping, Tuple, Union

from mtnlion.domain import Domain
from mtnlion.formula import TrialFunctions

ElementMapping = Mapping[str, Domain[str, List[Any]]]
ElementListMapping = Mapping[str, Domain[str, List[int]]]


class Element:
    """
    Abstract base class to define the interface for "elements"
    """

    @property
    def mapping(self) -> ElementListMapping:
        """
        A dictionary defining the mapping between trial functions and elements. Elements are stored as a list in
        self.elements.

        :raises NotImplementedError if not implemented.
        """
        raise NotImplementedError

    @property
    def elements(self) -> List[Any]:
        """
        A list of elements defining the solution vector.

        :raises NotImplementedError if not implemented.
        """
        raise NotImplementedError


class ElementSpace(Element):
    """
    ElementSpace is used to define the mapping between functions and their domains to a list of elements that FEniCS can
    recognize.
    """

    def __init__(self, equation_spec: Union[ElementMapping, TrialFunctions]):
        """
        Create a map to a list of elements.

        :param equation_spec: Specification for mapping to elements
        """
        if isinstance(equation_spec, TrialFunctions):
            self.equation_spec: ElementMapping = {tf.name: tf.element for tf in equation_spec}
        else:
            self.equation_spec = equation_spec
        self._mapping, self._elements = self.map(self.equation_spec)

    @property
    def mapping(self):
        return self._mapping

    @property
    def elements(self):
        return self._elements

    @staticmethod
    def map(equation_spec: ElementMapping) -> Tuple[ElementListMapping, List[Any]]:
        """
        Given a mapping between functions and their elements, form a list of elements and create a mapping between
        the functions and the indices of their respective elements in the element list.

        :param equation_spec: Dictionary mapping between functions and their elements
        :return: Mapping of functions to the indices of their respective elements in the element list
        """

        # Don't change the values of the passed argument
        _mapping = copy.deepcopy(equation_spec)
        _elements: List[int] = []

        index = 0
        for name, domains in equation_spec.items():
            for domain, elements in domains.items():
                stop_index = index + len(elements)

                _mapping[name][domain] = list(range(index, stop_index))

                if len(_mapping[name][domain]) == 1:
                    _mapping[name][domain] = _mapping[name][domain][0]

                _elements += elements
                index = stop_index

        return _mapping, _elements

    def remap(self, offset: int) -> None:
        """
        Shift the indices of the map by an offset. Usually used to merge element spaces.

        :param offset: Amount to offset the map
        """
        self._mapping = {
            name: Domain(
                {
                    domain: [index + offset for index in indices] if isinstance(indices, list) else indices + offset
                    for domain, indices in domains.items()
                }
            )
            for name, domains in self._mapping.items()
        }

    def __len__(self) -> int:
        """
        Number of elements in the mapping
        """
        return len(self.elements)


class SimpleElementSpace(ElementSpace):
    """
    A wrapper to simplify the definition of the element space.

    TODO: Potentially deprecated.
    """

    def __init__(self, element, num_functions=1, **equations):
        self.equations = equations
        self.element = element
        self.num_functions = num_functions
        super().__init__(self._setup_dict(self.equations, self.element, self.num_functions))

    @staticmethod
    def _setup_dict(equations, element, num_functions):
        return {
            name: Domain({domain: [element] * num_functions for domain in value.meta["domains"]})
            if not value.meta["boundary"]
            else {"any": [element] * num_functions}
            for name, value in equations.items()
        }


class MixedElementSpace(Element):
    """
    Handles the combination of multiple element spaces into one vector.

    TODO: Potentially deprecated.
    """

    def __init__(self, *spaces: ElementSpace):
        """
        Merge multiple element spaces into one mapping and one vector.
        """
        super(MixedElementSpace, self).__init__()
        self.spaces = spaces
        self._remap()

    @property
    def elements(self):
        return [element for space in self.spaces for element in space.elements]

    @property
    def mapping(self):
        return {name: value for space in self.spaces for name, value in space.mapping.items()}

    def _remap(self):
        offset = len(self.spaces[0])
        for space in self.spaces[1:]:
            space.remap(offset)
            offset += len(space)
