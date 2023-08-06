# TODO: fix pylint
# pylint:disable=all

from mtnlion.formula import Formula, TrialFunction
from mtnlion.models import newman_isothermal


class DoubleLayer(newman_isothermal.NewmanIsothermal):
    def __init__(self, hyper_params, Ns):
        super(DoubleLayer, self).__init__(hyper_params, Ns)

    def _trial_functions(self):
        return [TrialFunction("jf", ["anode", "cathode"]), TrialFunction("jdl", ["anode", "cathode"])] + super(
            DoubleLayer, self
        )._trial_functions()

    def _formulas(self):
        return [self._TotalFlux(), self._DoubleLayer()] + super(DoubleLayer, self)._formulas()

    class _ButlerVolmer(newman_isothermal.NewmanIsothermal._ButlerVolmer):
        def __init__(self, domains=None, trial_functions=None, test_functions=None, **kwargs):
            domains = self._set(domains, ["anode", "cathode"])
            trial_functions = self._set(trial_functions, ["jf"])
            test_functions = self._set(test_functions, ["v"])
            super(DoubleLayer._ButlerVolmer, self).__init__(
                domains=domains, trial_functions=trial_functions, test_functions=test_functions, **kwargs
            )

        def _form_(self, jf, i0, eta, alpha, F, R, T, v):
            return super(DoubleLayer._ButlerVolmer, self)._form_(jf, i0, eta, alpha, F, R, T, v)

    class _SolidConcentrationNeumann(newman_isothermal.NewmanIsothermal._SolidConcentrationNeumann):
        def __init__(self, domains=None, trial_functions=None, test_functions=None, **kwargs):
            domains = self._set(domains, ["anode", "cathode"])
            trial_functions = self._set(trial_functions, ["cs", "jf"])
            test_functions = self._set(test_functions, ["v_cs"])
            super(DoubleLayer._SolidConcentrationNeumann, self).__init__(
                domains=domains, trial_functions=trial_functions, test_functions=test_functions, **kwargs
            )

        def _form_(self, jf, v_cs):
            return super(DoubleLayer._SolidConcentrationNeumann, self)._form_(jf, v_cs)

    class _TotalFlux(Formula):
        def __init__(self, domains=None, trial_functions=None, test_functions=None, **kwargs):
            domains = self._set(domains, ["anode", "cathode"])
            trial_functions = self._set(trial_functions, ["j", "jf", "jdl"])
            test_functions = self._set(test_functions, ["v"])
            super(DoubleLayer._TotalFlux, self).__init__(
                domains=domains, trial_functions=trial_functions, test_functions=test_functions, **kwargs
            )

        def _form_(self, j, jf, jdl, v):
            return (j - (jf + jdl)) * v

    class _DoubleLayer(Formula):
        def __init__(self, domains=None, trial_functions=None, test_functions=None, time_derivatives=None, **kwargs):
            domains = self._set(domains, ["anode", "cathode"])
            trial_functions = self._set(trial_functions, ["jdl", "phis", "phie"])
            test_functions = self._set(test_functions, ["v"])
            time_derivatives = self._set(time_derivatives, ["dt_jdl", "dt_phis", "dt_phie"])
            super(DoubleLayer._DoubleLayer, self).__init__(
                domains=domains,
                trial_functions=trial_functions,
                test_functions=test_functions,
                time_derivatives=time_derivatives,
                **kwargs,
            )

        def _form_(self, dt_jdl, jdl, dt_phis, phis, dt_phie, phie, Cdl, Rdl, F, a_s, L, v):
            lhs = (Cdl) * (dt_phis - dt_phie) / F
            rhs = Rdl * (Cdl) * dt_jdl + jdl

            return (lhs - rhs) * v
