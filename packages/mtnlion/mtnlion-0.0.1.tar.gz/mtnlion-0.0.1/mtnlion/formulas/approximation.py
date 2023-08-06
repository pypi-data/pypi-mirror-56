"""
Tools for approximating functions
"""
import mpmath  # type: ignore
import numpy as np

from mtnlion.tools.cache import persist_to_npy_file


class Legendre:
    """
    Generate Legendre matrices from Eqs. (3.30) and (3.31) in "Continuum-Scale Lithium-Ion Battery Cell Model in FEniCS"
    """

    def __init__(self, num_functions: int):
        """
        Initialize with the number of polynomials to approximate with

        :param num_functions: Number of polynomials to approximate with
        """
        self.num_functions = num_functions

        self.M_vec = np.vectorize(self.Mmn)  # pylint: disable=invalid-name
        self.K_vec = np.vectorize(self.Kmn)  # pylint: disable=invalid-name

    @staticmethod
    def Mmn(row: int, col: int) -> float:  # pylint: disable=invalid-name
        """
        Calculate the Mmn matrix entries

        :param row: row to calculate
        :param col: column to calculate
        """
        return float(
            mpmath.quad(lambda r: r ** 2 * mpmath.legendre(row, 2 * r - 1) * mpmath.legendre(col, 2 * r - 1), [0, 1])
        )

    @staticmethod
    def Kmn(row: int, col: int) -> float:  # pylint: disable=invalid-name
        """
        Calculate the Kmn matrix entries

        :param row: row to calculate
        :param col: column to calculate
        """

        def d_legendre(order: int, radius: float) -> float:
            """
            Calculate the derivative of the shifted legendre polynomial.

            :param order: Order of the polynomial
            :param radius: Point to calculate derivative
            """
            return mpmath.diff(lambda x: mpmath.legendre(order, 2 * x - 1), radius)

        return float(mpmath.quad(lambda r: r ** 2 * d_legendre(row, r) * d_legendre(col, r), [0, 1]))

    @property  # type: ignore
    @persist_to_npy_file(
        "legendre_m.npy", lambda cache, cls, *_: cache.shape[0] < cls.num_functions
    )  # pylint: disable=invalid-name
    def M(self):
        """
        Calculate the Mmn matrix.
        """
        return np.fromfunction(self.M_vec, (self.num_functions, self.num_functions))

    @property  # type: ignore
    @persist_to_npy_file(
        "legendre_k.npy", lambda cache, cls, *_: cache.shape[0] < cls.num_functions
    )  # pylint: disable=invalid-name
    def K(self):
        """
        Calculate the Kmn matrix
        """
        return np.fromfunction(self.K_vec, (self.num_functions, self.num_functions))
