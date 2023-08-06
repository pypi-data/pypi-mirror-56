"""This module provides utilities for loading and saving data in various file formats."""
import logging
import os
from typing import Callable, Dict, List

import numpy as np

LOGGER = logging.getLogger(__name__)


def save_npz_file(filename: str, data_dict: Dict[str, np.ndarray], **kwargs) -> None:
    """
    Save data to an npz file. See numpy.savez for additional argument options.

    :param data_dict: data to be saved to an npz file
    :param filename: name of the npz file
    :param kwargs: additional numpy.savez arguments
    """
    LOGGER.info("Saving data to npz: %s", filename)
    np.savez(filename, **data_dict, **kwargs)


def load_numpy_file(filename: str, **kwargs) -> Dict[str, np.ndarray]:
    """
    Load data from an npz file. See numpy.load for additional argument options.

    :param filename: name of the npz file
    :param kwargs: additional numpy.load arguments
    :return: data dictionary
    """
    LOGGER.info("Loading data from npz: %s", filename)
    with np.load(filename, **kwargs) as data:
        return {k: v for k, v in data.items()}


def load_csv_file(
    filename: str, comments: str = "%", delimiter: str = ",", d_type: type = np.float64, **kwargs
) -> np.ndarray:
    """
    Load data from a csv file. See numpy.load for additional argument options.

    :param filename: name of the csv file
    :param comments: lines starting with a comment will be ignored
    :param delimiter: delimiting character(s)
    :param d_type: data type
    :param kwargs: additional numpy.loadtxt arguments
    :return: file data
    """
    LOGGER.info("Loading CSV file: %s", filename)
    return np.loadtxt(filename, comments=comments, delimiter=delimiter, dtype=d_type, **kwargs)


def format_name(name: str) -> str:
    """
    Do nothing for formatting names and log the event.

    :param name: filename
    :return: variable name
    """
    key = os.path.splitext(os.path.basename(name))[0]
    LOGGER.info("Using key name: %s", key)
    return key


def collect_files(
    file_list: List[str], format_key: Callable = format_name, loader: Callable = load_numpy_file, **kwargs
) -> Dict[str, np.ndarray]:
    """
    Collect files using the provided loader.

    Collect files given as a list of filenames using the function loader to load the file and the function format_key
    to format the variable name.
    :param file_list: list of filenames
    :param format_key: function to format variable names
    :param loader: function to load files
    :param kwargs: extra arguments to the loader
    :return: data dictionary
    """
    msg = "Collecting files: {}".format(file_list)
    LOGGER.info(msg)

    data_dict = dict()
    for file_name in file_list:
        data_dict[format_key(file_name)] = loader(file_name, **kwargs)

    # return {format_key(k): loader(k) for k in file_list}
    return data_dict
