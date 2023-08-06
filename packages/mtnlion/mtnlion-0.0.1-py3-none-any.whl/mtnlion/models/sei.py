# TODO: fix pylint
# pylint:disable=all

import dolfin as fem

from mtnlion.formula import Formula, FormulaDAE, TrialFunction
from mtnlion.models import newman_isothermal


class SEI(newman_isothermal.NewmanIsothermal):
    def __init__(self, hyper_params, Ns):
        super(SEI, self).__init__(hyper_params, Ns)

    def _trial_functions(self):
        return [
            TrialFunction("js", ["anode"]),
            TrialFunction("delta_film", ["anode"]),
            TrialFunction("Q", ["anode"]),
        ] + super(SEI, self)._trial_functions()

    def _formulas(self):
        return [
            self._SideReactionFlux(),
            self._SideReactionExchangeCurrentDensity(),
            self._Eta_s(),
            self._FilmThickness(),
            self._FilmResistance(),
            self._CapacityLoss(),
            self._LocalMolecularFlux(),
        ] + super(SEI, self)._formulas()

    class _Eta(FormulaDAE):
        def __init__(self, name="eta", domains=None, trial_functions=None, pass_domain=True, **kwargs):
            domains = self._set(domains, ["anode", "cathode"])
            trial_functions = self._set(trial_functions, ["phis", "phie", "j"])
            super(SEI._Eta, self).__init__(
                name=name, domains=domains, trial_functions=trial_functions, pass_domain=pass_domain, **kwargs
            )

        def _form_(self, phis, phie, Uocp, Uref_sei, F, Rfilm, j_total, j, domain):
            if domain == "anode":
                return phis - phie - Uocp - F * Rfilm * j_total
            elif domain == "cathode":
                return phis - phie - Uocp - F * Rfilm * j

    class _LocalMolecularFlux(FormulaDAE):
        def __init__(self, name="j_total", domains=None, trial_functions=None, **kwargs):
            domains = self._set(domains, ["anode"])
            trial_functions = self._set(trial_functions, ["j", "js"])
            super(SEI._LocalMolecularFlux, self).__init__(
                name=name, domains=domains, trial_functions=trial_functions, **kwargs
            )

        def _form_(self, j, js):
            return j + js

    class _SideReactionFlux(Formula):
        def __init__(self, domains=None, trial_functions=None, test_functions=None, **kwargs):
            domains = self._set(domains, ["anode"])
            trial_functions = self._set(trial_functions, ["js"])
            test_functions = self._set(test_functions, ["v"])
            super(SEI._SideReactionFlux, self).__init__(
                domains=domains, trial_functions=trial_functions, test_functions=test_functions, **kwargs
            )

        def _form_(self, js, io_sei, eta_s, alpha, F, R, T, v):
            """Flux through the boundary of the solid."""
            return (js + io_sei / F * fem.exp(-alpha * F * eta_s / (R * T))) * v

    class _SideReactionExchangeCurrentDensity(FormulaDAE):
        def __init__(self, name="i0_s", domains=None, trial_functions=None, **kwargs):
            domains = self._set(domains, ["anode"])
            trial_functions = self._set(trial_functions, ["ce"])
            super(SEI._SideReactionExchangeCurrentDensity, self).__init__(
                name=name, domains=domains, trial_functions=trial_functions, **kwargs
            )

        def _form_(self, ce, alpha_s, k_norm_ref):
            return k_norm_ref * ce ** alpha_s

    class _Eta_s(FormulaDAE):
        def __init__(self, name="eta_s", domains=None, trial_functions=None, **kwargs):
            domains = self._set(domains, ["anode"])
            trial_functions = self._set(trial_functions, ["phis", "phie"])
            super(SEI._Eta_s, self).__init__(name=name, domains=domains, trial_functions=trial_functions, **kwargs)

        def _form_(self, phis, phie, Uref_sei, F, Rfilm, j_total):
            return phis - phie - Uref_sei - F * Rfilm * j_total

    class _FilmThickness(Formula):
        def __init__(self, domains=None, trial_functions=None, test_functions=None, time_derivatives=None, **kwargs):
            domains = self._set(domains, ["anode"])
            trial_functions = self._set(trial_functions, ["delta_film", "js"])
            test_functions = self._set(test_functions, ["v"])
            time_derivatives = self._set(time_derivatives, ["dt_delta_film"])
            super(SEI._FilmThickness, self).__init__(
                domains=domains,
                trial_functions=trial_functions,
                test_functions=test_functions,
                time_derivatives=time_derivatives,
                **kwargs,
            )

        # TODO: remove requirement for delta_film to be in arg list
        def _form_(self, dt_delta_film, delta_film, Mp, rho_p, v, js):
            lhs = dt_delta_film * v
            rhs = -Mp / rho_p * js * v
            return lhs - rhs

    class _FilmResistance(FormulaDAE):
        def __init__(self, name="Rfilm2", domains=None, trial_functions=None, **kwargs):
            domains = self._set(domains, ["anode"])
            trial_functions = self._set(trial_functions, ["delta_film"])
            super(SEI._FilmResistance, self).__init__(
                name=name, domains=domains, trial_functions=trial_functions, **kwargs
            )

        def _form_(self, delta_film, Rsei, kappa_p):
            return Rsei + delta_film / kappa_p

    class _CapacityLoss(Formula):
        def __init__(self, domains=None, trial_functions=None, test_functions=None, time_derivatives=None, **kwargs):
            domains = self._set(domains, ["anode"])
            trial_functions = self._set(trial_functions, ["Q", "js"])
            test_functions = self._set(test_functions, ["v"])
            time_derivatives = self._set(time_derivatives, ["dt_Q"])
            super(SEI._CapacityLoss, self).__init__(
                domains=domains,
                trial_functions=trial_functions,
                test_functions=test_functions,
                time_derivatives=time_derivatives,
                **kwargs,
            )

        def _form_(self, dt_Q, Q, a_s, Acell, F, v, js, dx):
            lhs = dt_Q * v
            rhs = fem.assemble(a_s * Acell * F * js * dx) * v
            return lhs - rhs
