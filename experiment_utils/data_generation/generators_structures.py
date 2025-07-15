import math

from src.tree import Tree
from src.tree_structures import fat_tree_structures


class RandomStructureGenerator:
    def __init__(self):
        pass
    
    def generate_structure(self, num_leaves):
        sqr = int(math.log(num_leaves)/math.log(2))
        tree_prefix = fat_tree_structures(sqr - 1)[-1]

        tree = Tree()
        tree.make_prefix(tree_prefix)
        assert(tree.num_leaf_nodes() == num_leaves)

        return tree