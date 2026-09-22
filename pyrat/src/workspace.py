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
The same command, run from a workspace that already exists, repairs it by giving it a clean virtual environment, without touching the programs it contains.
"""

##########################################################################################
######################################### IMPORTS ########################################
##########################################################################################

# External imports
import argparse
import os
import re
import shutil
import subprocess
import sys
import tomllib

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

# Directory in which a workspace is created when none is given, unless the command is run from an existing workspace
# It is not named after the package it contains, so that the two are told apart when reading a path such as "pyrat_project/pyrat_workspace/players"
DEFAULT_WORKSPACE_DIRECTORY = "pyrat_project"

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

# Name of the virtual environment directory of a workspace
# uv creates a "relocatable" virtual environment, whose scripts find their own location instead of storing it once and for all, but only when it is explicitly asked to
# Any virtual environment uv recreates on its own, for instance because it was deleted, therefore records an absolute path again, and stops working as soon as the workspace is renamed or moved
# This is why running "pyrat-init" on an existing workspace rebuilds its virtual environment from scratch, rather than trying to fix the one that is there
VENV_DIRECTORY_NAME = ".venv"

# Description written in the "pyproject.toml" file of the created workspaces
WORKSPACE_DESCRIPTION = "Workspace for the PyRat software"

# Directory containing the files copied into every new workspace
TEMPLATE_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "workspace")

##########################################################################################
######################################## FUNCTIONS #######################################
##########################################################################################

def init_workspace ( target_directory:  str | None = None,
                     pyrat_requirement: str = PYRAT_REQUIREMENT
                   ) ->                 None:

    """
    Creates a clean student workspace, as a `uv <https://docs.astral.sh/uv>`_ project, or repairs an existing one.
    The workspace is initialized with ``uv init``, which fixes the Python version to use and creates the files needed by uv.
    Then, a few default programs are added to start with, and the PyRat library is added to the dependencies of the workspace.
    This function also takes care of making the workspace installable, so that its package is available in its virtual environment and players can be imported from games.
    The workspace is installed in editable mode, so that the files run are always the ones the student edits, and it is reinstalled by uv whenever it is needed.
    The programs live in a ``pyrat_workspace`` package, whose subdirectories, including those the student creates later, are importable without any further declaration.

    Running this on a workspace that already exists repairs it: the programs of the student are left untouched, but the workspace is given a brand new virtual environment.
    That environment is created relocatable, so that renaming or moving the workspace keeps its commands working, and everything the workspace declares is installed in it again.
    This is how a workspace is fixed when its virtual environment was damaged, or when it was recreated by uv itself and thus lost the ability to be moved around.
    When no directory is given, the workspace to repair is the current directory if it is already a PyRat workspace, and a new workspace is created in a ``pyrat_project`` directory otherwise.

    Args:
        target_directory:  The directory in which to create the workspace, or ``None`` to determine it from the current directory.
        pyrat_requirement: The requirement to add to the workspace to make the PyRat library available.

    Raises:
        PyRatException: If uv cannot be found, if the command runs from the virtual environment it has to rebuild, or if one of the uv commands used to prepare the workspace fails.
    """

    # Debug
    assert isinstance(target_directory, (str, type(None))), "Argument 'target_directory' must be a string or None"
    assert isinstance(pyrat_requirement, str), "Argument 'pyrat_requirement' must be a string"

    # Repair the current directory when it is already a workspace, rather than creating a new workspace inside it
    if target_directory is None:
        target_directory = "." if _is_pyrat_workspace(os.getcwd()) else DEFAULT_WORKSPACE_DIRECTORY

    # Debug
    assert is_valid_directory(target_directory), "Workspace directory cannot be created"

    # Check what already exists, as we do not want to overwrite the work of the student
    # A directory is taken for an existing workspace once it is a uv project, so that an empty directory still receives the programs to start with
    target_workspace = os.path.abspath(target_directory)
    existing_files = set(os.listdir(target_workspace)) if os.path.isdir(target_workspace) else set()
    workspace_existed = "pyproject.toml" in existing_files

    # Make the target directory a uv project if not already the case
    if not workspace_existed:
        _run_uv(["init", "--no-package", "--vcs", "git", "--python", PYTHON_VERSION, target_workspace])
        _set_workspace_description(target_workspace, WORKSPACE_DESCRIPTION)
        print(f"Workspace initialized as a uv project using Python {PYTHON_VERSION}", file=sys.stderr)

    # Remove the example program created by uv, as the workspace comes with its own programs
    if "main.py" not in existing_files and os.path.exists(os.path.join(target_workspace, "main.py")):
        os.remove(os.path.join(target_workspace, "main.py"))

    # Copy the template workspace into the target directory, unless it is a workspace whose programs we must not touch
    # The directory already exists, as uv just made it a project, thus the "dirs_exist_ok" argument
    # The files written by uv that the template also provides (README, .gitignore) are replaced by those of the template
    if not workspace_existed:
        shutil.copytree(TEMPLATE_DIRECTORY, target_workspace, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__"))
        print(f"Workspace created in {target_workspace}", file=sys.stderr)
    else:
        print(f"Workspace {target_workspace} already exists, its contents are left unchanged", file=sys.stderr)

    # Make the workspace installable, so that its package becomes available in its virtual environment
    # This is what allows games to import players, as in "from pyrat_workspace.players.random1 import Random1"
    if _add_build_configuration(target_workspace):
        print("Workspace configured to be installed in its virtual environment", file=sys.stderr)

    # Give the workspace a brand new relocatable virtual environment, so that renaming or moving it does not break its commands
    # Nothing is lost by replacing the one that may be there, as a workspace describes everything it needs in its "pyproject.toml" file
    _prepare_virtual_environment(target_workspace)
    print("Clean relocatable virtual environment created for the workspace", file=sys.stderr)

    # Add PyRat to the dependencies of the workspace
    # This also installs in the virtual environment the workspace itself, and everything else the workspace declares
    _run_uv(["add", pyrat_requirement], cwd=target_workspace)
    print("PyRat added to the dependencies of the workspace", file=sys.stderr)

    # Confirmation, telling the student how to reach the workspace unless they already are in it
    print("Your workspace is ready! You can now start coding your players and run games.", file=sys.stderr)
    move_to_workspace = "" if target_workspace == os.getcwd() else f"go to the workspace using 'cd {target_directory}', then "
    print(f"To run a game, {move_to_workspace}use for instance 'uv run {WORKSPACE_PACKAGE_NAME}/games/sample_game.py'.", file=sys.stderr)

##########################################################################################

def main () -> None:

    """
    Entry point of the ``pyrat-init`` command, which creates or repairs a PyRat workspace from a terminal.
    It is a simple command line interface around the :func:`init_workspace` function.
    """

    # Describe the command line interface
    parser = argparse.ArgumentParser(prog="pyrat-init", description="Creates a PyRat workspace, as a uv project in which PyRat is available. Run from an existing workspace, it repairs it by giving it a clean virtual environment.")
    parser.add_argument("target_directory", nargs="?", default=None, help=f"Directory in which to create the workspace, or the workspace to repair (default: the current directory when it is a PyRat workspace, and {DEFAULT_WORKSPACE_DIRECTORY} otherwise)")
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
                                 ) ->                None:

    """
    Gives the workspace a brand new relocatable virtual environment, replacing the one it may already have.
    A virtual environment normally records the absolute path it was created for, in the scripts that activate it and in the commands it installs.
    Renaming or moving a workspace would therefore break it, which is why we ask uv for a relocatable one, whose scripts find their own location.
    uv only does so when asked, so the virtual environment of a workspace loses that property as soon as uv has to recreate it, and rebuilding it here is what gives it back.
    Replacing the virtual environment costs nothing, as a workspace describes in its ``pyproject.toml`` file every library that has to be installed in it.

    Args:
        target_workspace: The directory of the workspace.

    Raises:
        PyRatException: If the uv command cannot be found on the system, if the running program uses the virtual environment to replace, or if the virtual environment cannot be created.
    """

    # Debug
    assert isinstance(target_workspace, str), "Argument 'target_workspace' must be a string"

    # Remove the virtual environment that is already there, unless we are the program it runs, as we would be pulling the rug from under our own feet
    venv_directory = os.path.join(target_workspace, VENV_DIRECTORY_NAME)
    if os.path.isdir(venv_directory):
        if _runs_from_virtual_environment(venv_directory):
            raise PyRatException("Command 'pyrat-init' is provided by the virtual environment it has to replace -- Please repair the workspace using 'uvx --from pyrat-game pyrat-init' instead")
        shutil.rmtree(venv_directory, ignore_errors=True)

    # Ask uv for a relocatable virtual environment
    _run_uv(["venv", "--relocatable"], cwd=target_workspace)

##########################################################################################

def _runs_from_virtual_environment ( venv_directory: str
                                   ) ->              bool:

    """
    Tells whether the Python interpreter running this program is the one of the given virtual environment.
    This happens when the ``pyrat-init`` command installed in a workspace is the one used to repair that same workspace.
    Removing that virtual environment would take away the interpreter and the libraries in use, which some systems refuse to do anyway.

    Args:
        venv_directory: The virtual environment directory of a workspace.

    Returns:
        ``True`` if the running interpreter comes from that virtual environment, ``False`` otherwise.
    """

    # Debug
    assert isinstance(venv_directory, str), "Argument 'venv_directory' must be a string"

    # Compare where the interpreter lives with the virtual environment, following links so that both are described the same way
    return os.path.realpath(sys.prefix) == os.path.realpath(venv_directory)

##########################################################################################

def _is_pyrat_workspace ( directory: str
                        ) ->         bool:

    """
    Tells whether a directory is already a PyRat workspace, rather than a directory in which one should be created.
    A workspace is recognized by its ``pyproject.toml`` file declaring PyRat among its dependencies, which is what :func:`init_workspace` writes in it.
    We answer ``False`` when that file is missing or cannot be understood, so that a directory we know nothing about is never taken for a workspace to repair.

    Args:
        directory: The directory to examine.

    Returns:
        ``True`` if the directory is a PyRat workspace, ``False`` otherwise.
    """

    # Debug
    assert isinstance(directory, str), "Argument 'directory' must be a string"

    # Read the project description of the directory, if it has one we can make sense of
    pyproject_file = os.path.join(directory, "pyproject.toml")
    if not os.path.isfile(pyproject_file):
        return False
    try:
        with open(pyproject_file, "rb") as f:
            contents = tomllib.load(f)
    except (OSError, tomllib.TOMLDecodeError):
        return False

    # A workspace is a project that depends on PyRat
    project = contents.get("project")
    dependencies = project.get("dependencies", []) if isinstance(project, dict) else []
    return any(isinstance(dependency, str) and _requirement_name(dependency) == PYRAT_REQUIREMENT for dependency in dependencies)

##########################################################################################

def _requirement_name ( requirement: str
                      ) ->           str:

    """
    Extracts the name of the library a requirement refers to, as requirements are written in the dependencies of a project.
    A requirement may carry a version, extras or a condition, as in ``pyrat-game>=6.4.4``, which are not part of the name.
    The name is returned in the form used to compare requirements, in which neither the case nor the separators matter.

    Args:
        requirement: The requirement to examine.

    Returns:
        The name of the library the requirement refers to.
    """

    # Debug
    assert isinstance(requirement, str), "Argument 'requirement' must be a string"

    # Keep what comes before the version, the extras and the condition, then write it the way the packaging specification asks
    name = re.split(r"[\[<>=!~;@\s]", requirement.strip(), maxsplit=1)[0]
    return re.sub(r"[-_.]+", "-", name).lower()

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
