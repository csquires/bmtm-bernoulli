import random
import math

from src.tree import Tree
from src.tree_structures import fat_tree_structures

class RandomStructureGenerator:
    def __init__(self):
        pass
    
    # def generate_structure(self, num_leaves):
    #     tree = Tree()
    #     tree.make_prefix([0, 0])
    #     while tree.num_leaf_nodes() < num_leaves:
    #         pi = random.randrange(tree.num_leaf_nodes())
    #         leaf = tree.get_leaf(pi)
    #         leaf.make_child()
    #         leaf.make_child()

    #     return tree
    
    def generate_structure(self, num_leaves):
        # tree = Tree()
        # tree.make_prefix([0, 0])
        # node_ix = 0
        # while tree.num_leaf_nodes() < num_leaves:
        #     node = tree.get_leaf(node_ix)
        #     node.make_child()
        #     node.make_child()
        #     node_ix += 1
        # assert(tree.num_leaf_nodes() == num_leaves)

        sqr = int(math.log(num_leaves)/math.log(2))
        tree_prefix = fat_tree_structures(sqr - 1)[-1]

        tree = Tree()
        tree.make_prefix(tree_prefix)
        assert(tree.num_leaf_nodes() == num_leaves)

        return tree