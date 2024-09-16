import os
import shutil


def mkdir(paths: str | list, hard: bool = False):
    """
    Create a directory at the given path.

    Parameters
    ----------
    paths : str or list
        The path(s) of the directory to create.
    hard : bool, optional
        If True, delete the directory if it already exists.
    """
    assert isinstance(paths, (str, list)), "paths must be a string or a list of strings."
    assert isinstance(hard, bool), "hard must be a boolean."

    if isinstance(paths, str):
        paths = [paths]

    for path in paths:
        if hard:
            # Create a directory
            shutil.rmtree(path, ignore_errors=True)
        os.makedirs(path, exist_ok=True)
