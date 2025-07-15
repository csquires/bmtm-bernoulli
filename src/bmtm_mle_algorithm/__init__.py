from src.bmtm_mle_algorithm.solver import Solver


def our_mle(sample_vector, tree_structure):
    solver = Solver()
    tree_structure.set_data(sample_vector)
    solver.predict_mle(tree_structure)

    return tree_structure