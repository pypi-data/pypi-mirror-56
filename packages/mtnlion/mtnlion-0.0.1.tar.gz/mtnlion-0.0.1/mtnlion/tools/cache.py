"""
File caching tools.
"""
from pathlib import Path
from typing import Any, Callable

import numpy as np

CACHE_DIR = Path.home().joinpath(".cache/mtnlion")


def persist_to_npy_file(
    file_name: str,
    do_cache: Callable[
        [np.ndarray, Any], bool
    ] = lambda cached, *args, **kwargs: True,  # pylint: disable=bad-whitespace
) -> Callable:
    """
    Decorator to cache numpy arrays to a file.

    :param file_name: name of the cached file
    :param do_cache: function to determine if caching should be performed
    """

    def decorator(original_func):
        cachefile = CACHE_DIR.joinpath(file_name)
        if cachefile.exists():
            cache = np.load(str(cachefile))
        else:
            cache = None

        def new_func(*args, **kwargs):
            nonlocal cache
            if cache is None or do_cache(cache, *args, **kwargs):
                cache = original_func(*args, **kwargs)
                np.save(str(cachefile), cache)
            return cache

        return new_func

    return decorator
