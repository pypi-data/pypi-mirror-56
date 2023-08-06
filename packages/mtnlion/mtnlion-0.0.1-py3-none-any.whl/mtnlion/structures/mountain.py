"""
Data structure for handling mathematical operations on dictionaries.
"""
from typing import Any, Callable, Tuple, Union

import numpy as np


class Mountain(dict):
    """
    A dictionary wrapper that allows math to be performed between like objects, or basic types. Also allows slicing
    into every value of the dictionary.
    """

    def sum(self) -> Any:
        """
        Sum all of the values in the dictionary.

        If the values are lists, the lists will be summed together and added to the results.
        TODO: Change to check for iterables, and sum if possible (could use try-catch)
        TODO: This method doesn't belong here

        :return: Summed values
        """
        if isinstance(list(self.values())[0], list):
            vec = [sum(v) for v in self.values()]
            return sum(vec)

        return sum(self.values())

    def concatenate(self, axis: int = 0, func: Callable[[Any], Any] = lambda x: x) -> np.ndarray:
        """
        Concatenate internal values, returns the result. Assumes that values being concatenated are numpy arrays.
        TODO: This method really doesn't belong here

        :param axis: Numpy axis
        :param func: Function that gets run on each dictionary value
        :return: Numpy array
        """
        return np.concatenate(tuple(func(v) for v in self.values()), axis)

    def __check(self, other: Union[dict, "Mountain", Any]) -> None:
        """
        Check if the argument is a dictionary and that all keys match.

        :param other: argument
        :return: None
        """
        if isinstance(other, dict):
            if self.keys() != other.keys():
                raise RuntimeError("Objects don't have the same keys")

    def __operate(self, other: Union[dict, "Mountain", Any], func: Callable[[Any, Any], Any]) -> "Mountain":
        """
        Perform an operation on all keys both self and argument if argument is based on a dict. If argument is
        not a dict, apply func on all keys on self with other as an argument.

        :param other: argument
        :param func: operation to perform
        :return: New Mountain
        """
        if isinstance(other, dict):
            return Mountain({key: func(value, other[key]) for key, value in self.items()})

        return Mountain({key: func(value, other) for key, value in self.items()})

    def __add__(self, other: Union[dict, "Mountain", Any]) -> "Mountain":
        self.__check(other)

        return self.__operate(other, lambda x, y: x + y)

    def __sub__(self, other: Union[dict, "Mountain", Any]) -> "Mountain":
        self.__check(other)

        return self.__operate(other, lambda x, y: x - y)

    def __neg__(self) -> "Mountain":
        return self.__sub__(0)

    def __mul__(self, other: Union[dict, "Mountain", Any]) -> "Mountain":
        self.__check(other)

        return self.__operate(other, lambda x, y: x * y)

    def __truediv__(self, other: Union[dict, "Mountain", Any]) -> "Mountain":
        self.__check(other)

        return self.__operate(other, lambda x, y: x / y)

    def __floordiv__(self, other: Union[dict, "Mountain", Any]) -> "Mountain":
        self.__check(other)

        return self.__operate(other, lambda x, y: x // y)

    def __mod__(self, other: Union[dict, "Mountain", Any]) -> "Mountain":
        self.__check(other)

        return self.__operate(other, lambda x, y: x % y)

    def __pow__(self, other: Union[dict, "Mountain", Any]) -> "Mountain":
        self.__check(other)

        return self.__operate(other, lambda x, y: x ** y)

    def __radd__(self, other: Union[dict, "Mountain", Any]) -> "Mountain":
        return self.__add__(other)

    def __rsub__(self, other: Union[dict, "Mountain", Any]) -> "Mountain":
        return self.__sub__(other)

    def __rmul__(self, other: Union[dict, "Mountain", Any]) -> "Mountain":
        return self.__mul__(other)

    def __rtruediv__(self, other: Union[dict, "Mountain", Any]) -> "Mountain":
        return self.__truediv__(other)

    def __rfloordiv__(self, other: Union[dict, "Mountain", Any]) -> "Mountain":
        return self.__floordiv__(other)

    def __rmod__(self, other: Union[dict, "Mountain", Any]) -> "Mountain":
        return self.__mod__(other)

    def __rpow__(self, other: Union[dict, "Mountain", Any]) -> "Mountain":
        return self.__pow__(other)

    def __isub__(self, other: Union[dict, "Mountain", Any]) -> "Mountain":
        for key, value in self.__sub__(other).items():
            self[key] = value
        return self

    def __iadd__(self, other: Union[dict, "Mountain", Any]) -> "Mountain":
        for key, value in self.__add__(other).items():
            self[key] = value
        return self

    def __imul__(self, other: Union[dict, "Mountain", Any]) -> "Mountain":
        for key, value in self.__mul__(other).items():
            self[key] = value
        return self

    def __idiv__(self, other: Union[dict, "Mountain", Any]) -> "Mountain":
        for key, value in self.__truediv__(other).items():
            self[key] = value
        return self

    def __ifloordiv__(self, other: Union[dict, "Mountain", Any]) -> "Mountain":
        for key, value in self.__floordiv__(other).items():
            self[key] = value
        return self

    def __imod__(self, other: Union[dict, "Mountain", Any]) -> "Mountain":
        for key, value in self.__mod__(other).items():
            self[key] = value
        return self

    def __ipow__(self, other: Union[dict, "Mountain", Any]) -> "Mountain":
        for key, value in self.__sub__(other).items():
            self[key] = value
        return self

    def __setitem__(self, key: Union[Tuple, Any], value: Union["Mountain", Any]) -> None:
        """
        Allow traditional dictionary key-value assignment, but add the ability to slice into all values stored in this
        object.

        If slicing, the assigning value must be a dictionary containing a subset of keys from the assignee, and the
        values contained in the assignee must be slice-able.

        :param key: Dictionary key
        :param value: Assignment value
        """
        if isinstance(key, tuple):
            if not isinstance(value, dict):
                raise ValueError("Attempting to assign sliced data without a dictionary assignment.")

            indices = key
            for _key, _value in value.items():
                self[_key][indices[0]] = _value[indices[1]]
        else:
            super(Mountain, self).__setitem__(key, value)

    def __getitem__(self, key: Union[Tuple, slice, Any]) -> Union["Mountain", Any]:
        """
        Allow traditional dictionary value fetch, but add the ability to slice into all values stored in this
        object.

        If slicing, the values contained in the object must be slice-able.

        :param key: Dictionary key
        """
        if isinstance(key, (tuple, slice)):
            return Mountain({_key: _value[_key] for _key, _value in self.items()})

        return super(Mountain, self).__getitem__(key)
