from experiment_utils.config_manager import ConfigManager
from experiment_utils.metrics_manager import MetricsManager
from experiment_utils.plot_manager import PlotManager

config = ConfigManager('experiments/preliminary/preliminary_experiment.yaml')

# === LOAD METRICS ===
metrics_manager = MetricsManager(config)
metrics_dict = metrics_manager.load_metrics()
frob_errors_dict = metrics_dict['frob_errors_dict']
bhv_distances_dict = metrics_dict['bhv_distances_dict']
frob_biases_dict = metrics_dict['frob_biases_dict']
frob_variances_dict = metrics_dict['frob_variances_dict']

# === PLOT METRICS ===
nleaves_list = config.get_sampling_config().get('nleaves_list')
estimators = config.get_reconstruction_config().get('estimators')

# === FIGURE 8 ===
estimators_fig8 = ["bmtm-mle", "ddgm-mle"]
plot_manager = PlotManager(config, estimators_fig8, nleaves_list)
plot_manager.plot_errorbars(
    frob_biases_dict, 
    ylabel="estimator bias (Frobenius squared)", 
    filename="fig8_biases.png",
    yscale='log'
)
plot_manager.plot_errorbars(
    frob_variances_dict, 
    ylabel="estimator variance (Frobenius squared)", 
    filename="fig8_variance.png",
    yscale='log'
)
plot_manager.plot_errorbars(
    frob_variances_dict, 
    ylabel="estimator risk (Frobenius squared)", 
    filename="fig8_risk.png",
    yscale='linear'
)
# plot_manager.plot_errorbars(
#     frob_variances_dict, 
#     ylabel="estimator risk (Frobenius variance)", 
#     filename="frob_variances.png",
#     yscale='log'
# )