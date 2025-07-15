from src.baseline_algorithms.subroutines import make_cluster_tree, make_cluster_var


def upgma_algorithm(sample_vector):
    clusters = [(d,) for d in sample_vector]
    dists = {(a, b):abs(a[0]-b[0]) for a in clusters for b in clusters}
    while len(clusters) > 1:
        mv, indi, indj = min((dists[clusters[a], clusters[b]], a, b) 
            for a in range(len(clusters)) 
                for b in range(len(clusters)) if a != b)

        ci = clusters[indi]
        cj = clusters[indj]

        nc = (ci,cj)
        for a in clusters:
            nd = (dists[(ci, a)]+dists[(cj, a)])/2
            dists[(nc, a)] = nd 
            dists[(a, nc)] = nd 
        dists[(nc, nc)] = 0

        clusters.remove(ci)
        clusters.remove(cj)
        clusters.append(nc) 
    upgma_tree = make_cluster_tree(clusters[0])
    vars = [0]+make_cluster_var(clusters[0], dists)
    #upgma_tree.set_var([v for v in vars])
    upgma_tree.set_var(vars)
    return upgma_tree