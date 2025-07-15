from experiment_utils.data_generation.generation_manager import GenerationManager
from experiment_utils.config_manager import ConfigManager


config = ConfigManager('experiments/experiment_1.yaml')
generation_manager = GenerationManager(config)
generation_manager.generate_and_save()
dataset = generation_manager.load_data_single_size(8)
