from src.tree import Tree
from src.tree_structures import long_tree_with_root


def ddgm_mle_algorithm(sample_vector):
    pos = sorted([d for d in sample_vector + [0] if d >= 0])
    neg = list(reversed(sorted([d for d in sample_vector + [0] if d <= 0])))
    pos_diff = [(pos[i]-pos[i+1])**2 for i in range(len(pos)-1)]
    neg_diff = [(neg[i]-neg[i+1])**2 for i in range(len(neg)-1)]


    tree = Tree()
    structure = long_tree_with_root(len(neg)-1) + long_tree_with_root(len(pos) - 1)
    tree.make_prefix(structure)
    fmt_data = [p for p in neg if p != 0]+[p for p in pos if p != 0]
    tree.set_data(fmt_data)
    def intersperse(diff):
        if len(diff) == 0:
            return []
        return list(map(float, (',0,'.join(map(str, diff))).split(',')))
    var = [0]+intersperse(neg_diff) + intersperse(pos_diff)
    tree.set_var(var)

    return tree