'''
Reconstruct covariance matrix given samples
'''
import os
import pickle

from tqdm import trange
import numpy as np

from src.bmtm_mle_algorithm import our_mle
from src.baseline_algorithms import neighbor_joining_algorithm, upgma_algorithm, least_squares_algorithm, ddgm_mle_algorithm
from src.shrinkage import mxshrink, ledoitwolfvalidshrink, fo_shrink
from experiment_utils.config_manager import ConfigManager




class AlgorithmRunner:
    def __init__(self, config: ConfigManager, estimator):
        self.config = config
        self.estimator = estimator

    def _run(self, dataset):
        ground_truths = dataset["ground_truths"]
        samples = dataset["samples"]
        structures = dataset["structures"]
        num_trials = len(ground_truths)

        guesses = []
        estimated_trees = []
        estimated_covs = []
        for i in trange(num_trials):
            tree_structure = structures[i]
            sample_vector = samples[i]
            ground_truth_tree = ground_truths[i]

            est_cov = None
            if self.estimator == 'gt':
                guesses.append(ground_truths[-1])
            # === OUR ALGORITHM (AND SHRINKAGE VARIANTS) ===
            elif self.estimator == 'bmtm-mle':
                est_tree = our_mle(sample_vector, tree_structure)
            elif self.estimator == 'one-third-shrink':
                original_est_tree = our_mle(sample_vector, tree_structure)
                est_tree = fo_shrink(original_est_tree)
            elif self.estimator == 'mxshrink':
                original_est_tree = our_mle(sample_vector, tree_structure)
                original_est_cov = np.array(original_est_tree.cov_matrix())
                est_cov = mxshrink(original_est_cov)
                est_tree = None
            elif self.estimator == 'linear-shrink':
                original_est_tree = our_mle(sample_vector, tree_structure)
                est_tree = ledoitwolfvalidshrink(original_est_tree, ground_truth_tree)
            # === BASELINE ALGORITHMS (NO TREE STRUCTURE) ===
            elif self.estimator == 'upgma':
                est_tree = upgma_algorithm(sample_vector)
            elif self.estimator == 'neighbor-joining':
                est_tree = neighbor_joining_algorithm(sample_vector)
            elif self.estimator == 'ddgm-mle':  # DDGM MLE
                est_tree = ddgm_mle_algorithm(sample_vector)
            # === BASELINE ALGORITHMS (WITH TREE STRUCTURE) ===
            elif self.estimator == 'least-squares':
                est_tree = least_squares_algorithm(sample_vector, tree_structure)
            
            else:
                print(self.estimator)
                raise ValueError('No match in estimator!')
            
            if est_cov is None:
                est_cov = np.array(est_tree.cov_matrix())
            estimated_trees.append(est_tree)
            estimated_covs.append(est_cov)
            
        return estimated_trees, estimated_covs
    
    def run_and_save(self, dataset, base_filename):
        estimated_trees, estimated_covs = self._run(dataset)
        results = dict(estimated_trees=estimated_trees, estimated_covs=estimated_covs)
        
        # === CREATE OUTFILE NAME ===
        outdir = self.config.get_paths_config().get('output_dir')
        outfilename = f'/{base_filename}.pkl'
        outfile = outdir + outfilename

        # === SAVE RESULTS ===
        os.makedirs(outdir, exist_ok=True)
        with open(outfile, 'wb') as f:
            pickle.dump(results, f)

    def load_results(self, base_filename):
        outdir = self.config.get_paths_config().get('output_dir')
        outfilename = f'/{base_filename}.pkl'
        outfile = outdir + outfilename
        results = pickle.load(open(outfile, 'rb'))
        return results
