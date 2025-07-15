import pickle

import numpy as np
from tqdm import trange
from experiment_utils.config_manager import ConfigManager


class MetricsManager:
    def __init__(self, config: ConfigManager):
        self.config = config

    def _compute_metrics(self, results_dict, datasets_dict):
        nleaves_list = self.config.get_sampling_config().get('nleaves_list')
        estimators = self.config.get_reconstruction_config().get('estimators')

        frob_errors_dict = dict()
        for nleaves in nleaves_list:
            dataset = datasets_dict[nleaves]
            ground_truths = dataset['ground_truths']
            ground_truth_covs = [np.array(t.cov_matrix()) for t in ground_truths]

            for estimator in estimators:
                results = results_dict[(estimator, nleaves)]
                # estimated_trees = results['estimated_trees']
                estimated_covs = results['estimated_covs']
                
                print(f"Computing metrics for {estimator} on {nleaves} leaves")
                frob_errors = self._compute_frob_errors(estimated_covs, ground_truth_covs)
                frob_errors_dict[(estimator, nleaves)] = frob_errors
        
        metrics_dict = dict(
            frob_errors_dict=frob_errors_dict
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
        for i in trange(len(estimated_covs)):
            diff = estimated_covs[i] - ground_truth_covs[i]
            errors.append(np.sum(diff**2))
        return errors
    