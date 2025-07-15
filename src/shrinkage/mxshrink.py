import numpy as np

def mxshrink(mle):
    values, vectors = np.linalg.eig(mle)
    other = vectors @ np.diag(values) @ np.transpose(vectors)
    assert(np.allclose(mle, other))
    
    p = mle.shape[0]
    n = (1 if p % 2 == 1 else 1.5)
    #print(n, p, len(data))
    newdiag = np.diag([(n/(n+p+1-2*i))*values[i] for i in range(len(values))])
    #print('values', values, newdiag)
    #newdiag = np.diag([(n/(n+p+1-2*i))*values[i] for i in range(len(values))])
    return [[float(a) for a in b] for b in vectors @ newdiag @ np.transpose(vectors)]