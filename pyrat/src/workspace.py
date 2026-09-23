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
Once created, a workspace needs nothing else from PyRat: ``uv sync`` is what rebuilds it, after a clone or at any other time.
"""

##########################################################################################
######################################### IMPORTS ########################################
##########################################################################################

# External imports
import argparse
import importlib.metadata
import os
import re
import shutil
import subprocess
import sys

# PyRat imports
from pyrat.src.game.exceptions import PyRatException

##########################################################################################
######################################## CONSTANTS #######################################
##########################################################################################

# Python version used by the workspaces, as written in the "requires-python" field of their description
PYTHON_VERSION = ">=3.12,<3.14"

# Requirement added to the dependencies of the workspaces to make the PyRat library available
PYRAT_REQUIREMENT = "pyrat-game"

# Directory in which a workspace is created when none is given
DEFAULT_WORKSPACE_DIRECTORY = "pyrat_workspace"

# File that makes the directories of a workspace importable, as in "from players.random1 import Random1"
# Python reads it when it starts, and it deduces the workspace from the virtual environment that contains it, so moving a workspace does not break it
# Installing the workspace records its location a second time, in the usual way, which covers the rarer setups in which the virtual environment is kept outside of it
# Its name must differ from the one uv gives to the file it writes for the workspace itself, which is built from the name of the project
PATH_FILE_NAME = "_pyrat_relocatable.pth"

# uv feature asking for relocatable virtual environments, declared by the workspaces in their description
# Without it, the commands installed in the virtual environment record the absolute path of the workspace, and stop working as soon as it is renamed or moved
RELOCATABLE_FEATURE = "relocatable-envs-default"

# Oldest version of uv that understands the feature above
# Older versions report an unknown field and ignore the whole uv configuration of the workspace, so they are worth naming when we ask the student to upgrade
MINIMUM_UV_VERSION = "0.12.0"

# Description of the project written in every new workspace
WORKSPACE_DESCRIPTION = "Workspace for the PyRat software"

# Directory containing the files copied into every new workspace
TEMPLATE_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "workspace")

# Description of the project written in every new workspace, which is what uv reads to prepare it
# The workspace is a uv project that installs itself, and installing it is what makes its directories importable, in two complementary ways
# The "dev-mode-dirs" setting records where the workspace is, as any project installed in editable mode does, which uv rewrites whenever it reinstalls the workspace
# The file added by "force-include" finds the workspace on its own instead, which is what keeps a renamed or moved workspace working with no command to run
# Neither of them lists the directories of the workspace, so the ones the student creates later are importable without any new declaration
PYPROJECT_TEMPLATE = '''\
[project]
name = "pyrat-workspace"
version = "0.1.0"
description = "{description}"
requires-python = "{python_version}"
dependencies = ["{pyrat_requirement}"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
bypass-selection = true
dev-mode-dirs = ["."]
force-include = {{"{path_file}" = "{path_file}"}}

[tool.uv]
package = true
preview-features = ["{relocatable_feature}"]
'''

##########################################################################################
######################################## FUNCTIONS #######################################
##########################################################################################

def init_workspace ( target_directory:  str | None = None,
                     pyrat_requirement: str = PYRAT_REQUIREMENT
                   ) ->                 None:

    """
    Creates a student workspace, as a `uv <https://docs.astral.sh/uv>`_ project in which the PyRat library is available.
    The workspace receives a few programs to start with, in a ``players`` directory and a ``games`` directory, and a description of the project telling uv what to install.
    Then ``uv sync`` gives it a virtual environment containing PyRat and the workspace itself.

    Installing the workspace adds it to the directories Python imports from, which is what makes every one of its directories importable, as in ``from players.random1 import Random1``.
    Nothing lists those directories, so the ones the student creates later are importable as well, with nothing to declare.
    This is recorded in two complementary ways: where the workspace is, as for any project installed in editable mode, and a file that finds the workspace from the virtual environment it contains.
    The latter is what keeps a renamed or moved workspace working with no command to run, while the former covers the rarer setups in which the virtual environment is kept outside the workspace.

    Nothing else is ever needed from PyRat: a workspace describes everything it needs, so ``uv sync`` is what rebuilds it, whether it was just cloned or its virtual environment was damaged.

    Args:
        target_directory:  The directory in which to create the workspace, or ``None`` to use the default one.
        pyrat_requirement: The requirement to add to the workspace to make the PyRat library available.

    Raises:
        PyRatException: If uv cannot be found, if the target directory already contains a project, or if uv fails to prepare the workspace.
    """

    # Debug
    assert isinstance(target_directory, (str, type(None))), "Argument 'target_directory' must be a string or None"
    assert isinstance(pyrat_requirement, str), "Argument 'pyrat_requirement' must be a string"

    # Warn about a uv too old to understand the configuration we write, rather than let it report an unknown field on every command
    _warn_if_uv_is_too_old()

    # Refuse to write into a directory that already describes a project, as it is a workspace whose programs we must not overwrite
    # Such a workspace has nothing to receive from us anyway, as uv rebuilds it from the description it already contains
    target_directory = target_directory or DEFAULT_WORKSPACE_DIRECTORY
    target_workspace = os.path.abspath(target_directory)
    if os.path.isfile(os.path.join(target_workspace, "pyproject.toml")):
        raise PyRatException(f"Directory {target_workspace} already contains a project -- Please run 'uv sync' from it to rebuild its virtual environment, or choose another directory to create a new workspace")

    # Copy the programs to start with, as well as the file that makes the directories of the workspace importable
    shutil.copytree(TEMPLATE_DIRECTORY, target_workspace, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__"))

    # Describe the project, which is what tells uv the Python version to use, the libraries to install, and how to install the workspace itself
    with open(os.path.join(target_workspace, "pyproject.toml"), "w", encoding="utf-8") as f:
        f.write(PYPROJECT_TEMPLATE.format(description=WORKSPACE_DESCRIPTION,
                                          python_version=PYTHON_VERSION,
                                          pyrat_requirement=pyrat_requirement,
                                          path_file=PATH_FILE_NAME,
                                          relocatable_feature=RELOCATABLE_FEATURE))
    print(f"Workspace created in {target_workspace}, as a uv project using Python {PYTHON_VERSION}", file=sys.stderr)

    # Give the workspace a repository of its own, so that the commits made from it do not go to a repository that happens to contain it
    _init_git_repository(target_workspace)

    # Install everything the workspace declares, which creates its virtual environment along the way
    _run_uv(["sync"], cwd=target_workspace)
    print("Virtual environment created, with PyRat installed in it", file=sys.stderr)

    # Confirmation, telling the student how to reach the workspace unless they already are in it
    print("Your workspace is ready! You can now start coding your players and run games.", file=sys.stderr)
    move_to_workspace = "" if target_workspace == os.getcwd() else f"go to the workspace using 'cd {target_directory}', then "
    print(f"To run a game, {move_to_workspace}use for instance 'uv run games/sample_game.py'.", file=sys.stderr)

##########################################################################################

def main () -> None:

    """
    Entry point of the ``pyrat-init`` command, which creates a PyRat workspace from a terminal.
    It is a simple command line interface around the :func:`init_workspace` function.
    """

    # Describe the command line interface
    parser = argparse.ArgumentParser(prog="pyrat-init", description="Creates a PyRat workspace, as a uv project in which PyRat is available.")
    parser.add_argument("target_directory", nargs="?", default=None, help=f"Directory in which to create the workspace (default: {DEFAULT_WORKSPACE_DIRECTORY})")
    parser.add_argument("--pyrat-requirement", default=PYRAT_REQUIREMENT, help="Requirement to add to the workspace to make PyRat available (default: %(default)s)")
    parser.add_argument("--version", action="version", version=_pyrat_version(), help="Show the version of PyRat that provides this command, and exit")
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

def _init_git_repository ( target_workspace: str
                         ) ->                None:

    """
    Gives the workspace a Git repository of its own, so that the programs of the student can be versioned right away.
    A workspace created inside a repository that already exists would otherwise send every commit made from it to that repository, which is rarely what the student wants and which nothing in the workspace shows.
    Failing to create the repository is only worth a warning, as the workspace itself is perfectly usable without one.

    Args:
        target_workspace: The directory of the workspace.
    """

    # Debug
    assert isinstance(target_workspace, str), "Argument 'target_workspace' must be a string"

    # Say what to do rather than fail, as versioning the workspace is not what the student asked for
    git_executable = shutil.which("git")
    if git_executable is None:
        print(f"Warning: command 'git' not found, so no repository was created -- Please run 'git init' from {target_workspace} once Git is installed, if you want to version your programs", file=sys.stderr)
        return

    # Create the repository, reporting a failure without making the whole command fail
    completed_process = subprocess.run([git_executable, "init", "--quiet", target_workspace], capture_output=True, text=True)
    if completed_process.returncode != 0:
        print(f"Warning: no Git repository could be created ({completed_process.stderr.strip()}) -- Please run 'git init' from {target_workspace} if you want to version your programs", file=sys.stderr)
    else:
        print("Git repository created for the workspace", file=sys.stderr)

##########################################################################################

def _warn_if_uv_is_too_old () -> None:

    """
    Warns the student when the uv they run is older than the oldest version that understands the configuration we write in their workspace.
    Such a version reports an unknown field and ignores the whole uv configuration of the workspace, on every command, which is a confusing way to discover the problem.
    We only warn, as everything else in the workspace still works, and the version of uv is not ours to change.
    """

    # Read the version of uv, and say nothing if we cannot make sense of it, as this is only a warning
    version = re.search(r"(\d+)\.(\d+)\.(\d+)", _run_uv(["--version"], capture_output=True))
    if version is None:
        return

    # Compare it with the version we need, and explain what to do
    current_version = tuple(int(number) for number in version.groups())
    minimum_version = tuple(int(number) for number in MINIMUM_UV_VERSION.split("."))
    if current_version < minimum_version:
        print(f"Warning: your uv is version {'.'.join(str(number) for number in current_version)}, and PyRat workspaces need {MINIMUM_UV_VERSION} or later", file=sys.stderr)
        print(f"Warning: older versions report an unknown field in 'pyproject.toml' and ignore the uv configuration of your workspace -- Please update uv, as described in https://docs.astral.sh/uv/getting-started/installation", file=sys.stderr)

##########################################################################################

def _pyrat_version () -> str:

    """
    Gives the version of the PyRat library that provides the running ``pyrat-init`` command.
    Knowing it is what allows a problem reported by a student to be reproduced, as the command may come from a version older than the one they think they are using.

    Returns:
        The version of the library, or a placeholder when it is run from sources that were never installed.
    """

    # Read the version recorded at installation, which is missing when the library is run from its sources
    try:
        return importlib.metadata.version("pyrat-game")
    except importlib.metadata.PackageNotFoundError:
        return "unknown (PyRat is run from its sources)"

##########################################################################################
##########################################################################################
