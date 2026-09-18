##########################################################################################
########################################## INFO ##########################################
##########################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# Please import necessary elements using the following syntax:
#     from pyrat import <element_name>

"""
This module provides utility functions for the PyRat library.
It includes mainly a function to create a workspace, which is meant to be called just at the beginning of a PyRat project.
The workspace is created as a `uv <https://docs.astral.sh/uv>`_ project, so that its Python version and its dependencies are handled for you.
The same thing can be done from a terminal using the ``pyrat-init`` command, which is installed along with the PyRat library.
"""

##########################################################################################
######################################### IMPORTS ########################################
##########################################################################################

# External imports
import pyfakefs.fake_filesystem_unittest
import argparse
import os
import shutil
import pathlib
import subprocess
import sys
import pyfakefs
import site
import sysconfig

##########################################################################################
######################################## CONSTANTS #######################################
##########################################################################################

# Python version used by the workspaces, in a format understood by the "--python" option of uv
PYTHON_VERSION = ">=3.12,<3.14"

# Requirement added to the dependencies of the workspaces to make the PyRat library available
PYRAT_REQUIREMENT = "pyrat-game"

# Name of the file that adds the workspace to the Python path of its virtual environment
PATH_FILE_NAME = "pyrat_workspace_path.pth"

# Description written in the "pyproject.toml" file of the created workspaces
WORKSPACE_DESCRIPTION = "Workspace for the PyRat software"

##########################################################################################
######################################## FUNCTIONS #######################################
##########################################################################################

def init_workspace ( target_directory:  str = "pyrat_workspace",
                     pyrat_requirement: str = PYRAT_REQUIREMENT
                   ) ->                 None:

    """
    Creates a clean student workspace, as a `uv <https://docs.astral.sh/uv>`_ project.
    The workspace is initialized with ``uv init``, which fixes the Python version to use and creates the files needed by uv.
    Then, a few default programs are added to start with, and the PyRat library is added to the dependencies of the workspace.
    This function also takes care of adding the workspace to the Python path of its virtual environment, so that players can be imported from games.
    If the workspace already exists, its contents are not modified, but we make sure it is a uv project with PyRat available anyway.

    Args:
        target_directory:  The directory in which to create the workspace.
        pyrat_requirement: The requirement to add to the workspace to make the PyRat library available.

    Raises:
        FileNotFoundError: If the uv command cannot be found on the system.
        RuntimeError:      If one of the uv commands used to prepare the workspace fails.
    """

    # Debug
    assert isinstance(target_directory, str), "Argument 'target_directory' must be a string"
    assert isinstance(pyrat_requirement, str), "Argument 'pyrat_requirement' must be a string"
    assert is_valid_directory(target_directory), "Workspace directory cannot be created"

    # Check what already exists, as we do not want to overwrite the work of the student
    source_workspace = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "workspace")
    target_workspace = os.path.abspath(target_directory)
    workspace_existed = os.path.exists(target_workspace)
    existing_files = set(os.listdir(target_workspace)) if workspace_existed else set()

    # Make the target directory a uv project if not already the case
    if "pyproject.toml" not in existing_files:
        _run_uv(["init", "--no-package", "--vcs", "git", "--python", PYTHON_VERSION, target_workspace])
        _set_workspace_description(target_workspace, WORKSPACE_DESCRIPTION)
        print(f"Workspace initialized as a uv project using Python {PYTHON_VERSION}", file=sys.stderr)

    # Remove the example program created by uv, as the workspace comes with its own programs
    if "main.py" not in existing_files and os.path.exists(os.path.join(target_workspace, "main.py")):
        os.remove(os.path.join(target_workspace, "main.py"))

    # Copy the template workspace into the target directory if not already existing
    # The directory may have just been created by uv, thus the "dirs_exist_ok" argument
    if not workspace_existed:
        shutil.copytree(source_workspace, target_workspace, dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__'))
        print(f"Workspace created in {target_workspace}", file=sys.stderr)
    else:
        print(f"Workspace {target_workspace} already exists, its contents were left unchanged", file=sys.stderr)

    # Add PyRat to the dependencies of the workspace
    # This also creates the virtual environment of the workspace if needed
    _run_uv(["add", pyrat_requirement], cwd=target_workspace)
    print(f"PyRat added to the dependencies of the workspace", file=sys.stderr)

    # Add the workspace to the Python path of its virtual environment, so that players can be imported from games
    site_packages = _workspace_site_packages(target_workspace)
    pth_file = os.path.join(site_packages, PATH_FILE_NAME)
    with open(pth_file, "w", encoding="utf-8") as f:
        f.write(target_workspace + "\n")
    if os.path.realpath(site_packages) == os.path.realpath(sysconfig.get_paths()["purelib"]):
        site.addsitedir(site_packages)
    print(f"Workspace added to Python path", file=sys.stderr)

    # Confirmation
    print(f"Your workspace is ready! You can now start coding your players and run games.", file=sys.stderr)
    print(f"To run a game, go to the workspace using 'cd {target_directory}', then use for instance 'uv run games/sample_game.py'.", file=sys.stderr)

##########################################################################################

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

##########################################################################################

def main () -> None:

    """
    Entry point of the ``pyrat-init`` command, which creates a PyRat workspace from a terminal.
    It is a simple command line interface around the :func:`init_workspace` function.
    """

    # Describe the command line interface
    parser = argparse.ArgumentParser(prog="pyrat-init", description="Creates a PyRat workspace, as a uv project in which PyRat is available.")
    parser.add_argument("target_directory", nargs="?", default="pyrat_workspace", help="Directory in which to create the workspace (default: %(default)s)")
    parser.add_argument("--pyrat-requirement", default=PYRAT_REQUIREMENT, help="Requirement to add to the workspace to make PyRat available (default: %(default)s)")
    arguments = parser.parse_args()

    # Create the workspace, and report errors in a readable way rather than with a traceback
    try:
        init_workspace(arguments.target_directory, arguments.pyrat_requirement)
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

##########################################################################################
#################################### PRIVATE FUNCTIONS ###################################
##########################################################################################

def _uv_executable () -> str:

    """
    Locates the uv executable to use.
    When uv runs a command itself, it indicates where it is located using an environment variable.
    Otherwise, we look for it in the directories of the system path.

    Returns:
        The path to the uv executable.

    Raises:
        FileNotFoundError: If the uv command cannot be found on the system.
    """

    # Look for uv, and complain in a way that tells the user what to do if it is missing
    uv_executable = os.environ.get("UV") or shutil.which("uv")
    if uv_executable is None:
        raise FileNotFoundError("Command 'uv' not found -- Please install uv as described in https://docs.astral.sh/uv/getting-started/installation")
    return uv_executable

##########################################################################################

def _run_uv ( arguments:      list[str],
              cwd:            str | None = None,
              capture_output: bool = False
            ) ->              str:

    """
    Runs a uv command, and fails explicitly if uv is missing or if the command does not succeed.

    Args:
        arguments:      The arguments to pass to uv.
        cwd:            The directory in which to run the command, or ``None`` to use the current one.
        capture_output: If ``True``, the output of the command is returned instead of being shown to the user.

    Returns:
        The output of the command if ``capture_output`` is ``True``, an empty string otherwise.

    Raises:
        FileNotFoundError: If the uv command cannot be found on the system.
        RuntimeError:      If the command fails.
    """

    # Debug
    assert isinstance(arguments, list), "Argument 'arguments' must be a list"
    assert all(isinstance(argument, str) for argument in arguments), "Argument 'arguments' must contain only strings"
    assert isinstance(cwd, (str, type(None))), "Argument 'cwd' must be a string or None"
    assert isinstance(capture_output, bool), "Argument 'capture_output' must be a boolean"

    # Run the command, letting uv show its progress to the user unless we need its output
    completed_process = subprocess.run([_uv_executable()] + arguments, cwd=cwd, capture_output=capture_output, text=True)
    if completed_process.returncode != 0:
        details = "\n" + completed_process.stderr.strip() if capture_output and completed_process.stderr else ""
        raise RuntimeError("Command 'uv " + " ".join(arguments) + f"' failed with code {completed_process.returncode}" + details)

    # Done
    return completed_process.stdout if capture_output else ""

##########################################################################################

def _workspace_site_packages ( target_workspace: str
                             ) ->                str:

    """
    Returns the directory where dependencies are installed in the virtual environment of a workspace.
    We ask uv rather than building the path ourselves, as it depends on the operating system and on the Python version.

    Args:
        target_workspace: The directory of the workspace.

    Returns:
        The site-packages directory of the virtual environment of the workspace.

    Raises:
        FileNotFoundError: If the uv command cannot be found on the system.
        RuntimeError:      If the location cannot be determined.
    """

    # Debug
    assert isinstance(target_workspace, str), "Argument 'target_workspace' must be a string"

    # Ask the Python of the workspace where its dependencies are installed
    command = "import sysconfig; print(sysconfig.get_paths()['purelib'])"
    site_packages = _run_uv(["run", "python", "-c", command], cwd=target_workspace, capture_output=True).strip()
    if not os.path.isdir(site_packages):
        raise RuntimeError(f"Could not locate the virtual environment of workspace {target_workspace}")

    # Done
    return site_packages

##########################################################################################

def _set_workspace_description ( target_workspace: str,
                                 description:      str
                               ) ->                None:

    """
    Replaces the placeholder description written by uv in the ``pyproject.toml`` file of a workspace.
    Nothing happens if the placeholder is not found, as this is only a cosmetic change.

    Args:
        target_workspace: The directory of the workspace.
        description:      The description to write in the ``pyproject.toml`` file.
    """

    # Debug
    assert isinstance(target_workspace, str), "Argument 'target_workspace' must be a string"
    assert isinstance(description, str), "Argument 'description' must be a string"

    # Replace the placeholder written by uv
    pyproject_file = os.path.join(target_workspace, "pyproject.toml")
    with open(pyproject_file, "r", encoding="utf-8") as f:
        contents = f.read()
    contents = contents.replace('description = "Add your description here"', f'description = "{description}"')
    with open(pyproject_file, "w", encoding="utf-8") as f:
        f.write(contents)

##########################################################################################
##########################################################################################
