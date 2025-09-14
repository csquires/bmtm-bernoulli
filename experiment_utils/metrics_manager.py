import pickle

from copy import deepcopy
import numpy as np
from tqdm import tqdm

from experiment_utils.config_manager import ConfigManager
from src.util import bhv_distance_owens_list, fr_norm_squared


class MetricsManager:
    def __init__(self, config: ConfigManager):
        self.config = config

    def _compute_metrics(self, results_dict, datasets_dict):
        nleaves_list = self.config.get_sampling_config().get('nleaves_list')
        estimators = self.config.get_reconstruction_config().get('estimators')

        frob_errors_dict = dict()
        bhv_distances_dict = dict()
        frob_biases_dict = dict()
        frob_variances_dict = dict()
        for nleaves in nleaves_list:
            dataset = datasets_dict[nleaves]
            ground_truths = dataset['ground_truths']
            ground_truth_covs = [np.array(t.cov_matrix()) for t in ground_truths]

            print(f"Computing metrics for {nleaves} leaves")
            for estimator in tqdm(estimators):
                results = results_dict[(estimator, nleaves)]
                estimated_trees = results['estimated_trees']
                estimated_covs = results['estimated_covs']
                
                frob_errors = self._compute_frob_errors(estimated_covs, ground_truth_covs)
                frob_errors_dict[(estimator, nleaves)] = frob_errors

                frob_biases = self._compute_frob_biases(estimated_covs, ground_truth_covs)
                frob_biases_dict[(estimator, nleaves)] = frob_biases

                frob_variances = self._compute_frob_variances(estimated_covs, ground_truth_covs)
                frob_variances_dict[(estimator, nleaves)] = frob_variances

                if estimator != "mxshrink":
                    bhv_distances = self._compute_bhv_distances(estimated_trees, ground_truths)
                    bhv_distances_dict[(estimator, nleaves)] = bhv_distances
            
        metrics_dict = dict(
            frob_errors_dict=frob_errors_dict,
            bhv_distances_dict=bhv_distances_dict,
            frob_biases_dict=frob_biases_dict,
            frob_variances_dict=frob_variances_dict
        )
        return metrics_dict
    
    def compute_and_save_metrics(self, results_dict, datasets_dict):
        metrics_dict = self._compute_metrics(results_dict, datasets_dict)
        filename = self.config.get_paths_config().get('metrics_file')
        pickle.dump(metrics_dict, open(filename, 'wb'))
        return metrics_dict

    def load_metrics(self):
        filename = self.config.get_paths_config().get('metrics_file')
        metrics_dict = pickle.load(open(filename, 'rb'))
        return metrics_dict

    def _compute_frob_errors(self, estimated_covs, ground_truth_covs):
        num_trials = len(estimated_covs)
        num_replicates = len(estimated_covs[0])
        errors = np.zeros(num_trials)
        for i in range(num_trials):
            diffs = [(estimated_covs[i][j] - ground_truth_covs[i]) for j in range(num_replicates)]
            errors_replicates = [fr_norm_squared(diff) for diff in diffs]
            errors[i] = np.mean(errors_replicates)
        return errors
    
    def _compute_bhv_distances(self, estimated_trees, ground_truths):
        num_trials = len(estimated_trees)
        num_replicates = len(estimated_trees[0])

        # calculate on flattened versions
        ground_truths_replicated = []
        for ground_truth in ground_truths:
            for _ in range(num_replicates):
                ground_truths_replicated.append(deepcopy(ground_truth))
        estimated_trees_flat = []
        for estimated_tree_trial in estimated_trees:
            for estimated_tree in estimated_tree_trial:
                estimated_trees_flat.append(estimated_tree)
        distances_flat = bhv_distance_owens_list(estimated_trees_flat, ground_truths_replicated)

        # unflatten
        distances = np.zeros(num_trials)
        for i in range(num_trials):
            distances_replicates = [distances_flat[i*num_replicates+j] for j in range(num_replicates)]
            distances[i] = np.mean(distances_replicates)
        return distances
    
    def _compute_frob_biases(self, estimated_covs, ground_truth_covs):
        num_trials = len(estimated_covs)
        num_replicates = len(estimated_covs[0])
        biases = np.zeros(num_trials)
        for i in range(num_trials):
            mean_estimated_cov = np.mean(estimated_covs[i], axis=0)
            biases[i] = fr_norm_squared(mean_estimated_cov - ground_truth_covs[i])
        return biases

    def _compute_frob_variances(self, estimated_covs, ground_truth_covs):
        num_trials = len(estimated_covs)
        num_replicates = len(estimated_covs[0])
        variances = np.zeros(num_trials)
        for i in range(num_trials):
            mean_estimated_cov = np.mean(estimated_covs[i], axis=0)
            diffs_from_mean = [estimated_covs[i][j] - mean_estimated_cov for j in range(num_replicates)]
            fr_norm_squareds = [fr_norm_squared(diff) for diff in diffs_from_mean]
            variances[i] = np.mean(fr_norm_squareds)
        return variances