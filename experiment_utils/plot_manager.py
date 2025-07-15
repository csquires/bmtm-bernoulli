import os

import matplotlib.pyplot as plt
import numpy as np

from experiment_utils.config_manager import ConfigManager


class PlotManager:
    def __init__(self, config: ConfigManager, estimators: list, nleaves_list: list):
        self.config = config
        self.estimators = estimators
        self.nleaves_list = nleaves_list
        self.nsizes = len(nleaves_list)
        self.num_estimators = len(estimators)

    def _compute_errorbars(self, errors_dict):
        errorbars_dict = dict()
        for e_ix, estimator in enumerate(self.estimators):
            means = np.zeros(self.nsizes)
            error_mat = np.zeros((2, self.nsizes))
            for x, nleaves in enumerate(self.nleaves_list):
                errors = errors_dict[(estimator, nleaves)]
                mid = np.median(errors)
                low = np.percentile(errors, 10)
                high = np.percentile(errors, 90)
                means[x] = float(mid)
                error_mat[0, x] = float(mid - low)
                error_mat[1, x] = float(high - mid)
            errorbars_dict[estimator] = (means, error_mat)
        return errorbars_dict

    def plot_errorbars(self, errors_dict, ylabel, filename, yscale='linear', legend_right=False):
        errorbars_dict = self._compute_errorbars(errors_dict)
        jitter = 0.08
        plt.clf()
        xs = np.arange(self.nsizes)
        for e_ix, estimator in enumerate(self.estimators):
            means = errorbars_dict[estimator][0]
            errors = errorbars_dict[estimator][1]
            plt.errorbar(xs + e_ix * jitter, means, yerr=errors, label=estimator, fmt="o", capsize=5)

        # === OTHER ===
        plt.yscale(yscale)
        if legend_right:
            plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        else:
            plt.legend()

        # === AXIS LABELS ===
        plt.xticks(xs + jitter * self.num_estimators / 2, self.nleaves_list)
        plt.xlabel("# of leaves")
        plt.ylabel(ylabel)

        # === SAVE FIGURE ===
        figures_dir = self.config.get_paths_config().get('figures_dir')
        os.makedirs(figures_dir, exist_ok=True)
        figure_filename = figures_dir + f'/{filename}'
        plt.savefig(figure_filename)