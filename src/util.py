import numpy as np

'''Utility functions for the command line scripts'''
def pow_of_2(c):
    if c == 2:
        return True
    if c < 2:
        return False
    return c % 2 == 0 and pow_of_2(c//2)


def max_var(data):
    new_l = list(data) + [0]
    print('newl', new_l)
    return 3*(max(abs(a-b)**2 for a in new_l for b in new_l)**2)

def lin(m):
    return [b for a in m for b in a]

def fr_norm_sq(one, two):
    return sum((a-b)**2 for a, b in zip(lin(one), lin(two)))
    
def fr_norm_sq_one(one):
    return sum((a)**2 for a in lin(one))

def operator_norm(arr):
    return np.linalg.norm(np.array(arr), 2)

def is_data_invalid(data):
    return any(abs(a-b) < .005 for i, a in enumerate(data) for b in data[i+1:]) or any(abs(a) < .005 for a in data)



def gen_cmds(vs, ad):
    if len(vs) == 0:
        return [ad]
    k, vals = vs[0]
    ret = []
    for v in vals:
        ret.extend(gen_cmds(vs[1:], ad+['--'+k, str(v)]))
    return ret