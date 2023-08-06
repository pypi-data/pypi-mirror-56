"""
Tools for defining data on multiple domains.
"""
import functools
import inspect
from typing import Any, Callable, Dict, Generic, Iterable, List, Mapping, Optional, Set, Tuple, TypeVar, Union

from mtnlion.structures.mountain import Mountain

VALID_DOMAINS = ["anode", "separator", "cathode", "any"]

_K = TypeVar("_K")
_V = TypeVar("_V")


class Domain(Mountain, Generic[_K, _V], Mapping[_K, _V]):
    """
    Implementation of Mountain that verifies that the domains fall within VALID_DOMAINS.
    """

    def __init__(self, *args: Mapping[Any, Any], **kwargs: Mapping[Any, Any]) -> None:
        """
        Create a Domain dataset
        """
        super(Domain, self).__init__(*args, **kwargs)

        for key in self:
            if key not in VALID_DOMAINS:
                raise RuntimeError("Key {} not a valid domain".format(key))

    def update(self, *args, **kwargs):
        for key in dict(*args, **kwargs):
            if key not in VALID_DOMAINS:
                raise RuntimeError("Key {} not a valid domain".format(key))

        super(Domain, self).update(*args, **kwargs)

    def __setitem__(self, key: Union[Tuple, Any], value: Any) -> None:
        if not isinstance(key, tuple) and key not in VALID_DOMAINS:
            raise RuntimeError("Key {} not a valid domain".format(key))

        super(Domain, self).__setitem__(key, value)


class DomainFunction:
    """
    Decorate a given function to run in each of the domains given. The function arguments will be parsed to determine
    if they are domain aware, and the correct domain will be selected. Otherwise, non domain aware values are passed
    to the function call exactly the same in every domain.
    """

    def __init__(
        self, func: Callable, domain_names: Union[List[str], Tuple[str]], pass_domain: Optional[bool] = False
    ) -> None:
        """
        Decorate a function such that the function is run in each of the domains given.

        :param func: Function to be decorated
        :param domain_names: List of domains to compute in
        :param pass_domain: Flag to indicate if an additional "domain" argument will be added to the arguments
        """
        if not domain_names:
            domain_names = ["auto"]

        if "physical" in domain_names:
            domain_names = ["anode", "separator", "cathode"]

        self._pass_domain = pass_domain
        self._func = func

        self.meta = {
            "domains": domain_names,
            "args": [arg for arg in inspect.getfullargspec(self._func)[0] if arg != "domain"],
        }

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        keys = self._auto_self(args, kwargs)
        kwargs = self._any_arg(kwargs, keys)

        return self._run_func(keys, *args, **kwargs)

    @staticmethod
    def _any_arg(kwargs: Mapping[str, Any], keys: Optional[Iterable[Any]]) -> Dict[str, Any]:
        """
        Parse the kwargs for the "any" key. If the key exists, replace the key with the keys provided, duplicating the
        values as required.

        :param kwargs: kwargs to parse
        :param keys: keys to substitute
        """
        if keys is not None:
            return {
                kwarg: Domain({k: val["any"] for k in keys}) if isinstance(val, dict) and "any" in val else val
                for kwarg, val in kwargs.items()
            }

        return {}

    def _auto_self(self, args: Iterable[Any], kwargs: Mapping[str, Any]) -> Optional[Set[Any]]:
        """
        If the auto keyword is given for the domains, attempt to deduce the relevant domains from the provided
        arguments.

        :param args: Arguments provided to the function
        :param kwargs: Arguments provided to the function
        """
        if "auto" in self.meta["domains"]:
            key_list = [set(arg) for arg in args if isinstance(arg, dict)]
            key_list.extend([key for arg in args if isinstance(arg, list) for key in arg])
            key_list.extend([set(arg) for arg in kwargs.values() if isinstance(arg, dict)])
            key_list.extend([set(key) for arg in kwargs.values() if isinstance(arg, list) for key in list(arg)])
            keys = functools.reduce(lambda x, y: x.intersection(y), key_list) if key_list else None
        else:
            keys = set(self.meta["domains"])

        return keys

    def _run_func(self, keys: Union[Iterable, None], *args, **kwargs) -> Domain[str, Any]:
        """
        Run the decorated function on the specified domains, otherwise run on all domains.

        :param keys: domains to run on
        :param args: formula arguments
        :param kwargs: formula arguments
        """

        def _args(k):
            _arg1 = [arg[k] if isinstance(arg, dict) and k in arg else arg for arg in args if not isinstance(arg, list)]
            _arg2 = [
                [gra[k] if isinstance(gra, dict) and k in gra else gra for gra in arg]
                for arg in args
                if isinstance(arg, list)
            ]
            return _arg1 + _arg2

        def _kwargs(k):
            _kwarg1 = {
                name: arg[k] if isinstance(arg, dict) and k in arg else arg
                for name, arg in kwargs.items()
                if not isinstance(arg, list)
            }
            _kwarg2 = {
                name: [gra[k] if isinstance(gra, dict) and k in gra else gra for gra in arg]
                for name, arg in kwargs.items()
                if isinstance(arg, list)
            }
            return {**_kwarg1, **_kwarg2}

        if self._pass_domain:
            if keys is None:
                return self._func(*args, domain=None, **kwargs)

            return Domain({k: self._func(*_args(k), domain=k, **_kwargs(k)) for i, k in enumerate(keys)})

        if keys is None:
            return self._func(*args, **kwargs)

        return Domain({k: self._func(*_args(k), **_kwargs(k)) for i, k in enumerate(keys)})

    def __repr__(self):
        return "<function %s at 0x%x>" % (self._func.__name__, hash(self))


def eval_domain(*domain_names: str, pass_domain: Optional[bool] = False) -> Callable:
    """
    Easy wrapper to decorate a function to run on given domains.

    :param domain_names: Domains to run on
    :param pass_domain: Add the "domain" argument to the evaluation
    """

    def decorator(func):
        return DomainFunction(func, domain_names, pass_domain=pass_domain)

    return decorator


def partial(func, *partial_args, **partial_kwargs):
    """
    TODO: deprecated, remove
    :param func:
    :param partial_args:
    :param partial_kwargs:
    :return:
    """
    _meta = func.meta

    _args = func.meta["args"][len(partial_args) :]
    _args = [k for k in _args if k not in partial_kwargs]

    def wrapper(*args, **kwargs):
        return func(*partial_args, *args, **partial_kwargs, **kwargs)

    wrapper.meta = _meta
    wrapper.meta.update({"args": _args})

    return wrapper
