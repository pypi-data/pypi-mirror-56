"""
Tools for assembling problem spaces.
"""
import dolfin as fem
import ufl.algebra  # type: ignore

from mtnlion.domain import Domain
from mtnlion.problem_space import ProblemSpaceAssembler


class OneDimensionalAssembler(ProblemSpaceAssembler):
    """
    Defines process for assembling a one dimensional problem
    """

    @staticmethod
    def _assemble_boundary(bound: Domain[str, ufl.algebra.Expr], ds: fem.Measure) -> Domain[str, fem.Form]:
        if len(bound) == 1:
            if "anode" in bound:
                bound *= ds(0)  # type: ignore
            elif "cathode" in bound:
                bound *= ds(1)  # type: ignore
            elif "separator" in bound:
                bound["anode"] *= ds(1)
                bound["separator"] *= ds
                bound["cathode"] *= ds(0)
            else:
                raise RuntimeError("Unable to handle boundary condition")
        elif len(bound) == 2:
            if "anode" in bound and "separator" in bound:
                bound["anode"] *= ds(1)
                bound["separator"] = -bound["separator"] * ds(0)
            elif "cathode" in bound and "separator" in bound:
                bound["cathode"] *= ds(0)
                bound["separator"] = -bound["separator"] * ds(1)
            elif "anode" in bound and "cathode" in bound:
                bound["cathode"] *= ds(1)
                bound["anode"] *= ds(0)
            else:
                raise RuntimeError("Unable to handle boundary condition")
        else:
            raise RuntimeError("Unable to handle boundary condition")
        return bound  # type: ignore
