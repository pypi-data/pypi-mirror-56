"""Define data utilities."""
import itertools as it
import operator as op
from functools import reduce


def paths_from(d, paths=(), acc=None):
    """Generate paths from nested dict :d:."""
    containers = (dict, list, tuple)
    non_dicts = containers[1:]

    acc = list() if acc is None else acc
    stack = list(d.items())
    visited = set()
    while stack:
        k, v = stack.pop()
        paths = (*paths, (k,))
        acc.append(tuple(it.chain.from_iterable(paths)))
        if not any(isinstance(v, type_) for type_ in containers):  # leaf
            paths = paths[:-1]  # slice off all except last for non-container leaf
        elif isinstance(v, dict):  # dict node
            if k not in visited:
                stack.extend(v.items())
        elif any(isinstance(v, type_) for type_ in non_dicts):  # list node
            for i in range(len(v)):
                paths = (*paths[:-1], (k, i))
                paths_from(v[i], paths, acc)
            paths = paths[:-1]  # slice off all except last for new array item

        visited.add(k)
    return acc


def get_from(data, path):
    """Get a leaf from iterable of keys and/or indices.

    :data: Collection where nodes are either a dict or list.
    :path: Collection of keys and/or indices leading to a leaf.
    """
    return reduce(op.getitem, path, data)
