"""
Tools for better reporting of the solution
"""
import json
from typing import Optional

import numpy as np
from matplotlib import pyplot as plt  # type: ignore

from mtnlion.tools.helpers import norm_rmse, overlay_plt, save_fig


class Report:
    """
    Simplify the reporting of the gathered solutions.
    """

    def __init__(self, solution, sample_times, split=False, comsol_data=None):
        """
        Create a reporting object.

        :param solution: solution data
        :param sample_times: times at which to resample the data
        :param split: if true split the report by subdomain
        :param comsol_data: data to compare against
        """
        self.sample_times = sample_times
        self.solution = solution
        self.solutions = self.solution.interp_time(solution.time, self.solution.solutions)
        self.split = split
        if comsol_data is None:
            self.comsol_data = {}
        else:
            self.comsol_data = comsol_data.copy()
        self.order = ["anode", "separator", "cathode"]
        self._handle_join()

    def _handle_join(self):
        if not self.split:
            self.mesh = np.concatenate((self.solution.mesh, self.solution.mesh + 1, self.solution.mesh + 2))
            for name, domains in self.solutions.items():
                data = None
                cs_data = None
                for domain in self.order:
                    if domains.get(domain, None) is None:
                        tmp = np.empty((data.shape[0], len(self.solution.mesh)))
                        tmp.fill(np.nan)
                        data = np.append(data, tmp, axis=1)
                        cs_data = np.append(cs_data, tmp, axis=1)
                        continue

                    if data is None:
                        data = domains[domain](self.sample_times)
                        if name in self.comsol_data:
                            cs_data = self.comsol_data[name][domain](self.sample_times)
                        else:
                            cs_data = np.empty((data.shape[0], len(self.solution.mesh)))
                            cs_data.fill(np.nan)
                    else:
                        data = np.append(data, domains[domain](self.sample_times), axis=1)
                        if name in self.comsol_data:
                            cs_data = np.append(cs_data, self.comsol_data[name][domain](self.sample_times), axis=1)
                        else:
                            tmp = np.empty((data.shape[0], len(self.solution.mesh)))
                            tmp.fill(np.nan)
                            cs_data = np.append(cs_data, tmp, axis=1)
                self.solutions[name] = data
                self.comsol_data[name] = cs_data
        else:
            self.solutions = {
                name: {domain: data(self.sample_times) for domain, data in domains.items()}
                for name, domains in self.solutions.items()
            }
            self.comsol_data = {
                name: {domain: data(self.sample_times) for domain, data in domains.items()}
                for name, domains in self.comsol_data.items()
            }

    @staticmethod
    def _format_name(name, domain):
        lookup = {
            "phis": r"$\Phi_s$",
            "phie": r"$\Phi_e$",
            "cs": "$c_$",
            "ce": "$c_e$",
            "j": "$j$",
            "cse": r"$c_{s,e}$",
            "js": "$j_s$",
        }

        return "{}: {}".format(lookup.get(name, name), domain) if domain else "{}".format(lookup.get(name, name))

    def plot(self, local_path: Optional[str] = None, save: Optional[str] = None):
        """
        Plot the stored solutions.

        :param local_path: Path of the calling module
        :param save: true to save the plot to disk
        """
        if self.split:
            for name, domains in self.solutions.items():
                for domain, data in domains.items():
                    fig = overlay_plt(
                        self.solution.mesh,
                        self.sample_times,
                        self._format_name(name, domain),
                        data,
                        self.comsol_data[name][domain],
                    )
                    plt.show()
                    if save is not None and local_path is not None:
                        save_fig(fig, local_path, "{}/{}_{}.png".format(save, name, domain))
        else:
            for name, data in self.solutions.items():
                fig = overlay_plt(
                    self.mesh, self.sample_times, self._format_name(name, ""), data, self.comsol_data[name]
                )
                plt.show()
                if save is not None and local_path is not None:
                    save_fig(fig, local_path, "{}/{}.png".format(save, name))

    def report_rmse(self):
        """
        Report the normalized RMSE
        """
        if self.split:
            return json.dumps(
                {
                    name: {
                        domain: norm_rmse(estimated, self.comsol_data[name][domain]).tolist()
                        for domain, estimated in domains.items()
                    }
                    for name, domains in self.solutions.items()
                },
                indent=4,
            )
        return json.dumps(
            {
                name: norm_rmse(estimated, self.comsol_data[name]).tolist()
                for name, estimated in self.solutions.items()
                if not np.all(np.isnan(self.comsol_data[name]))
            },
            indent=4,
        )
