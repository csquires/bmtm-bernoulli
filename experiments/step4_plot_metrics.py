import os

import numpy as np
import matplotlib.pyplot as plt

from experiment_utils.config_manager import ConfigManager
from experiment_utils.metrics_manager import MetricsManager

config = ConfigManager('experiments/experiment_1.yaml')
plot_manager = MetricsManager(config)
metrics_dict = plot_manager.load_metrics()



frob_errors_dict = metrics_dict['frob_errors_dict']
nleaves_list = config.get_sampling_config().get('nleaves_list')
estimators = config.get_reconstruction_config().get('estimators')
nsizes = len(nleaves_list)
num_estimators = len(estimators)

plt.clf()
nsizes = len(nleaves_list)
xs = np.arange(nsizes)
jitter = 0.1
for e_ix, estimator in enumerate(estimators):
    means = np.zeros(nsizes)
    errors = np.zeros((2, nsizes))
    for x, nleaves in enumerate(nleaves_list):
        frob_errors = frob_errors_dict[(estimator, nleaves)]
        mid = np.median(frob_errors)
        low = np.percentile(frob_errors, 10)
        high = np.percentile(frob_errors, 90)
        means[x] = mid
        errors[0, x] = mid - low
        errors[1, x] = high - mid
        # if low > mid or high < mid:
            # breakpoint()
    plt.errorbar(xs + e_ix * jitter, means, yerr=errors, label=estimator, fmt="o", capsize=5)

plt.yscale("log")
plt.xlabel("# of leaves")
plt.ylabel("estimator risk (Frobenius squared)")
plt.xticks(xs + jitter * num_estimators / 2, nleaves_list)
plt.legend()
figures_dir = config.get_paths_config().get('figures_dir')
os.makedirs(figures_dir, exist_ok=True)
figure_filename = figures_dir + '/frob_errors.png'
plt.savefig(figure_filename)





