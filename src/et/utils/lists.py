from collections.abc import Iterable
from copy import deepcopy
from treelib import Tree, Node


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

def print_tree(lst):
    """
    Pretty print an arbitrarily nested list as a tree structure.

    Parameters
    ----------
    lst : list
        A nested list of elements. The tree structure of the list can be arbitrarily complex.
    """
    def _recurse(node, lst):
        for child in lst:
            if isinstance(child, Iterable):
                child_node = tree.create_node(f"L{node.data + 1}", data=node.data + 1, parent=node)
                _recurse(child_node, child)
            else:
                tree.create_node(str(child), data=node.data + 1, parent=node)

    tree, root = Tree(), Node(f"L{0}", data=0)  # data is the depth
    tree.add_node(root)
    _recurse(root, lst)
    print(tree.show(stdout=False))
