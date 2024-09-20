import os
import shutil
import errno

def cp_r(src, dst):
    """
    Recursively copy a file or directory from src to dst
    Stolen from https://stackoverflow.com/questions/1994488/copy-file-or-directories-recursively-in-python

    Parameters
    ----------
    src : str
        Source path
    dst : str
        Destination path

    Returns
    -------
    None
    """
    try:
        shutil.copytree(src, dst)
    except OSError as exc:  # python >2.5
        if exc.errno in (errno.ENOTDIR, errno.EINVAL):
            shutil.copy(src, dst)
        else:
            raise

def symlink(src, dst):
    """
    Create a symbolic link from src to dst
    If dst exists, remove it first
    Stolen from https://stackoverflow.com/questions/49182755/how-do-i-link-directories-in-python-linux-cmd-ln-s-equivalent

    Parameters
    ----------
    src : str
        Source path
    dst : str
        Destination path

    Returns
    -------
    None
    """
    os.symlink(os.path.abspath(src), os.path.abspath(dst), target_is_directory=os.path.isdir(src))
