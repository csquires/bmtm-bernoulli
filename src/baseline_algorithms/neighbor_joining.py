from src.baseline_algorithms.subroutines import make_cluster_tree, make_cluster_var


def neighbor_joining_algorithm(sample_vector):
    clusters = [(d,) for d in sample_vector]
    dists = {(a, b):abs(a[0]-b[0]) for a in clusters for b in clusters}
    def ad(piv):
        return sum(dists[(piv, k)] for k in clusters)
    def n():
        return len(clusters) + 1
    while len(clusters) > 1:
        qdists = {(a, b):((n()-2)*dists[(a, b)]
            - ad(a) - ad(b))
        for a in clusters for b in clusters}
        mv, indi, indj = min((qdists[clusters[a], clusters[b]], a, b) 
            for a in range(len(clusters)) 
                for b in range(len(clusters)) if a != b)

        ci = clusters[indi]
        cj = clusters[indj]

        nc = (ci,cj)
        # check cluster len
        dists[(ci, nc)] = ((1/2)*dists[(ci, cj)] 
            + (1/(2*(n()-2)))*(ad(ci) - ad(cj)))
        dists[(cj, nc)] = dists[(ci, cj)] - dists[(ci, nc)]
        dists[(nc, ci)] = dists[(ci, nc)]
        dists[(nc, cj)] = dists[(cj, nc)]

        clusters.remove(ci)
        clusters.remove(cj)

        for a in clusters:
            nd = (dists[(ci, a)]+dists[(cj, a)] - dists[(ci, cj)])/2
            dists[(nc, a)] = nd 
            dists[(a, nc)] = nd 

        dists[(nc, nc)] = 0
        clusters.append(nc) 

    nj_tree = make_cluster_tree(clusters[0])
    vars = [0]+make_cluster_var(clusters[0], dists)
    nj_tree.set_var([v**2 for v in vars])
    #nj_tree.set_var(vars)
    return nj_tree