import yaml
from dotwiz import DotWiz


def load_yaml(filepath: str) -> dict:
    """
    Load a yaml file and return a DotWiz dictionary. More info on DotWiz can be found at https://github.com/rnag/dotwiz.

    Parameters:
    ----------
    filepath: str
        The path to the yaml file to load.

    Returns:
    -------
    DotWiz
        A DotWiz dictionary containing the yaml file data.
    """
    return convert_to_dotwiz(yaml.load(open(filepath, 'r'), Loader=yaml.FullLoader))

def convert_to_dotwiz(data: dict) -> DotWiz:
    """
    Convert a dictionary to a DotWiz dictionary. More info on DotWiz can be found at https://github.com/rnag/dotwiz.

    Parameters:
    ----------
    data: dict
        The dictionary to convert to a DotWiz dictionary.

    Returns:
    -------
    DotWiz
        A DotWiz dictionary containing the data from the input dictionary.
    """
    if not isinstance(data, dict):
        try:
            data = data.__dict__
        except:
            raise ValueError("Input data must be a dictionary or an object with a __dict__ attribute.")
    return DotWiz(**data)