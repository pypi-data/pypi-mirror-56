"""
Newman model assuming that ButlerVolmer takes a DAE format
"""
# TODO: fix pylint
# pylint:disable=all

import dolfin as fem

from mtnlion.formula import Formula, FormulaDAE
from mtnlion.models import newman_isothermal


class NewmanIsothermal(newman_isothermal.NewmanIsothermal):
    def __init__(self, hyper_params, Ns):
        super(NewmanIsothermal, self).__init__(hyper_params, Ns)

    def _trial_functions(self):
        trial_functions = super(NewmanIsothermal, self)._trial_functions()
        del trial_functions[trial_functions.index(next(filter(lambda x: x.name == "j", trial_functions)))]
        return trial_functions

    class _ButlerVolmer(FormulaDAE):
        def __init__(self, name="j", domains=None, trial_functions=None, **kwargs):
            domains = self._set(domains, ["anode", "cathode"])
            trial_functions = self._set(trial_functions, None)
            super(NewmanIsothermal._ButlerVolmer, self).__init__(
                name=name, domains=domains, trial_functions=trial_functions, **kwargs
            )

        def _form_(self, i0, eta, alpha, F, R, T):
            """Flux through the boundary of the solid."""
            return i0 * (fem.exp((1 - alpha) * F * eta / (R * T)) - fem.exp(-alpha * F * eta / (R * T)))

    class _SolidPotential(Formula):
        def __init__(self, domains=None, trial_functions=None, test_functions=None, **kwargs):
            domains = self._set(domains, ["anode", "cathode"])
            trial_functions = self._set(trial_functions, ["phis"])
            test_functions = self._set(test_functions, ["v_phis"])
            super(NewmanIsothermal._SolidPotential, self).__init__(
                domains=domains, trial_functions=trial_functions, test_functions=test_functions, **kwargs
            )

        def _form_(self, j, phis, v_phis, a_s, F, sigma_eff, L):
            """Charge conservation in the solid."""
            lhs = -sigma_eff / L * fem.dot(fem.grad(phis), fem.grad(v_phis))
            rhs = L * a_s * F * j * v_phis

            return rhs - lhs

    class _ElectrolytePotential(Formula):
        def __init__(self, domains=None, trial_functions=None, test_functions=None, pass_domain=True, **kwargs):
            domains = self._set(domains, ["anode", "separator", "cathode"])
            trial_functions = self._set(trial_functions, ["phie", "ce"])
            test_functions = self._set(test_functions, ["v_phie"])
            super(NewmanIsothermal._ElectrolytePotential, self).__init__(
                domains=domains,
                trial_functions=trial_functions,
                test_functions=test_functions,
                pass_domain=pass_domain,
                **kwargs,
            )

        def _form_(self, j, ce, phie, v_phie, kappa_eff, kappa_Deff, L, a_s, F, domain):
            if domain == "separator":
                j = 0

            """Charge conservation in the electrolyte."""
            lhs = kappa_eff / L * fem.dot(fem.grad(phie), fem.grad(v_phie))  # all domains
            rhs1 = -kappa_Deff / L * fem.dot(fem.grad(fem.ln(ce)), fem.grad(v_phie))  # all domains
            rhs2 = L * a_s * F * j * v_phie  # electrodes

            return lhs - rhs1 - rhs2

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
            trial_functions = self._set(trial_functions, ["ce", "phie"])
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

        def _form_(self, dt_ce, j, ce, v_ce, a_s, De_eff, t_plus, L, eps_e, domain):
            if domain == "separator":
                j = 0

            """Concentration of lithium in the electrolyte."""
            lhs = L * eps_e * v_ce  # all domains
            rhs1 = -De_eff / L * fem.dot(fem.grad(ce), fem.grad(v_ce))  # all domains
            rhs2 = L * a_s * (1 - t_plus) * j * v_ce  # electrodes

            return lhs * dt_ce - rhs1 - rhs2

    class _SolidConcentrationNeumann(Formula):
        def __init__(self, domains=None, trial_functions=None, test_functions=None, **kwargs):
            domains = self._set(domains, ["anode", "cathode"])
            trial_functions = self._set(trial_functions, ["cs"])
            test_functions = self._set(test_functions, ["v_cs"])
            super(NewmanIsothermal._SolidConcentrationNeumann, self).__init__(
                domains=domains, trial_functions=trial_functions, test_functions=test_functions, **kwargs
            )

        def _form_(self, j, v_cs):
            return j * sum(v_cs)

    class _Eta(FormulaDAE):
        def __init__(self, name="eta", domains=None, trial_functions=None, **kwargs):
            domains = self._set(domains, ["anode", "cathode"])
            trial_functions = self._set(trial_functions, ["phis", "phie", "j"])
            super(NewmanIsothermal._Eta, self).__init__(
                name=name, domains=domains, trial_functions=trial_functions, **kwargs
            )

        def _form_(self, phis, phie, Uocp):
            return phis - phie - Uocp
