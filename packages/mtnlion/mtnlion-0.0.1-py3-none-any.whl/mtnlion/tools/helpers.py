"""
Assorted useful helper functions
"""
import os
import time
from typing import Mapping, Tuple

import dolfin as fem
import munch
import numpy as np
from matplotlib import pyplot as plt  # type: ignore
from scipy import interpolate

from mtnlion import engine
from mtnlion.domain import Domain, eval_domain


@eval_domain("auto")
def interp_time2(sample_time: np.ndarray, data: np.ndarray) -> interpolate.interp1d:
    """
    Interpolate time for all elements in a domain.

    :param sample_time: Times at which the data is sampled
    :param data: Data to interpolate
    """
    return interpolate.interp1d(sample_time, data, axis=0, fill_value="extrapolate")


def set_domain_data(anode=None, cathode=None, separator=None):
    """
    Convenience function for unpacking data into a dictionary

    :param anode:
    :param cathode:
    :param separator:
    """
    data = Domain()
    if anode is not None:
        data["anode"] = anode

    if separator is not None:
        data["separator"] = separator

    if cathode is not None:
        data["cathode"] = cathode

    return data


def create_solution_matrices(num_rows: int, num_cols: int, num_solutions: int) -> Tuple[np.ndarray, ...]:
    """
    Create numpy arrays for storing data.

    :param num_rows:
    :param num_cols:
    :param num_solutions:
    :return:
    """
    return tuple(np.empty((num_rows, num_cols)) for _ in range(num_solutions))


def get_1d(func: fem.Function, V: fem.FunctionSpace) -> np.ndarray:  # pylint: disable=invalid-name
    """
    Fetch the one-dimensional solution from a FEniCS function

    :param func: FEniCS function
    :param V: Function space
    """
    return func.vector().get_local()[fem.vertex_to_dof_map(V)]


def save_fig(fig: plt.Figure, local_module_path: str, name: str):
    """
    Save a figure to the given path using the given name

    :param fig: figure to save
    :param local_module_path: path at which to save
    :param name: name of the file
    """
    file = os.path.join(os.path.dirname(local_module_path), name)
    directory = os.path.dirname(os.path.abspath(file))
    if not os.path.exists(directory):
        os.makedirs(directory)

    fig.savefig(name)


def overlay_plt(
    xdata: np.ndarray,
    sample_time: np.ndarray,
    title: str,
    *ydata: np.ndarray,
    figsize: Tuple[int, int] = (15, 9),
    linestyles: Tuple[str, str] = ("-", "--"),
):
    """
    Plot solution data at multiple time slices against a comparison data set.

    :param xdata: Common x axis
    :param sample_time: Sample times
    :param title: Title of the plot
    :param ydata: One or more sets of data in both space and time
    :param figsize: Size of the figure
    :param linestyles: style of the lines
    """
    fig, ax = plt.subplots(figsize=figsize)  # pylint: disable=invalid-name

    new_x = np.repeat([xdata], len(sample_time), axis=0).T

    for i, data in enumerate(ydata):
        if i == 1:
            plt.plot(new_x, data.T, linestyles[i], marker="o")
        else:
            plt.plot(new_x, data.T, linestyles[i])
        plt.gca().set_prop_cycle(None)
    plt.grid()
    plt.title(title)

    legend1 = plt.legend(
        ["t = {}".format(t) for t in sample_time], title="Time", bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.0
    )
    ax.add_artist(legend1)

    h = [  # pylint: disable=invalid-name
        plt.plot([], [], color="gray", ls=linestyles[i])[0] for i in range(len(linestyles))
    ]
    plt.legend(
        handles=h, labels=["FEniCS", "COMSOL"], title="Solver", bbox_to_anchor=(1.01, 0), loc=3, borderaxespad=0.0
    )

    return fig


def norm_rmse(estimated: np.ndarray, true: np.ndarray):
    """
    Calculate the normalized RMSE

    :param estimated: Estimated quantity
    :param true: True quantity
    """
    estimated = estimated[:, ~np.isnan(estimated).any(axis=0)]
    true = true[:, ~np.isnan(true).any(axis=0)]
    return engine.rmse(estimated, true) / (np.max(true) - np.min(true))


class Timer:
    """
    Convenient class for measuring time with `with` operators.
    """

    def __init__(self):
        self.start = None
        self.end = None
        self.interval = None

    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start


def gather_expressions() -> Mapping[str, str]:
    """
    Collect C++ based expressions
    :return: Dictionary of C++ strings
    """
    # TODO: read entire directory
    localdir = os.path.dirname(__file__)
    code = dict()
    with open(os.path.join(localdir, "../headers/xbar.h")) as file:
        code["xbar"] = "".join(file.readlines())

    with open(os.path.join(localdir, "../headers/composition.h")) as file:
        code["composition"] = "".join(file.readlines())

    with open(os.path.join(localdir, "../headers/piecewise.h")) as file:
        code["piecewise"] = "".join(file.readlines())

    with open(os.path.join(localdir, "../headers/xbar_simple.h")) as file:
        code["xbar_simple"] = "".join(file.readlines())

    with open(os.path.join(localdir, "../headers/template.h")) as file:
        code["template"] = "".join(file.readlines())

    with open(os.path.join(localdir, "../newman/j_newman.h")) as file:
        code["j_newman"] = "".join(file.readlines())

    return munch.Munch(code)


# TODO: this is ugly
EXPRESSIONS = gather_expressions()


def build_expression_class(class_name: str, eval_expr: str, **kwargs: Mapping[str, str]):
    """
    Create a FEniCS C++ expression from a template

    :param class_name: Name of the expression
    :param eval_expr: Expression to evaluate
    :param kwargs: Required arguments
    """

    # pylint: disable=too-many-locals

    generic_func_preamble = "std::shared_ptr<dolfin::GenericFunction> "
    eigen_map = "Eigen::Map<Eigen::Matrix<double, 1, 1>>"
    generic_func_vars = list(kwargs)
    generic_func_vars_declare = ["double " + v + ";" for v in generic_func_vars]
    generic_funcs = ["generic_function_" + v for v in generic_func_vars]
    generic_func_eval = [
        f + "->eval({} (&{}), x, cell);".format(eigen_map, v) for f, v in zip(generic_funcs, generic_func_vars)
    ]
    generic_func_expose = [
        '.def_readwrite("{}", &{}::{})'.format(v, class_name, g) for v, g in zip(generic_func_vars, generic_funcs)
    ]

    # Find the proper indent level... Not really a requirement, I'm just OCD. But man, this is UGLY.
    template_list = EXPRESSIONS["template"].split("\n")
    keys = ("{COMMANDS}", "{GENERIC_FUNCTIONS}", "{EXPOSE_GENERIC_FUNCTIONS}")
    indents = {}
    for template in template_list:
        for key in keys:
            if key in template:
                indents[key] = "\n"
                for char in template.split(key)[0]:
                    if char.isspace():
                        indents[key] += " "

    eval_command = "values[0] = " + eval_expr + ";"

    commands = (
        indents[keys[0]].join(generic_func_vars_declare)
        + indents[keys[0]]
        + indents[keys[0]].join(generic_func_eval)
        + indents[keys[0]]
        + eval_command
    )

    generic_functions = indents[keys[1]].join("{} {};".format(generic_func_preamble, t) for t in generic_funcs)
    expose_generic_functions = indents[keys[2]].join(generic_func_expose)

    return EXPRESSIONS["template"].format(
        CLASS_NAME=class_name,
        COMMANDS=commands,
        GENERIC_FUNCTIONS=generic_functions,
        EXPOSE_GENERIC_FUNCTIONS=expose_generic_functions,
    )
