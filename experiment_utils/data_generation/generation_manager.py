import pickle
from tqdm import tqdm
import random
from pathlib import Path

import numpy as np

from experiment_utils.config_manager import ConfigManager
from experiment_utils.data_generation.generators_structures import RandomStructureGenerator
from experiment_utils.data_generation.generators_parameters import RandomParameterGenerator


class GenerationManager:
    def __init__(self, config: ConfigManager):
        """
        Initialize the sampler with configuration.
        
        Args:
            config: Configuration manager instance
        """
        self.config = config
        self.sampling_config = config.get_sampling_config()
        self.tree_config = config.get_tree_config()
        self.paths_config = config.get_paths_config()

    def _generate_single_size(self, nleaves: int):
        """
        Generate data for a given number of trials
        """
        num_trials = self.sampling_config.get('num_trials')
        print(f"Generating {num_trials} trees with {nleaves} leaves")

        # === STRUCTURES ===
        structure_generator = RandomStructureGenerator()
        print(f"Generating structures...")
        structures = [structure_generator.generate_structure(nleaves) for _ in range(num_trials)]

        # === PARAMETERS ===
        parameter_generator = RandomParameterGenerator()
        ground_truths = []
        print(f"Generating parameters...")
        for structure in tqdm(structures):
            tree_with_params = parameter_generator.generate_parameters(structure)
            ground_truths.append(tree_with_params)

        # === SAMPLES ===
        print(f"Generating data...")
        num_replicates = self.sampling_config.get('num_replicates')
        samples = [[tree.sample_data() for _ in range(num_replicates)] for tree in ground_truths]

        return ground_truths, samples, structures
    
    def _generate_and_save_single_size(self, nleaves: int):
        """
        Generate data and save to pickle file
        """
        ground_truths, samples, structures = self._generate_single_size(nleaves)
        dataset = dict(structures=structures, ground_truths=ground_truths, samples=samples)
        dataset["config"] = dict(sampling=self.sampling_config, tree=self.tree_config, paths=self.paths_config)
        
        data_dir = Path(self.paths_config.get('data_dir'))
        output_filename = f"nleaves_{nleaves}.pkl"
        output_file = data_dir / output_filename
        print(f"Saving data to {output_file}")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        pickle.dump(dataset, open(output_file, "wb"))

    def generate_and_save(self):
        seed = self.sampling_config.get('seed')
        random.seed(seed)
        np.random.seed(seed)
        nleaves_list = self.sampling_config.get('nleaves_list')
        for nleaves in nleaves_list:
            self._generate_and_save_single_size(nleaves)

    def load_data_single_size(self, nleaves: int):
        data_dir = Path(self.paths_config.get('data_dir'))
        data_file = data_dir / f"nleaves_{nleaves}.pkl"
        dataset = pickle.load(open(data_file, "rb"))
        return dataset