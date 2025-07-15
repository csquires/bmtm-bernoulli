from experiment_utils.config_manager import ConfigManager
from experiment_utils.metrics_manager import MetricsManager
from experiment_utils.plot_manager import PlotManager

config = ConfigManager('experiments/experiment_1.yaml')

# === LOAD METRICS ===
metrics_manager = MetricsManager(config)
metrics_dict = metrics_manager.load_metrics()
frob_errors_dict = metrics_dict['frob_errors_dict']
bhv_distances_dict = metrics_dict['bhv_distances_dict']

# === PLOT METRICS ===
nleaves_list = config.get_sampling_config().get('nleaves_list')
estimators = config.get_reconstruction_config().get('estimators')

plot_manager = PlotManager(config, estimators, nleaves_list)
plot_manager.plot_errorbars(
    frob_errors_dict, 
    ylabel="estimator risk (Frobenius squared)", 
    filename="frob_errors.png",
    yscale='log'
)
plot_manager.plot_errorbars(
    bhv_distances_dict, 
    ylabel="estimator risk (BHV distance)", 
    filename="bhv_distances.png",
    yscale='log'
)
