def fat_tree_structures(levels):
    trees = [[0, 0]]
    for i in range(levels):
        half = [len(trees[-1])] + trees[-1]
        trees.append(half + half)
    return trees

def stars(max_nodes):
    trees = []
    for i in range(2, max_nodes+1):
        trees.append([0]*i)
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


# def binary_tree(num_leaves):
#     assert(pow_of_2(num_leaves))
#     sqr = int(math.log(num_leaves)/math.log(2))
#     return fat_tree_structures(sqr - 1)