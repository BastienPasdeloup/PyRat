##########################################################################################
########################################## INFO ##########################################
##########################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# It is internal to the library, and nothing in it is meant to be imported by PyRat programs.
# Its entry point is the "pyrat-init" command, which is installed along with the library.

"""
This module creates the workspace in which students write their PyRat programs.
The workspace is created as a `uv <https://docs.astral.sh/uv>`_ project, so that its Python version and its dependencies are handled for you.
It is created from a terminal using the ``pyrat-init`` command, which is installed along with the PyRat library.
"""

##########################################################################################
######################################### IMPORTS ########################################
##########################################################################################

# External imports
import argparse
import os
import shutil
import subprocess
import sys

# PyRat imports
from pyrat.src.game.exceptions import PyRatException
from pyrat.src.utils import is_valid_directory

##########################################################################################
######################################## CONSTANTS #######################################
##########################################################################################

# Python version used by the workspaces, in a format understood by the "--python" option of uv
PYTHON_VERSION = ">=3.12,<3.14"

# Requirement added to the dependencies of the workspaces to make the PyRat library available
PYRAT_REQUIREMENT = "pyrat-game"

# Name of the package that contains the programs of a workspace
# Its directories, such as "players" and "games", are subpackages, and so are those the student creates
WORKSPACE_PACKAGE_NAME = "pyrat_workspace"

# Configuration added to the "pyproject.toml" file of the workspaces, so that they are installed in their virtual environment
# Installing the workspace is what makes its package importable from anywhere, as in "from pyrat_workspace.players.random1 import Random1"
# uv installs it in editable mode, so the files that run are the ones the student edits, and directories added later need no new declaration
BUILD_CONFIGURATION = '''
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["{package}"]

[tool.uv]
package = true
'''

# Name of the virtual environment directory of a workspace, and of the script in it that tells us how it was created
# uv can create a "relocatable" virtual environment, whose scripts find their own location instead of storing it once and for all
# A virtual environment that is not relocatable records an absolute path, and stops working as soon as the workspace is renamed or moved
VENV_DIRECTORY_NAME = ".venv"
VENV_MARKER_FILES = [os.path.join("bin", "activate"), os.path.join("Scripts", "activate")]
VENV_MARKER_VARIABLE = "VIRTUAL_ENV="

# Description written in the "pyproject.toml" file of the created workspaces
WORKSPACE_DESCRIPTION = "Workspace for the PyRat software"

# Directory containing the files copied into every new workspace
TEMPLATE_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "workspace")

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
    This function also takes care of making the workspace installable, so that its package is available in its virtual environment and players can be imported from games.
    The workspace is installed in editable mode, so that the files run are always the ones the student edits, and it is reinstalled by uv whenever it is needed.
    The virtual environment is created relocatable, so that renaming or moving a workspace keeps its commands working; uv reinstalls the workspace itself on the next command it runs there.
    The programs live in a ``pyrat_workspace`` package, whose subdirectories, including those the student creates later, are importable without any further declaration.
    If the workspace already exists, its contents are not modified, but we make sure it is a uv project with PyRat available anyway.

    Args:
        target_directory:  The directory in which to create the workspace.
        pyrat_requirement: The requirement to add to the workspace to make the PyRat library available.

    Raises:
        PyRatException: If uv cannot be found, or if one of the uv commands used to prepare the workspace fails.
    """

    # Debug
    assert isinstance(target_directory, str), "Argument 'target_directory' must be a string"
    assert isinstance(pyrat_requirement, str), "Argument 'pyrat_requirement' must be a string"
    assert is_valid_directory(target_directory), "Workspace directory cannot be created"

    # Check what already exists, as we do not want to overwrite the work of the student
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
    # The directory was just created by uv, thus the "dirs_exist_ok" argument
    # The files written by uv that the template also provides (README, .gitignore) are replaced by those of the template
    if not workspace_existed:
        shutil.copytree(TEMPLATE_DIRECTORY, target_workspace, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__"))
        print(f"Workspace created in {target_workspace}", file=sys.stderr)
    else:
        print(f"Workspace {target_workspace} already exists, its contents were left unchanged", file=sys.stderr)

    # Make the workspace installable, so that its package becomes available in its virtual environment
    # This is what allows games to import players, as in "from pyrat_workspace.players.random1 import Random1"
    if _add_build_configuration(target_workspace):
        print("Workspace configured to be installed in its virtual environment", file=sys.stderr)

    # Give the workspace a relocatable virtual environment, so that renaming or moving it does not break its commands
    if _prepare_virtual_environment(target_workspace):
        print("Relocatable virtual environment created for the workspace", file=sys.stderr)

    # Add PyRat to the dependencies of the workspace
    # This also installs the workspace itself in the virtual environment
    _run_uv(["add", pyrat_requirement], cwd=target_workspace)
    print("PyRat added to the dependencies of the workspace", file=sys.stderr)

    # Confirmation
    print("Your workspace is ready! You can now start coding your players and run games.", file=sys.stderr)
    print(f"To run a game, go to the workspace using 'cd {target_directory}', then use for instance 'uv run {WORKSPACE_PACKAGE_NAME}/games/sample_game.py'.", file=sys.stderr)

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
        PyRatException: If the uv command cannot be found on the system.
    """

    # Look for uv, and complain in a way that tells the user what to do if it is missing
    uv_executable = os.environ.get("UV") or shutil.which("uv")
    if uv_executable is None:
        raise PyRatException("Command 'uv' not found -- Please install uv as described in https://docs.astral.sh/uv/getting-started/installation")
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
        PyRatException: If the uv command cannot be found on the system, or if the command fails.
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
        raise PyRatException("Command 'uv " + " ".join(arguments) + f"' failed with code {completed_process.returncode}" + details)

    # Done
    return completed_process.stdout if capture_output else ""

##########################################################################################

def _add_build_configuration ( target_workspace: str
                             ) ->                bool:

    """
    Adds to the ``pyproject.toml`` file of a workspace the configuration that makes it installable.
    Once installed, the package of the workspace is available in its virtual environment, so games can import players from anywhere.
    uv installs the workspace in editable mode, which means that the files run are always the ones the student edits.
    Nothing is written if the file already describes how to build the workspace, so that a customized configuration is preserved.

    Args:
        target_workspace: The directory of the workspace.

    Returns:
        ``True`` if the configuration was added, ``False`` if the file already had one.
    """

    # Debug
    assert isinstance(target_workspace, str), "Argument 'target_workspace' must be a string"

    # Do nothing if the workspace already describes how it should be built
    pyproject_file = os.path.join(target_workspace, "pyproject.toml")
    with open(pyproject_file, "r", encoding="utf-8") as f:
        contents = f.read()
    if "[build-system]" in contents:
        return False

    # Append the configuration, making sure it starts on its own line
    with open(pyproject_file, "a", encoding="utf-8") as f:
        f.write(("" if contents.endswith("\n") else "\n") + BUILD_CONFIGURATION.format(package=WORKSPACE_PACKAGE_NAME))
    return True

##########################################################################################

def _prepare_virtual_environment ( target_workspace: str
                                 ) ->                bool:

    """
    Makes sure the workspace has a relocatable virtual environment, creating it if needed.
    A virtual environment normally records the absolute path it was created for, in the scripts that activate it and in the commands it installs.
    Renaming or moving a workspace would therefore break it, which is why we ask uv for a relocatable one, whose scripts find their own location.
    An existing virtual environment that still records an absolute path was created by an older version of PyRat, or by uv itself, and is replaced.

    Args:
        target_workspace: The directory of the workspace.

    Returns:
        ``True`` if a virtual environment was created, ``False`` if a relocatable one was already there.

    Raises:
        PyRatException: If the uv command cannot be found on the system, or if the virtual environment cannot be created.
    """

    # Debug
    assert isinstance(target_workspace, str), "Argument 'target_workspace' must be a string"

    # Replace a virtual environment that records an absolute path, as it would stop working as soon as the workspace moves
    venv_directory = os.path.join(target_workspace, VENV_DIRECTORY_NAME)
    if os.path.isdir(venv_directory) and _records_absolute_path(venv_directory):
        shutil.rmtree(venv_directory, ignore_errors=True)

    # Keep the virtual environment already there, otherwise ask uv for a relocatable one
    if os.path.isdir(venv_directory):
        return False
    _run_uv(["venv", "--relocatable"], cwd=target_workspace)
    return True

##########################################################################################

def _records_absolute_path ( venv_directory: str
                           ) ->              bool:

    """
    Tells whether a virtual environment stores the absolute path it was created for, rather than finding its own location.
    We read the activation script, which sets the location of the virtual environment: a relocatable one computes it, a regular one writes it down.
    We answer ``False`` when we cannot tell, as deleting a working virtual environment would make us lose the libraries installed in it.

    Args:
        venv_directory: The virtual environment directory of a workspace.

    Returns:
        ``True`` if the virtual environment records an absolute path, ``False`` otherwise.
    """

    # Debug
    assert isinstance(venv_directory, str), "Argument 'venv_directory' must be a string"

    # Read the location the activation script gives to the virtual environment
    for marker_file in VENV_MARKER_FILES:
        marker_path = os.path.join(venv_directory, marker_file)
        if not os.path.isfile(marker_path):
            continue
        with open(marker_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                if line.startswith(VENV_MARKER_VARIABLE):
                    recorded = line[len(VENV_MARKER_VARIABLE):].strip().strip("'\"")
                    return os.path.isabs(recorded)

    # Nothing conclusive
    return False

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
