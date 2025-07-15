from experiment_utils.data_generation.generation_manager import GenerationManager
from experiment_utils.config_manager import ConfigManager
from experiment_utils.algorithm_runner import AlgorithmRunner


config = ConfigManager('experiments/experiment_1.yaml')
generation_manager = GenerationManager(config)

nleaves_list = config.get_sampling_config().get('nleaves_list')
estimators = config.get_reconstruction_config().get('estimators')
for nleaves in nleaves_list:
    dataset = generation_manager.load_data_single_size(nleaves)
    for estimator in estimators:
        algorithm_runner = AlgorithmRunner(config, estimator)
        print(f"Running {estimator} on {nleaves} leaves")
        guesses = algorithm_runner.run_and_save(dataset, base_filename=f'{estimator}_{nleaves}_covariance')









