import cvxpy as cp
import numpy as np

from src.tree import Tree


def least_squares_algorithm(sample_vector, tree_structure: Tree):
    tree_structure.set_data(sample_vector)
    _, sample_cov, _ = tree_structure._build_matrices()
    sample_cov = np.array(sample_cov)

    # Problem data.
    p = tree_structure.num_leaf_nodes()
    np.random.seed(1)

    # Construct the problem.
    A = cp.Variable((p, p))
    objective = cp.Minimize(cp.sum_squares(A - sample_cov))
    constraints = [A[i][j] - A[j][i] == 0 for i in range(p) for j in range(i+1, p)]
    #constraints.extend([A[i][j] >= 0 for i in range(p) for j in range(i+1, p)])
    #constraints = [A >> 0]
    #constraints.append(A >> 0)
    constraints.append(A >= 0)

    eqfunnel = {}
    for i, a in enumerate(tree_structure.leaves()):
        for j, b in enumerate(tree_structure.leaves()):
            if j >= i:
                continue
            parent = a.lca(b)
            if parent.num_leaf_nodes() > 2:
                eqfunnel[parent] = (i, j)

    for i, a in enumerate(tree_structure.leaves()):
        for j, b in enumerate(tree_structure.leaves()):
            if j >= i:
                continue
            parent = a.lca(b)
            if parent in eqfunnel:
                k, l = eqfunnel[parent]
                if (k, l) != (i, j):
                    constraints.append(A[i][j] - A[k][l] == 0)

    for i, a in enumerate(tree_structure.leaves()):
        a.ind = i
    
    def m_ind(a):
        if len(a.children) == 0:
            return a.ind, a.ind
        else:
            return a.children[0].get_leaf(0).ind, a.children[1].get_leaf(0).ind
    for a in tree_structure.nodes():
        if a.parent is not None:
            ac1, ac2 = m_ind(a)
            pc1, pc2 = m_ind(parent)
            constraints.append(A[pc1][pc2] - A[ac1][ac2] <= 0)

    prob = cp.Problem(objective, constraints)

    # The optimal objective value is returned by `prob.solve()`.
    result = prob.solve()
    #print(constraints[0].dual_value)
    for a in tree_structure.nodes():
        ac1, ac2 = m_ind(a)
        a.tv = A.value[ac1][ac2]
    for a in tree_structure.nodes():
        a.above_var = a.tv - (a.parent.tv if a.parent is not None else 0)
    
    return tree_structure
