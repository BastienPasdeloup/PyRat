#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# Please import necessary elements using the following syntax:
#     from pyrat import <element_name>

"""
This module provides utility functions for the PyRat library.
It includes mainly a function to create a workspace, which is meant to be called just at the beginning of a PyRat project.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
import pyfakefs.fake_filesystem_unittest
import os
import shutil
import pathlib
import sys
import pyfakefs
import site

#####################################################################################################################################################
##################################################################### FUNCTIONS #####################################################################
#####################################################################################################################################################

def create_workspace ( target_directory: str
                     ) ->                None:

    """
    Creates all the directories for a clean student workspace.
    Also creates a few default programs to start with.
    This function also takes care of adding the workspace to the Python path so that it can be used directly.
    If the workspace already exists, it is not modified but we setup the Python path anyway to use it.
    
    Args:
        target_directory: The directory in which to create the workspace.
    """

    # Debug
    assert isinstance(target_directory, str), "Argument 'target_directory' must be a string"
    assert is_valid_directory(os.path.join(target_directory, "pyrat_workspace")), "Workspace directory cannot be created"

    # Copy the template workspace into the target directory if not already existing
    source_workspace = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "workspace")
    target_workspace = os.path.abspath(os.path.join(target_directory, "pyrat_workspace"))
    if not os.path.exists(target_workspace):
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
#####################################################################################################################################################