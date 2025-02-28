from typing import Any

import yaml

from dotwiz import DotWiz


def load_yaml(filepath: str, **kwargs: Any) -> DotWiz:
    """
    Load a yaml file and return a DotWiz dictionary. More info on DotWiz can be found at https://github.com/rnag/dotwiz.

    Parameters:
    ----------
    filepath: str
        The path to the yaml file to load.
    kwargs: Any
        Any additional keyword arguments to pass to the DotWiz dictionary.

    Returns:
    -------
    DotWiz
        A DotWiz dictionary containing the yaml file data.
    """
    return convert_to_dotwiz(yaml.load(open(filepath, 'r'), Loader=yaml.FullLoader), **kwargs)


def convert_to_dotwiz(data: dict | Any, **kwargs: Any) -> DotWiz:
    """
    Convert a dictionary to a DotWiz dictionary. More info on DotWiz can be found at https://github.com/rnag/dotwiz.

    Parameters:
    ----------
    data: dict | Any
        The dictionary to convert to a DotWiz dictionary. Add Any typing in case it's something like a dataclass
        (but needs __dict__ property implemented).
    kwargs: Any
        Any additional keyword arguments to pass to the DotWiz dictionary.

    Returns:
    -------
    DotWiz
        A DotWiz dictionary containing the data from the input dictionary.
    """
    if not isinstance(data, dict):
        try:
            data = data.__dict__
        except:
            return data

    # Do this recursively in case it's a nested object
    return_dict = {}
    for key, value in data.items():
        return_dict[key] = convert_to_dotwiz(value)
    return DotWiz(**dict(return_dict, **kwargs))
