"""
Base Newman isothermal model
"""

# TODO: fix pylint
# pylint:disable=all

import dolfin as fem

import mtnlion.formulas.approximation
import mtnlion.formulas.dfn
from mtnlion import model
from mtnlion.formula import Formula, FormulaDAE, LagrangeMultiplier, TrialFunction


# TODO: Investigate using TrialFunction in place of Formula.trialfunctions
class NewmanIsothermal(model.Model):
    def __init__(self, hyper_params, Ns):
        """
        Defines the basic Newman Isothermal model.

        :param hyper_params: Non-function parameters
        :param Ns: Number of Legendre polynomials to approximate cs
        """
        self.Ns = Ns

        super(NewmanIsothermal, self).__init__(hyper_params)

    def _trial_functions(self):
        return [
            TrialFunction("j", ["anode", "cathode"]),
            TrialFunction("phis", ["anode", "cathode"]),
            TrialFunction("phie", ["anode", "separator", "cathode"]),
            TrialFunction("cs", ["anode", "cathode"], num_functions=self.Ns),
            TrialFunction("ce", ["anode", "separator", "cathode"]),
            TrialFunction("lm_phis_gnd", ["anode"]),
            TrialFunction("lm_phie_as", ["anode", "separator"]),
            TrialFunction("lm_phie_sc", ["separator", "cathode"]),
            TrialFunction("lm_ce_as", ["anode", "separator"]),
            TrialFunction("lm_ce_sc", ["separator", "cathode"]),
        ]

    def _formulas(self):
        legendre = mtnlion.formulas.approximation.Legendre(self.Ns)
        return [
            self._ButlerVolmer(),
            self._SolidPotential(),
            self._ElectrolytePotential(),
            self._SolidConcentration(legendre=legendre),
            self._ElectrolyteConcentration(),
            self._SolidConcentrationBoundary(),
            self._SolidPotentialNeumann(["anode"]),
            self._SolidPotentialNeumann(["cathode"]),
            self._SolidConcentrationNeumann(),
            self._ExchangeCurrentDensity(),
            self._Eta(),
            LagrangeMultiplier(["anode"], "lm_phis_gnd", "phis"),
            LagrangeMultiplier(["anode", "separator"], "lm_phie_as", "phie"),
            LagrangeMultiplier(["separator", "cathode"], "lm_phie_sc", "phie"),
            LagrangeMultiplier(["anode", "separator"], "lm_ce_as", "ce"),
            LagrangeMultiplier(["separator", "cathode"], "lm_ce_sc", "ce"),
        ]

    class _ButlerVolmer(Formula):
        def __init__(self, domains=None, trial_functions=None, test_functions=None, **kwargs):
            domains = self._set(domains, ["anode", "cathode"])
            trial_functions = self._set(trial_functions, ["j"])
            test_functions = self._set(test_functions, ["v"])
            super(NewmanIsothermal._ButlerVolmer, self).__init__(
                domains=domains, trial_functions=trial_functions, test_functions=test_functions, **kwargs
            )

        def _form_(self, j, i0, eta, alpha, F, R, T, v):
            """Flux through the boundary of the solid."""
            return (j - i0 * (fem.exp((1 - alpha) * F * eta / (R * T)) - fem.exp(-alpha * F * eta / (R * T)))) * v

    class _SolidPotential(Formula):
        def __init__(self, domains=None, trial_functions=None, test_functions=None, **kwargs):
            domains = self._set(domains, ["anode", "cathode"])
            trial_functions = self._set(trial_functions, ["phis", "j"])
            test_functions = self._set(test_functions, ["v_phis"])
            super(NewmanIsothermal._SolidPotential, self).__init__(
                domains=domains, trial_functions=trial_functions, test_functions=test_functions, **kwargs
            )

        def _form_(self, phis, v_phis, a_s, F, sigma_eff, L, j):
            """Charge conservation in the solid."""
            lhs = -sigma_eff / L * fem.dot(fem.grad(phis), fem.grad(v_phis))
            rhs = L * a_s * F * j * v_phis

            return rhs - lhs

    class _ElectrolytePotential(Formula):
        def __init__(self, domains=None, trial_functions=None, test_functions=None, pass_domain=True, **kwargs):
            domains = self._set(domains, ["anode", "separator", "cathode"])
            trial_functions = self._set(trial_functions, ["phie", "ce", "j"])
            test_functions = self._set(test_functions, ["v_phie"])
            super(NewmanIsothermal._ElectrolytePotential, self).__init__(
                domains=domains,
                trial_functions=trial_functions,
                test_functions=test_functions,
                pass_domain=pass_domain,
                **kwargs,
            )

        def _form_(self, ce, phie, v_phie, kappa_eff, kappa_Deff, L, a_s, F, j, domain):
            if domain == "separator":
                j = 0

            """Charge conservation in the electrolyte."""
            lhs = kappa_eff / L * fem.dot(fem.grad(phie), fem.grad(v_phie))  # all domains
            rhs1 = -kappa_Deff / L * fem.dot(fem.grad(fem.ln(ce)), fem.grad(v_phie))  # all domains
            rhs2 = L * a_s * F * j * v_phie  # electrodes

            return lhs - rhs1 - rhs2

    class _SolidConcentration(Formula):
        def __init__(
            self, legendre, domains=None, trial_functions=None, test_functions=None, time_derivatives=None, **kwargs
        ):
            self.legendre = legendre
            self.Ns = legendre.num_functions

            domains = self._set(domains, ["anode", "cathode"])
            trial_functions = self._set(trial_functions, ["cs"])
            test_functions = self._set(test_functions, ["v_cs"])
            time_derivatives = self._set(time_derivatives, ["dt_cs"])
            super(NewmanIsothermal._SolidConcentration, self).__init__(
                domains=domains,
                trial_functions=trial_functions,
                test_functions=test_functions,
                time_derivatives=time_derivatives,
                **kwargs,
            )

        def _form_(self, dt_cs, cs, v_cs, Rs, Ds_ref):
            """Concentration of lithium in the solid."""
            """time_integration, cs, v are lists of length num_functions"""

            M = self.legendre.M
            K = self.legendre.K

            lhs_terms = [M[m, n] * dt_cs[n] * v_cs[m] for m in range(self.Ns) for n in range(self.Ns)]
            rhs_terms = [K[m, n] * cs[n] * v_cs[m] for m in range(self.Ns) for n in range(self.Ns)]

            lhs = sum(lhs_terms) * Rs
            rhs = sum(rhs_terms) * Ds_ref / Rs

            return rhs + lhs

    class _ElectrolyteConcentration(Formula):
        def __init__(
            self,
            domains=None,
            trial_functions=None,
            test_functions=None,
            time_derivatives=None,
            pass_domain=True,
            **kwargs,
        ):
            domains = self._set(domains, ["anode", "separator", "cathode"])
            trial_functions = self._set(trial_functions, ["ce", "phie", "j"])
            test_functions = self._set(test_functions, ["v_ce"])
            time_derivatives = self._set(time_derivatives, ["dt_ce"])
            super(NewmanIsothermal._ElectrolyteConcentration, self).__init__(
                domains=domains,
                trial_functions=trial_functions,
                test_functions=test_functions,
                time_derivatives=time_derivatives,
                pass_domain=pass_domain,
                **kwargs,
            )

        def _form_(self, dt_ce, ce, v_ce, a_s, De_eff, t_plus, L, eps_e, j, domain):
            if domain == "separator":
                j = 0

            """Concentration of lithium in the electrolyte."""
            lhs = L * eps_e * v_ce  # all domains
            rhs1 = -De_eff / L * fem.dot(fem.grad(ce), fem.grad(v_ce))  # all domains
            rhs2 = L * a_s * (1 - t_plus) * j * v_ce  # electrodes

            return lhs * dt_ce - rhs1 - rhs2

    class _SolidConcentrationBoundary(FormulaDAE):
        def __init__(self, name="cse", domains=None, trial_functions=None, **kwargs):
            domains = self._set(domains, ["anode", "cathode"])
            trial_functions = self._set(trial_functions, ["cs"])
            super(NewmanIsothermal._SolidConcentrationBoundary, self).__init__(
                name=name, domains=domains, trial_functions=trial_functions, **kwargs
            )

        def _form_(self, cs):
            return sum(cs)

    class _SolidPotentialNeumann(Formula):
        def __init__(self, domains=None, trial_functions=None, test_functions=None, **kwargs):
            domains = self._set(domains, ["anode", "cathode"])
            trial_functions = self._set(trial_functions, ["phis"])
            test_functions = self._set(test_functions, ["v"])
            super(NewmanIsothermal._SolidPotentialNeumann, self).__init__(
                domains=domains, trial_functions=trial_functions, test_functions=test_functions, boundary=True, **kwargs
            )

        def _form_(self, Iapp, Acell, v):
            return Iapp / Acell * v

    class _SolidConcentrationNeumann(Formula):
        def __init__(self, domains=None, trial_functions=None, test_functions=None, **kwargs):
            domains = self._set(domains, ["anode", "cathode"])
            trial_functions = self._set(trial_functions, ["cs", "j"])
            test_functions = self._set(test_functions, ["v_cs"])
            super(NewmanIsothermal._SolidConcentrationNeumann, self).__init__(
                domains=domains, trial_functions=trial_functions, test_functions=test_functions, **kwargs
            )

        def _form_(self, j, v_cs):
            return j * sum(v_cs)

    class _ExchangeCurrentDensity(FormulaDAE):
        def __init__(self, name="i0", domains=None, trial_functions=None, **kwargs):
            domains = self._set(domains, ["anode", "cathode"])
            trial_functions = self._set(trial_functions, ["ce"])
            super(NewmanIsothermal._ExchangeCurrentDensity, self).__init__(
                name=name, domains=domains, trial_functions=trial_functions, **kwargs
            )

        def _form_(self, ce, cse, csmax, ce0, alpha, k_norm_ref):
            return (
                k_norm_ref
                * (abs(((csmax - cse) / csmax)) ** (1 - alpha))
                * (abs(cse / csmax) ** alpha)
                * (abs(ce / ce0) ** (1 - alpha))
            )

    class _Eta(FormulaDAE):
        def __init__(self, name="eta", domains=None, trial_functions=None, **kwargs):
            domains = self._set(domains, ["anode", "cathode"])
            trial_functions = self._set(trial_functions, ["phis", "phie", "j"])
            super(NewmanIsothermal._Eta, self).__init__(
                name=name, domains=domains, trial_functions=trial_functions, **kwargs
            )

        def _form_(self, phis, phie, Uocp):
            return phis - phie - Uocp
