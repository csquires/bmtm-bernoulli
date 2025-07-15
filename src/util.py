import numpy as np
import subprocess

from src.tree import Tree


def operator_norm(arr):
    return np.linalg.norm(np.array(arr), 2)


def bhv_distance_owens(t1: Tree, t2: Tree, fh='tmpbhv.txt'):
    data = t1.get_data()
    t2.set_data(data)
    input = t1.newick() + '\n' + t2.newick()
    with open(fh, 'w') as f:
        f.write(input)
    cmd = 'java -jar jj.jar -o /dev/stdout {}'.format(fh)
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    comps = output.decode().strip().split()
    # print(comps)

    return float(comps[-1])


def bhv_distance_owens_list(trees1, trees2, fh='tmpbhv.txt'):
    for tree1, tree2 in zip(trees1, trees2):
        tree2.set_data(tree1.get_data())
    
    trees1_newick = [tree.newick() for tree in trees1]
    trees2_newick = [tree.newick() for tree in trees2]
    inputs = [t1_newick + '\n' + t2_newick for t1_newick, t2_newick in zip(trees1_newick, trees2_newick)]
    input = '\n'.join(inputs)
    with open(fh, 'w') as f:
        f.write(input)
    cmd = 'java -jar jj.jar -o /dev/stdout {}'.format(fh)
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    comps = [line.strip().split() for line in output.decode().strip().split('\n')]

    # TODO: remove temporary files
    return [float(c[-1]) for c in comps]