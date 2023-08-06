"""
Classes for defining time integration methods
"""
from mtnlion.formula import Rothes


class Euler(Rothes):
    """
    First order implicit Euler.
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, trial_functions, delta_t):
        super(Euler, self).__init__(trial_functions=trial_functions, delta_t=delta_t, order=1, domains=["auto"])

    def _form_(self, u_list):
        """
        Create FFL expression for euler explicit/implicit time stepping.
        """
        if isinstance(u_list[0], (list, tuple)):
            if isinstance(u_list[1], (list, tuple)):
                lhs = [(i - j) / self.delta_t for i, j in zip(u_list[0], u_list[1])]
            else:
                raise RuntimeError("Cannot mix iterables with non-iterables")
        else:
            lhs = (u_list[0] - u_list[1]) / self.delta_t

        return lhs
