from src.tree import Tree


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