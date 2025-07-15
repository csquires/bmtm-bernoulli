from src.tree import Tree


def fat_tree_structures(levels):
    trees = [[0, 0]]
    for i in range(levels):
        half = [len(trees[-1])] + trees[-1]
        trees.append(half + half)
    return trees


def long_tree_structures(max_nodes):
    if max_nodes == 0:
        return [[]]
    if max_nodes == 1:
        return [[0]]
    trees = [[0, 0]]
    for i in range(max_nodes-2):
        trees.append([0, (i*2)+2] + trees[-1])
    return trees


def long_tree_with_root(max_nodes):
    start = long_tree_structures(max_nodes)[-1]
    if max_nodes > 1:
        return [len(start)] + start
    return start


def make_cluster_var(cl, dists):
    if type(cl[0]) != tuple:
        return []

    vars = []
    for c in cl: 
        vars.append(dists[(c, cl)])
        vars.extend(make_cluster_var(c, dists))
    return vars


def make_cluster_tree(cl):
    if type(cl[0]) != tuple:
        t = Tree()
        t.data = cl[0]
        return t

    t = Tree()
    for c in cl: 
        t.children.append(make_cluster_tree(c))
        t.children[-1].parent = t
    return t