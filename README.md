
## Replicating experiments
To replicate the experiments, run the following four files:
1. `python3 experiments/step1_generate_data.py`
2. `python3 experiments/step2_run_algorithms.py`
3. `python3 experiments/step3_compute_metrics.py`
4. `python3 experiments/step4_plot_metrics.py`

Step 1 creates synthetic data, which is saved in `experiments/data/`. Step 2 runs the estimators on this data and saves the results in `experiments/results/`. Step 3 computes the metrics reported in the paper, such as Frobenius error and BHV distance, and saves them in `experiments/metrics.pkl`. Step 4 handles plotting and saves the figures in `experiments/figures/`.


## Overview of file structure
- `src/` contains an implementation of all algorithms and the data structure used for trees.
- `experiment_utils/` contains classes to manage each step of the experiments.
- `experiments/` contains scripts to run the experiments (see **Replicating Experiments** above)


## Algorithms and data structure
In `src/`, we provide an implementation of our algorithm, shrinkage methods, and baselines.
- `baseline_algorithms`
    - `ddgm_mle.py`: Diagonally-dominant Gaussian model MLE
    - `least_squares.py`: Optimization-based algorithm to minimize Frobenius norm
    - `neighbor_joining.py`: The Neighbor Joining (NJ) algorithm
    - `upgma.py`: The UPGMA algorithm
- `bmtm_mle_algorithm`
    - `solver.py`: Dynamic programming algorithm introduced by the paper
- `shrinkage`
    - `ledoitwolfvalidshrink.py`
    - `mxshrink.py`
- `tree.py`: Data structure for BMTMs
- `tree_utils.py`: Utilities for building trees
- `util.py`: General utility functions


## Experiment utilities
- `data_generation/generation_manager.py`: Defines the `GenerationManager` class, which is responsible for creating synthetic data. Calls on `data_generation/generators_structures.py` to generate tree structures and `data_generation/generators_parameters.py` to generate BMTM parameters.
- `algorithm_runner.py`: Defines the `AlgorithmRunner` class, which is responsible for running the algorithms on the generated data and saving the results.
- `config_manager.py`: Defines the `ConfigManager` class, which is used throughout the experiments to keep track of all information.
- `metrics_manager.py`: Defines the `MetricsManager` class, which is responsible for computing the metrics that we plot.
- `plot_manager.py`: Defines the `PlotManager` class, which is responsible for plotting the results.