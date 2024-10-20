from collections.abc import Iterable

def flatten_list(lst: Iterable) -> Iterable:
    """
    Flatten an arbitrarily nested Python list of elements. Places no assumptions on the type of the list other than it
    is an iterable, but all iterables in this list must be of the same type then.

    e.g. if `type(lst) == list`, then all elements in lst must be lists as well.

    Adapted from stolen code on the internet.

    Parameters
    ----------
    lst : list
        A nested list of elements. The tree structure of the list can be arbitrarily complex.

    Returns
    -------
    list
        A flattened list of elements.
    """
    if not isinstance(lst, Iterable):
        return [lst]

    result = []
    for item in lst:
        result.extend(flatten_list(item))
    return result
