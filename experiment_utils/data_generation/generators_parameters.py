import random

from src.tree import Tree
from src.util import operator_norm




class RandomParameterGenerator:
    def __init__(self):
        pass
    
    def generate_parameters(self, tree: Tree):
        tree = self._create_exponential_ultrametric_tree(tree)
        tree = self._normalize_tree(tree)
        return tree

    def _create_exponential_ultrametric_tree(self, tree: Tree) -> Tree:
        p = 0.01
        num = tree.num_leaf_nodes()
        nt = Tree()
        nt.above_var = 0.1
        
        while nt.num_leaf_nodes() < num:
            leaves = [nt.get_leaf(i) for i in range(nt.num_leaf_nodes()) if random.uniform(0, 1) < p]
            random.shuffle(leaves)
            
            for leaf in leaves:
                leaf.make_child()
                leaf.make_child()
                if nt.num_leaf_nodes() >= num:
                    break
            
            for i in range(nt.num_leaf_nodes()):
                leaf = nt.get_leaf(i)
                leaf.above_var += 0.01
        
        return nt
    
    def _normalize_tree(self, tree: Tree) -> Tree:
        """Normalize tree variance values."""
        coef = operator_norm(tree.cov_matrix())
        tree.set_var([a / coef for a in tree.get_var()])
        # fo_seed = [random.randrange(0, 20) for _ in range(tree.num())]
        # tree.random_fo(fo_seed)
        assert(abs(operator_norm(tree.cov_matrix()) - 1) < 1e-6)
        return tree