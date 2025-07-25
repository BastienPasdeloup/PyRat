#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This file is part of the PyRat library.
    It is meant to be used as a library, and not to be executed directly.
    Please import necessary elements using the following syntax:
        from pyrat import <element_name>
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
import pdoc
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
        In:
            * target_directory: The directory in which to create the workspace.
        Out:
            * None.
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

def generate_documentation ( workspace_directory: str
                           ) ->                   None:

    """
        Generates the documentation for the project.
        The function will parse the PyRat library, and all the subdirectories of the workspace directory.
        This will create a doc directory in the workspace directory, and fill it with the documentation.
        In:
            * workspace_directory: The directory in which the workspace is located.
        Out:
            * None.
    """
    
    # Debug
    assert isinstance(workspace_directory, str), "Argument 'workspace_directory' must be a string"
    assert is_valid_directory(os.path.join(workspace_directory, "doc")), "Doc directory cannot be created"

    # Process paths
    target_directory = pathlib.Path(os.path.join(workspace_directory, "doc"))
    workspace_subdirectories = [os.path.join(workspace_directory, directory) for directory in os.listdir(workspace_directory) if directory != "doc"]
    for d in workspace_subdirectories:
        sys.path.append(d)
    
    # Generate the documentation for PyRat, and for workspace subdirectories
    pdoc.render.configure(docformat="google")
    pdoc.pdoc("pyrat", *workspace_subdirectories, output_directory=target_directory)

#####################################################################################################################################################

def caller_file () -> pathlib.Path:

    """
        Returns the path to the file from which the caller of this function was called.
        In:
            * None.
        Out:
            * file_path: The path to the file from which the caller of this function was called.
    """

    # Check stack to get the file name
    caller = inspect.currentframe().f_back.f_back.f_code.co_filename
    file_path = pathlib.Path(caller)
    return file_path

#####################################################################################################################################################

def pyrat_files () -> List[pathlib.Path]:

    """
        Returns the list of all the paths to files in the PyRat library.
        In:
            * None.
        Out:
            * file_paths: The list of all the paths to files in the PyRat library.
    """

    # Get the list of all the files in the PyRat library
    pyrat_path = os.path.dirname(os.path.realpath(__file__))
    file_paths = [pathlib.Path(os.path.join(pyrat_path, file)) for file in os.listdir(pyrat_path) if file.endswith(".py")]
    return file_paths

#####################################################################################################################################################

def is_valid_directory ( directory: str
                       ) ->         bool:

    """
        Checks if a directory exists or can be created, without actually creating it.
        In:
            * directory: The directory to check.
        Out:
            * valid: True if the directory can be created, False otherwise.
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