from experiment_utils.data_generation.generation_manager import GenerationManager
from experiment_utils.config_manager import ConfigManager
from experiment_utils.algorithm_runner import AlgorithmRunner
from experiment_utils.metrics_manager import MetricsManager

config = ConfigManager('experiments/experiment_1.yaml')
generation_manager = GenerationManager(config)

nleaves_list = config.get_sampling_config().get('nleaves_list')
estimators = config.get_reconstruction_config().get('estimators')

results_dict = dict()
datasets_dict = dict()
for nleaves in nleaves_list:
    dataset = generation_manager.load_data_single_size(nleaves)
    datasets_dict[nleaves] = dataset
    for estimator in estimators:
        algorithm_runner = AlgorithmRunner(config, estimator)
        print(f"Loading {estimator} on {nleaves} leaves")
        results = algorithm_runner.load_results(base_filename=f'{estimator}_{nleaves}_covariance')
        results_dict[(estimator, nleaves)] = results

metrics_manager = MetricsManager(config)
metrics_manager.compute_and_save_metrics(results_dict, datasets_dict)











