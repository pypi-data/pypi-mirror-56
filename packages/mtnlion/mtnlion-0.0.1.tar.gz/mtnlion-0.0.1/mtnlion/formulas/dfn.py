"""
A collection of formulas useful for the Doyl-Fuller-Newman cell model
"""
import ufl  # type: ignore
from ufl import algebra  # type: ignore

import mtnlion.formula
import mtnlion.tools.cache

SAFE_DICT = {"abs": algebra.Abs}
FENICS_SAFE_LIST = [
    "max_value",
    "min_value",
    "sign",
    "sqrt",
    "exp",
    "ln",
    "erf",
    "cos",
    "sin",
    "tan",
    "acos",
    "asin",
    "atan",
    "atan_2",
    "cosh",
    "sinh",
    "tanh",
    "bessel_J",
    "bessel_Y",
    "bessel_I",
    "bessel_K",
]

SAFE_DICT.update({(k, getattr(ufl, k)) for k in FENICS_SAFE_LIST})


class SOC(mtnlion.formula.FormulaDAE):
    """
    State of Charge (SOC) formula.
    """

    # pylint: disable=too-few-public-methods
    # pylint: disable=arguments-differ

    def __init__(self):
        super(SOC, self).__init__(name="soc", domains=["anode", "cathode"])

    def _form_(self, cse, csmax):
        """Evaluate the open-circuit potential equation."""
        soc = cse / csmax
        return soc


class Uocp(mtnlion.formula.FormulaDAE):
    """
    Open-circuit potential formula.
    """

    # pylint: disable=too-few-public-methods
    # pylint: disable=arguments-differ
    # pylint: disable=eval-used
    # TODO: remove evals

    def __init__(self, uocp_str):
        self.uocp_str = uocp_str
        super(Uocp, self).__init__(name="Uocp", domains=["anode", "cathode"], pass_domain=True)

    def _form_(self, soc, domain):
        """Evaluate the open-circuit potential equation."""
        return eval(str(self.uocp_str[domain]), {"__builtins__": None}, {"soc": soc, **SAFE_DICT})


class KappaRef(mtnlion.formula.FormulaDAE):
    """
    Bulk conductivity of the homogeneous materials.
    """

    # pylint: disable=too-few-public-methods
    # pylint: disable=arguments-differ
    # pylint: disable=eval-used
    # TODO: remove evals

    def __init__(self, kappa_ref):
        self.kappa_ref = kappa_ref
        super(KappaRef, self).__init__(
            name="kappa_ref", domains=["anode", "separator", "cathode"], trial_functions=["ce"]
        )

    def _form_(self, ce):
        return eval(str(self.kappa_ref), {"__builtins__": None}, {"x": ce, **SAFE_DICT})


class KappaEff(mtnlion.formula.Formula):
    """
    Effective conductivity of the electrolyte.
    """

    # pylint: disable=too-few-public-methods
    # pylint: disable=arguments-differ

    def __init__(self):
        super(KappaEff, self).__init__(name="kappa_eff", domains=["anode", "separator", "cathode"])

    def _form_(self, kappa_ref, eps_e, brug_kappa):
        kappa_eff = kappa_ref * eps_e ** brug_kappa
        return kappa_eff


class KappaDEff(mtnlion.formula.Formula):
    """
    kappa_d effective
    """

    # pylint: disable=too-few-public-methods
    # pylint: disable=arguments-differ

    def __init__(self):
        super(KappaDEff, self).__init__(name="kappa_Deff", domains=["anode", "separator", "cathode"])

    def _form_(self, kappa_ref, eps_e, kappa_D):
        return kappa_D * kappa_ref * eps_e
