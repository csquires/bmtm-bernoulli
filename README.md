
## Replicating experiments
To replicate the experiments, run the following four files:
1. `python3 experiments/step1_generate_data.py`
2. `python3 experiments/step2_run_algorithms.py`
3. `python3 experiments/step3_compute_metrics.py`
4. `python3 experiments/step4_plot_metrics.py`
The results will be in `experiments/figures/`.


## Overview of file structure
- `src/` contains an implementation of all algorithms and the data structure used for trees.
- `experiment_utils/` contains classes to manage each step of the experiments.
- `experiments/` contains scripts to run the experiments (see **Replicating Experiments** above)


## Algorithms
In `src/`, we provide an implementation of our algorithm, shrinkage methods, and baselines.
- `baseline_algorithms`
    - `ddgm_mle.py`
    - `least_squares.py`
    - `neighbor_joining.py`: The Neighbor Joining algorithm
    - `subroutines.py`
    - `upgma.py`: The UPGMA algorithm
- `bmtm_mle_algorithm`
    - `solver.py`
- `shrinkage`
    - `ledoitwolfvalidshrink.py`
    - `mxshrink.py`
