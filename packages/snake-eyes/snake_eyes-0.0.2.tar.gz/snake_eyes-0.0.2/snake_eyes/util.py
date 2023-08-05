import numpy as np

try:
    from math import prod
except ImportError:
    from functools import reduce
    import operator as op


    def prod(x):
        """
        implementation of math.prod for python < 3.8
        """
        return reduce(op.mul, x)


def min_max_prod(minimums, maximums):
    """
    returns the smallest and largest products achievable by interweaving maximums and minimums

    >>> min_max_prod((3,6,0,1,6),(-4,3,-5,-4,0))
    (-2880, 2160)
    """
    assert len(maximums) == len(minimums)

    ret_min, ret_max = 1, 1
    for op_min, op_max in zip(minimums, maximums):
        cands = (op_min * ret_min, op_min * ret_max, op_max * ret_min, op_max * ret_max)
        ret_min = min(cands)
        ret_max = max(cands)
    return ret_min, ret_max


def _maybe_parenthesise(x, convert=str):
    """
    convert an object to string and surround in parenthesis if it contains an operator
    """
    warrenters = '+*/\\-^'
    ret = convert(x)
    if any((w in ret) for w in warrenters):
        return "(" + ret + ")"
    return ret


def common_dtype(*args):
    """
    Get the common dtype for numpy arrays, or object if none found
    """
    try:
        return np.result_type(*args)
    except TypeError:
        return object
