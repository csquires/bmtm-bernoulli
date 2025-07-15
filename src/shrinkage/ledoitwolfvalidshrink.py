import numpy as np

from src.bmtm_mle_algorithm import our_mle



def ledoitwolfvalidshrink(mle_tree, ground_truth_tree):
    mle_matrix = np.array(mle_tree.cov_matrix())
    #sample_cov_matrix = np.array(sample_cov(data))
    identity_matrix = np.identity(mle_matrix.shape[0])
    ground_truth_matrix = np.array(ground_truth_tree.cov_matrix())

    def diff(a, b):
        d = a - b
        return np.trace(np.matmul(d, np.transpose(d)))
    
    mu = np.trace(ground_truth_matrix)/mle_matrix.shape[0]
    a_sq = diff(ground_truth_matrix, mu*identity_matrix)
    b_sq = 0
    trials = 20
    for i in range(trials):
        b_sq += diff(ground_truth_matrix, mle_matrix)
    b_sq /= trials
    delta_sq = a_sq + b_sq
    
    #final_matrix = (b_sq/delta_sq)*mu*identity_matrix + (a_sq/delta_sq)*mle_matrix
    #guesses.append(list(final_matrix))
    #guesses.append(list((4/5)*mu*identity + (1/5)*mle))
    for l in mle_tree.nodes():
        l.above_var = (a_sq/delta_sq)*l.above_var
    for l in mle_tree.leaves():
        l.above_var += (b_sq/delta_sq)*mu
    return mle_tree