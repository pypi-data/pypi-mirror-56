"""
Utility functions for working with files.
"""
import os
from hockeyjockey.models import HJTeam, HJMatchup, HJTeamStats
import hockeyjockey.config as cfg



def get_hj_dir() -> str:
    """
    Creates and returns a path to the hockeyjockey directory. If creation fails, alerts the user and returns None.

    :return: A directory path (str) to the hockeyjockey directory if directory creation was successful, else None.
    """
    print('Setting up hockeyjockey directory...', end='')
    try:
        hj_dir = os.path.join(os.path.expanduser(cfg.file.data_dir_loc), cfg.file.data_dir_name)
        print('Done.')
        return hj_dir
    except OSError:
        print('\nCould not create the hockeyjockey directory.  Downloaded data will not be cached locally.')
        return None


def get_hj_file_path(hj_dir: os.path, filename: str) -> str:
    """
    Takes the filename parameter and sets up a path to that file in the hockeyjockey directory.  Does nothing if the
     file already exists.  Alerts the user and returns None if an error is encountered.

    :param hj_dir: The hockeyjockey data storage directory.
    :param filename: A filename for the path to be created.
    :return: The file path (str) to the file that was created, or None if creation failed.
    """
    print(f'Setting up {filename} file path...', end='')
    try:
        os.path.isdir(hj_dir) or os.mkdir(hj_dir)
        path = os.path.join(hj_dir, filename)
        print('Done.')
        return path
    except OSError:
        print('\nError creating {0} file.'.format(filename))
        return None


def deserialize(filepath: str) -> object:
    """
    Deserializes a flat file that was populated with repr(obj), i.e transforms it back into its object-oriented
    representation. If deserialization fails, warns the user and returns None.

    :param filepath: File path string of the file to be deserialized.
    :return: The deserialized python object if the process was successful, else None.
    """
    with open(filepath, 'r') as fh:
        ser_str = fh.read()
    try:
        de_ser_obj = eval(ser_str)
        print('Done.')
        return de_ser_obj
    except SyntaxError:
        print('An error occurred loading file from disk.  Downloading instead...')
        return None
