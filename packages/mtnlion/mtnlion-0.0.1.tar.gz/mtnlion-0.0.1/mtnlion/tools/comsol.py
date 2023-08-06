"""
COMSOL Data Handling.

This module is designed to load 1D solution data from a Gu & Wang reference model from COMSOL as
CSV files.
The idea is that CSV files take a long time to load, so it is more efficient to convert the data to a binary
(npz) format before processing.

COMSOL now saves it's data as a 2D matrix, however it still only uses repeated x values when the boundary solves for
different values on either side. In order to normalize the repeated bounds, all bounds are check to ensure they've got
repeated x values, such that the y values are duplicated.
"""
import logging
import os
from typing import Dict, List, Mapping, MutableMapping, Tuple, Union

import dolfin as fem
import munch
import numpy as np
from scipy import interpolate

from mtnlion import deprecated_domain, engine
from mtnlion.domain import Domain
from mtnlion.tools import loader

LOGGER = logging.getLogger(__name__)


def fix_boundaries(mesh: np.ndarray, data: np.ndarray, boundaries: Union[float, List[int], np.ndarray]) -> np.ndarray:
    """
    Adjust COMSOL's interpretation of two-sided boundaries.

    When COMSOL outputs data from the reference model there are two solutions at every internal boundary, which causes
    COMSOL to have repeated domain values; one for the right and one for the left of the boundary. If there is only one
    internal boundary on the variable mesh at a given time, then a duplicate is added.

    :param mesh: x data to use to correct the y data
    :param data: in 2D, this would be the y data
    :param boundaries: internal boundaries
    :return: normalized boundaries to be consistent
    """
    msg = "Fixing boundaries: {}".format(boundaries)
    LOGGER.debug(msg)
    b_indices = np.searchsorted(mesh, boundaries)

    if not b_indices.any():
        return data

    for index in b_indices[::-1]:
        if mesh[index] != mesh[index + 1]:  # add boundary
            LOGGER.debug("Adding boundary, copying %f at index %d", mesh[index], index)
            data = np.insert(data, index, data[index], axis=0)

    return data


def remove_dup_boundary(data: deprecated_domain.ReferenceCell, item: np.ndarray) -> Union[np.ndarray, None]:
    """
    Remove points at boundaries where two values exist at the same coordinate, favor electrodes over separator.

    :param data: data in which to reference the mesh and separator indices from

    :param item: item to apply change to
    :return: Array of points with interior boundaries removed
    """
    LOGGER.info("Removing duplicate boundaries")
    mask = np.ones(item.shape[-1], dtype=bool)
    mask[[data.sep_ind.start, data.sep_ind.stop - 1]] = False
    return item[..., mask]


def get_standardized(cell: deprecated_domain.ReferenceCell) -> Union[engine.Mountain, None]:
    """
    Convert COMSOL solutions to something more easily fed into FEniCS (remove repeated coordinates at boundaries).

    :param cell: reference cell to remove double boundary values from
    :return: Simplified solution cell
    """
    LOGGER.info("Retrieving FEniCS friendly solution cell")
    return cell.filter_space([slice(0, len(cell.mesh))], func=lambda x: remove_dup_boundary(cell, x))
    # mesh = remove_dup_boundary(cell, cell.mesh)
    # new_data = {k: remove_dup_boundary(cell, v) for k, v in cell.data.items()}
    # return domain.ReferenceCell(mesh, cell.time_mesh, cell.boundaries, **new_data)


# TODO generalize the formatting of data for mesh name and arbitrary dimensions
def format_data(
    raw_data: Mapping[str, np.ndarray], boundaries: Union[float, List[int]]
) -> Union[Mapping[str, np.ndarray], None]:
    """
    Format COMSOL stacked 1D data into a 2D matrix.

    Collect single-column 2D data from COMSOL CSV format and convert into 2D matrix for easy access, where the
    first dimension is time and the second is the solution in space. Each solution has it's own entry in a
    dictionary where the key is the name of the variable. The time step size (time_integration) and mesh have
    their own keys.

    :param raw_data: COMSOL formatted CSV files
    :param boundaries: internal boundary locations
    :return: convenient dictionary of non-stationary solutions
    """
    LOGGER.info("Reformatting 2D data")
    data = dict()
    try:
        mesh_dict = {"time_mesh": raw_data["time_mesh"], "mesh": raw_data["mesh"], "boundaries": boundaries}
    except KeyError as ex:
        LOGGER.critical("Missing required data", exc_info=True)
        raise ex

    for key, value in raw_data.items():
        if key in ("mesh", "time_mesh"):
            continue

        LOGGER.info("Reformatting %s", key)
        try:
            (x_data, y_data) = (value[:, 0], value[:, 1:])

            data[key] = fix_boundaries(x_data, y_data, boundaries).T

            if data[key].shape[-1] != len(raw_data["mesh"]):
                LOGGER.warning("%s does not fit the mesh, skipping", key)
                data.pop(key, None)
            elif key not in data:
                LOGGER.warning("%s was skipped, unknown reason", key)
        except IndexError:
            LOGGER.warning("%s must have two columns and fit the mesh, skipping", key, exc_info=True)
            continue
        except Exception as ex:
            LOGGER.critical("Error occurred while formatting %s", key, exc_info=True)
            raise ex

        LOGGER.info("Done formatting %s", key)
    return {**data, **mesh_dict}


def format_name(name: str) -> str:
    """
    Determine variable name from filename to be used in loader.collect_files.

    :param name: filename
    :return: variable name
    """
    var_name = os.path.splitext(os.path.basename(name))[0]
    if ".CSV" not in name.upper():
        LOGGER.warning("%s does not have a CSV extension", name)
    else:
        var_name = var_name.split(".", 1)[0]

    return var_name


def load(filename: str) -> engine.Mountain:
    """
    Load COMSOL reference cell from formatted npz file.

    :param filename: name of the npz file
    :return: ReferenceCell
    """
    file_data = loader.load_numpy_file(filename)
    return deprecated_domain.ReferenceCell.from_dict(file_data)


def adimensionalize_comsol_data(
    comsol_data: deprecated_domain.ReferenceCell, mesh: np.ndarray
) -> Mapping[str, Mapping[str, np.ndarray]]:
    """
    Separate a one dimensional (in time) set of cell data into three [0-1] domains.

    :param comsol_data: data to adimensionalize
    :param mesh: destination mesh
    """

    def make_dict(data, axis=0):
        out = Domain()
        if ~np.isnan(data[:, comsol_data.neg_ind]).any():
            out.update({"anode": interpolate.interp1d(comsol_data.neg, data[:, comsol_data.neg_ind], axis=axis)(mesh)})
        if ~np.isnan(data[:, comsol_data.sep_ind]).any():
            out.update(
                {"separator": interpolate.interp1d(comsol_data.sep, data[:, comsol_data.sep_ind], axis=axis)(mesh + 1)}
            )
        if ~np.isnan(data[:, comsol_data.pos_ind]).any():
            out.update(
                {"cathode": interpolate.interp1d(comsol_data.pos, data[:, comsol_data.pos_ind], axis=axis)(mesh + 2)}
            )

        return out

    data = {k: make_dict(v, 1) for k, v in comsol_data.data.items()}
    return data


def interp_time(
    time: np.ndarray, adim_data: Mapping[str, Mapping[str, np.ndarray]]
) -> Dict[str, Dict[str, interpolate.interp1d]]:
    """
    Return one dimensional interpolation functions corresponding to a dictionary of dictionaries.

    :param time: Times at which the data is sampled
    :param adim_data: Data to interpolate
    """
    data = {k: {k1: interpolate.interp1d(time, v1, axis=0) for k1, v1 in v.items()} for k, v in adim_data.items()}
    return data


def comsol_preprocessor(
    comsol_data: deprecated_domain.ReferenceCell, mesh: np.ndarray
) -> Dict[str, Dict[str, interpolate.interp1d]]:
    """
    Pre-process COMSOL data to make it more useful in simulations.

    :param comsol_data: Data to preprocess
    :param mesh: New solution mesh (adimensionalized)
    """
    data = adimensionalize_comsol_data(comsol_data, mesh)
    data = interp_time(comsol_data.time_mesh, data)

    return data


def collect_parameters(
    params: Mapping[str, Mapping[str, float]]
) -> Tuple[Mapping[str, Mapping[str, float]], Mapping[str, float]]:
    """
    Translate deprecated domains into current domain.

    :param params: parameters
    """
    n_dict: MutableMapping[str, Domain[str, float]] = {}
    keys = set()

    for key, value in params.items():
        if key != "const":
            keys.update(list(value.keys()))

    for key in keys:
        n_dict[key] = Domain()
        if params["neg"].get(key, None) is not None:
            n_dict[key].update({"anode": params["neg"][key]})
        if params["sep"].get(key, None) is not None:
            n_dict[key].update({"separator": params["sep"][key]})
        if params["pos"].get(key, None) is not None:
            n_dict[key].update({"cathode": params["pos"][key]})

    return n_dict, params["const"]


class FenicsFunctions:
    """
    Handle the assignment of raw COMSOL data to FEniCS functions.
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, data: Mapping[str, Domain[str, np.ndarray]], function_space: fem.FunctionSpace):
        """
        Initialize FEniCS functions from COMSOL data

        :param data: COMSOL data
        :param function_space: Function space for the FEniCS functions
        """
        self.data = munch.munchify(data)
        self.function_space = function_space

        self.funcs: MutableMapping[str, Mapping[str, fem.Function]] = {}
        for fname, fval in data.items():
            self.funcs[fname] = {k: fem.Function(function_space) for k in fval.keys()}

    def _set(self, dest, source):
        if isinstance(source, np.ndarray):
            dest.vector()[:] = source[fem.dof_to_vertex_map(self.function_space)].astype("double")

    def update(self, time):
        """
        Update the FEniCS function values for the current time. Interpolates the data as required.

        :param time: Time at which to assign the function
        """
        for fname, domains in self.funcs.items():
            for key, value in domains.items():
                self._set(value, self.data[fname][key](time))
