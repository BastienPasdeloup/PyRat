#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# Please import necessary elements using the following syntax:
#     from pyrat import <element_name>

"""
This module provides utility functions for the PyRat library.
It includes functions to create a workspace, get the caller file, get PyRat files, and check if a directory is valid.
Except for the ``create_workspace()`` function, which is meant to be called just at the beginning of a PyRat project, all other functions are mostly for internal use.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
from typing import *
import pyfakefs.fake_filesystem_unittest
from typing_extensions import *
from numbers import *
import os
import shutil
import inspect
import pathlib
import sys
import pyfakefs
import site

#####################################################################################################################################################
##################################################################### FUNCTIONS #####################################################################
#####################################################################################################################################################

def caller_file () -> pathlib.Path:

    """
    Returns the path to the file from which the caller of this function was called.

    Returns:
        The path to the file from which the caller of this function was called.
    """

    # Check stack to get the file name
    caller = inspect.currentframe().f_back.f_back.f_code.co_filename
    file_path = pathlib.Path(caller)
    return file_path

#####################################################################################################################################################

def create_workspace ( target_directory: str
                     ) ->                None:

    """
    Creates all the directories for a clean student workspace.
    Also creates a few default programs to start with.
    This function also takes care of adding the workspace to the Python path so that it can be used directly.
    
    Args:
        target_directory: The directory in which to create the workspace.
    """

    # Debug
    assert isinstance(target_directory, str), "Argument 'target_directory' must be a string"
    assert is_valid_directory(os.path.join(target_directory, "pyrat_workspace")), "Workspace directory cannot be created"

    # Copy the template workspace into the target directory if not already existing
    source_workspace = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "workspace")
    target_workspace = os.path.abspath(os.path.join(target_directory, "pyrat_workspace"))
    shutil.copytree(source_workspace, target_workspace, ignore=shutil.ignore_patterns('__pycache__'))
    print(f"Workspace created in {target_workspace}", file=sys.stderr)

    # Permanently add the workspace to path
    site_packages = site.getusersitepackages()
    pth_file = os.path.join(site_packages, "pyrat_workspace_path.pth")
    with open(pth_file, "w") as f:
        f.write(target_workspace + "\n")
    print(f"Workspace added to Python path", file=sys.stderr)

#####################################################################################################################################################

def is_valid_directory ( directory: str
                       ) ->         bool:

    """
    Checks if a directory exists or can be created, without actually creating it.

    Args:
        directory: The directory to check.
    
    Returns:
        ``True`` if the directory can be created, ``False`` otherwise.
    """

    # Debug
    assert isinstance(directory, str), "Argument 'directory' must be a string"

    # Initialize the fake filesystem
    valid = False
    with pyfakefs.fake_filesystem_unittest.Patcher() as patcher:
        fs = patcher.fs
        directory_path = pathlib.Path(directory)
        
        # Try to create the directory in the fake filesystem
        try:
            fs.makedirs(directory_path, exist_ok=True)
            valid = True
        except:
            pass
    
    # Done
    return valid

#####################################################################################################################################################

def pyrat_files () -> List[pathlib.Path]:

    """
    Returns the list of all the paths to files in the PyRat library.

    Returns:
        * file_paths: The list of all the paths to files in the PyRat library.
    """

    # Get the list of all the files in the PyRat library
    pyrat_path = os.path.dirname(os.path.realpath(__file__))
    file_paths = [pathlib.Path(os.path.join(pyrat_path, file)) for file in os.listdir(pyrat_path) if file.endswith(".py")]
    return file_paths

#####################################################################################################################################################
#####################################################################################################################################################