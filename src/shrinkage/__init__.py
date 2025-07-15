from .mxshrink import mxshrink
from .ledoitwolfvalidshrink import ledoitwolfvalidshrink


def fo_shrink(original_tree):
    original_tree.set_var([(1/3)*a if a != 0 else a for a in original_tree.get_var()])
    return original_tree