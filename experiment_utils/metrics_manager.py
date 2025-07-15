import pickle

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

    def load_metrics(self):
        filename = self.config.get_paths_config().get('metrics_file')
        metrics_dict = pickle.load(open(filename, 'rb'))
        return metrics_dict

    def _compute_frob_errors(self, estimated_covs, ground_truth_covs):
        errors = []
        for i in range(len(estimated_covs)):
            diff = estimated_covs[i] - ground_truth_covs[i]
            errors.append(np.sum(diff**2))
        return errors
    
    def _compute_bhv_distances(self, estimated_trees, ground_truths):
        distances = bhv_distance_owens_list(estimated_trees, ground_truths)
        # distances = []
        # for i in trange(len(estimated_trees)):
            # bhv_distance = bhv_distance_owens(estimated_trees[i], ground_truths[i])
            # distances.append(bhv_distance)
        return distances
    
    def _compute_frob_biases(self, estimated_covs, ground_truth_covs):
        mean_estimated_cov = np.mean(estimated_covs, axis=0)
        biases = np.array([
            fr_norm_squared(mean_estimated_cov - true_cov) for true_cov in ground_truth_covs
        ])
        return biases

    def _compute_frob_variances(self, estimated_covs, ground_truth_covs):
        mean_estimated_cov = np.mean(estimated_covs, axis=0)
        variances = np.array([
            fr_norm_squared(estimated_cov - mean_estimated_cov) for estimated_cov in estimated_covs
        ])
        return variances