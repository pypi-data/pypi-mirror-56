"""Define data utilities."""
import operator as op
from functools import reduce


def paths_in_data(data: dict, parent=()):
    """Calculate keys and/or indices in dict."""

    if not any(isinstance(data, type_) for type_ in (dict, list, tuple)):
        return (parent,)
    else:
        try:
            return reduce(
                op.add,
                (paths_in_data(v, op.add(parent, (k,))) for k, v in data.items()),
                (),
            )
        except AttributeError:
            return reduce(
                op.add,
                (paths_in_data(v, op.add(parent, (data.index(v),))) for v in data),
                (),
            )


def get_from(data, path):
    """Get a leaf from iterable of keys and/or indices.

    :data: Collection where nodes are either a dict or list.
    :path: Collection of keys and/or indices leading to a leaf.
    """
    return reduce(op.getitem, path, data)
