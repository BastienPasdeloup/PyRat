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
import importlib.metadata
import os
import re
import shutil
import subprocess
import sys
import tomllib

# PyRat imports
from pyrat.src.game.exceptions import PyRatException

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
preview-features = ["{relocatable_feature}"]
'''

# uv feature asking for relocatable virtual environments, declared by the workspaces in their "pyproject.toml" file
# Without it, only the environment created by "uv venv --relocatable" is relocatable, and the one uv writes on its own, for instance during a "uv sync", is not
# Declaring it in the workspace is what lets a student repair their workspace with plain uv commands, rather than with a command of our own
RELOCATABLE_FEATURE = "relocatable-envs-default"

# Oldest version of uv that understands the feature above
# Older versions report an unknown field and ignore the whole uv configuration of the workspace, so they are worth naming when we ask the student to upgrade
MINIMUM_UV_VERSION = "0.12.0"

# Name of the virtual environment directory of a workspace
# A virtual environment records the absolute path it was created for, unless it is "relocatable", in which case its scripts find their own location instead
# Workspaces declare the uv feature above so that every environment uv writes for them is relocatable, including the ones a plain "uv sync" creates
# Running "pyrat-init" on an existing workspace still rebuilds the environment from scratch, which is how a workspace created before that declaration gets a relocatable one
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
    The uv configuration of the workspace is repaired as well, by removing the elements that PyRat never writes and that keep uv from working, such as those a ``uv init`` run by mistake in the package directory leaves behind.
    This is how a workspace is fixed when its virtual environment was damaged, or when it was recreated by uv itself and thus lost the ability to be moved around.
    When no directory is given, the workspace to repair is the current directory if it is already a PyRat workspace, and a new workspace is created in a ``pyrat_project`` directory otherwise.
    Creating a workspace inside another one is refused, as uv rejects every command run in nested projects.

    Args:
        target_directory:  The directory in which to create the workspace, or ``None`` to determine it from the current directory.
        pyrat_requirement: The requirement to add to the workspace to make the PyRat library available.

    Raises:
        PyRatException: If uv cannot be found, if the workspace to create is inside another one, if the command runs from the virtual environment it has to rebuild, or if one of the uv commands used to prepare the workspace fails.
    """

    # Debug
    assert isinstance(target_directory, (str, type(None))), "Argument 'target_directory' must be a string or None"
    assert isinstance(pyrat_requirement, str), "Argument 'pyrat_requirement' must be a string"

    # Warn about a uv too old to understand the configuration we write, rather than let it report an unknown field on every command
    _warn_if_uv_is_too_old()

    # Repair the current directory when it is already a workspace, rather than creating a new workspace inside it
    if target_directory is None:
        target_directory = "." if _is_pyrat_workspace(os.getcwd()) else DEFAULT_WORKSPACE_DIRECTORY

    # Check what already exists, as we do not want to overwrite the work of the student
    # A directory is taken for an existing workspace once it is a uv project, so that an empty directory still receives the programs to start with
    target_workspace = os.path.abspath(target_directory)
    existing_files = set(os.listdir(target_workspace)) if os.path.isdir(target_workspace) else set()
    workspace_existed = "pyproject.toml" in existing_files

    # Stop on a description of the project that cannot be read, rather than write into a file we do not understand and let uv complain about it much later
    if workspace_existed:
        _check_pyproject_file(target_workspace)

    # Refuse to create a workspace inside another one, as nesting uv projects makes uv reject every command in both of them
    # This happens when "pyrat-init" is given the package directory of a workspace, for instance by following instructions written for an older version
    if not workspace_existed:
        enclosing_workspace = _enclosing_workspace(target_workspace)
        if enclosing_workspace is not None:
            raise PyRatException(f"Directory {target_workspace} is inside the PyRat workspace {enclosing_workspace} -- Please run 'pyrat-init' from {enclosing_workspace} to repair that workspace, or choose a directory outside it to create a new one")

    # Make the target directory a uv project if not already the case
    # We ask uv for a standalone project, so that it never registers the workspace as a member of a uv project that happens to contain it
    if not workspace_existed:
        _run_uv(["init", "--no-package", "--no-workspace", "--vcs", "git", "--python", PYTHON_VERSION, target_workspace])
        _set_workspace_description(target_workspace, WORKSPACE_DESCRIPTION)
        print(f"Workspace initialized as a uv project using Python {PYTHON_VERSION}", file=sys.stderr)
        _warn_if_no_repository_of_its_own(target_workspace)

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
        for repair in _repair_uv_configuration(target_workspace):
            print(repair, file=sys.stderr)

    # Make the workspace installable, so that its package becomes available in its virtual environment
    # This is what allows games to import players, as in "from pyrat_workspace.players.random1 import Random1"
    if _add_build_configuration(target_workspace):
        print("Workspace configured to be installed in its virtual environment", file=sys.stderr)

    # Make sure the workspace asks uv for relocatable virtual environments, as workspaces created before PyRat declared it do not
    # This is what lets a plain "uv sync" rebuild an environment that keeps working when the workspace is renamed or moved
    if _add_relocatable_feature(target_workspace):
        print("Workspace configured to be given relocatable virtual environments", file=sys.stderr)

    # Give the workspace a brand new relocatable virtual environment, so that renaming or moving it does not break its commands
    # Nothing is lost by replacing the one that may be there, as a workspace describes everything it needs in its "pyproject.toml" file
    _prepare_virtual_environment(target_workspace)
    print("Clean relocatable virtual environment created for the workspace", file=sys.stderr)

    # Add PyRat to the dependencies of the workspace
    # This also installs in the virtual environment the workspace itself, and everything else the workspace declares
    # The virtual environment was replaced just above, so a failure here leaves the workspace without one, and the student has to be told how to get it back
    try:
        _run_uv(["add", pyrat_requirement], cwd=target_workspace)
    except PyRatException as error:
        raise PyRatException(f"{error}\nYour workspace was left without a virtual environment -- Please run 'uv sync' from {target_workspace} once the problem above is solved")
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

def _warn_if_no_repository_of_its_own ( target_workspace: str
                                      ) ->                None:

    """
    Warns the student when the workspace we just created did not receive a Git repository of its own.
    uv creates one for a new project, but silently does nothing when the directory it creates is already inside a repository.
    Every Git command the student then runs from the workspace applies to the repository that contains it, which is rarely what they want, and which nothing in the workspace shows.
    We only warn, as creating a repository inside another one is a decision that belongs to the student.

    Args:
        target_workspace: The directory of the workspace.
    """

    # Debug
    assert isinstance(target_workspace, str), "Argument 'target_workspace' must be a string"

    # Nothing to say when the workspace has a repository of its own
    if os.path.exists(os.path.join(target_workspace, ".git")):
        return

    # Explain where the commits of the student would go, and how to give the workspace a repository of its own
    enclosing_repository = _enclosing_repository(target_workspace)
    if enclosing_repository is None:
        print(f"Warning: no Git repository was created for this workspace -- Please run 'git init' from {target_workspace} if you want to version your programs", file=sys.stderr)
    else:
        print(f"Warning: no Git repository was created for this workspace, as it is inside the repository {enclosing_repository}", file=sys.stderr)
        print(f"Warning: the commits you make from the workspace would go to that repository -- Please run 'git init' from {target_workspace} to give the workspace a repository of its own", file=sys.stderr)

##########################################################################################

def _enclosing_repository ( directory: str
                          ) ->         str | None:

    """
    Looks for a Git repository among the directories that contain the given one.
    The directory itself is not examined, as we are asking what the workspace ended up inside of.

    Args:
        directory: The directory to examine.

    Returns:
        The directory of the repository that contains it, or ``None`` if there is none.
    """

    # Debug
    assert isinstance(directory, str), "Argument 'directory' must be a string"

    # Climb toward the root of the filesystem, stopping at the first repository found
    # The Git directory is not always a directory, as it is a file in a worktree or a submodule, hence the test on its mere existence
    current_directory = os.path.dirname(os.path.abspath(directory))
    while True:
        if os.path.exists(os.path.join(current_directory, ".git")):
            return current_directory
        parent_directory = os.path.dirname(current_directory)
        if parent_directory == current_directory:
            return None
        current_directory = parent_directory

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
        f.write(("" if contents.endswith("\n") else "\n") + BUILD_CONFIGURATION.format(package=WORKSPACE_PACKAGE_NAME, relocatable_feature=RELOCATABLE_FEATURE))
    return True

##########################################################################################

def _add_relocatable_feature ( target_workspace: str
                             ) ->                bool:

    """
    Makes the ``pyproject.toml`` file of a workspace ask uv for relocatable virtual environments.
    uv writes an environment that records the absolute path it was created for, unless this feature is declared, and such an environment stops working as soon as the workspace is renamed or moved.
    Declaring it in the workspace, rather than passing an option to the command that creates the environment, is what makes a plain ``uv sync`` produce an environment that can be moved around.
    Workspaces created before PyRat declared it receive it here, which is what the repair of a workspace is for.
    Nothing is written if the workspace already lists features of its own, so that a configuration the student wrote is preserved.

    Args:
        target_workspace: The directory of the workspace.

    Returns:
        ``True`` if the feature was added, ``False`` if it was already there or if the file declares features of its own.
    """

    # Debug
    assert isinstance(target_workspace, str), "Argument 'target_workspace' must be a string"

    # Do nothing if the workspace already says something about the features it wants
    pyproject_file = os.path.join(target_workspace, "pyproject.toml")
    with open(pyproject_file, "r", encoding="utf-8") as f:
        contents = f.read()
    try:
        uv_configuration = tomllib.loads(contents).get("tool", {}).get("uv", {})
    except tomllib.TOMLDecodeError:
        return False
    if not isinstance(uv_configuration, dict) or "preview-features" in uv_configuration:
        return False

    # Write the setting in the uv section of the workspace, creating that section if there is none
    setting = f'preview-features = ["{RELOCATABLE_FEATURE}"]'
    if "[tool.uv]" in contents:
        repaired_contents = contents.replace("[tool.uv]", "[tool.uv]\n" + setting, 1)
    else:
        repaired_contents = contents.rstrip("\n") + "\n\n[tool.uv]\n" + setting + "\n"

    # Write the result back, unless we made something uv can no longer read
    try:
        tomllib.loads(repaired_contents)
    except tomllib.TOMLDecodeError:
        return False
    with open(pyproject_file, "w", encoding="utf-8") as f:
        f.write(repaired_contents)
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
    Tells whether a directory is the root of a PyRat workspace, rather than a directory in which one should be created.
    A workspace is normally recognized by its ``pyproject.toml`` file declaring PyRat among its dependencies, which is what :func:`init_workspace` writes in it.
    A second trace is accepted, the package of programs that a workspace is built around, so that a workspace whose ``pyproject.toml`` file was emptied, damaged or lost is recognized all the same.
    Recognizing it is what makes :func:`init_workspace` repair the workspace instead of creating a new one inside it, which would nest two uv projects.

    Args:
        directory: The directory to examine.

    Returns:
        ``True`` if the directory is a PyRat workspace, ``False`` otherwise.
    """

    # Debug
    assert isinstance(directory, str), "Argument 'directory' must be a string"

    # A workspace is a project that depends on PyRat
    # A description we cannot make sense of is exactly the kind of damage we want to repair, so we keep looking rather than give up here
    pyproject_file = os.path.join(directory, "pyproject.toml")
    if os.path.isfile(pyproject_file):
        try:
            with open(pyproject_file, "rb") as f:
                contents = tomllib.load(f)
        except (OSError, tomllib.TOMLDecodeError):
            contents = {}
        project = contents.get("project")
        dependencies = project.get("dependencies", []) if isinstance(project, dict) else []
        if any(isinstance(dependency, str) and _requirement_name(dependency) == PYRAT_REQUIREMENT for dependency in dependencies):
            return True

    # A workspace is also recognized by the package of programs it contains, which survives the loss of the description of the project
    # That package is a plain directory of programs: a directory of the same name that is a project of its own is a workspace sitting next to us, not the one we are in
    package_directory = os.path.join(directory, WORKSPACE_PACKAGE_NAME)
    return os.path.isdir(package_directory) and not os.path.isfile(os.path.join(package_directory, "pyproject.toml"))

##########################################################################################

def _check_pyproject_file ( target_workspace: str
                          ) ->                None:

    """
    Makes sure the description of the project of an existing workspace can still be read.
    Every step that follows either writes into that file or asks uv to read it, so going on would bury the real problem under a less helpful error.
    We never rewrite the file ourselves, as this is where the student declares the libraries they added to their workspace, and we would lose them.

    Args:
        target_workspace: The directory of the workspace.

    Raises:
        PyRatException: If the ``pyproject.toml`` file of the workspace exists but cannot be read.
    """

    # Debug
    assert isinstance(target_workspace, str), "Argument 'target_workspace' must be a string"

    # Read the file, and explain what to do rather than write into something we do not understand
    pyproject_file = os.path.join(target_workspace, "pyproject.toml")
    if not os.path.isfile(pyproject_file):
        return
    try:
        with open(pyproject_file, "rb") as f:
            tomllib.load(f)
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise PyRatException(f"File {pyproject_file} cannot be read ({error}) -- Please correct it, or delete it and run 'pyrat-init' again to have a new one written for you")

##########################################################################################

def _repair_uv_configuration ( target_workspace: str
                             ) ->                list[str]:

    """
    Removes from an existing workspace the uv elements that have no reason to be there, and that keep uv from working.
    They all come from a ``uv init`` run by mistake in the package directory of a workspace, which turns that directory into a second project and declares it a member of the workspace.
    uv then sees two projects with the same name and refuses every command, in a way that no amount of reinstalling can fix, as the problem is in the files rather than in the virtual environment.
    Only elements that :func:`init_workspace` never writes are removed, so the programs of the student, and any configuration they added themselves, are left untouched.

    Args:
        target_workspace: The directory of the workspace.

    Returns:
        A description of each repair made, to be reported to the student, empty if there was nothing to repair.
    """

    # Debug
    assert isinstance(target_workspace, str), "Argument 'target_workspace' must be a string"

    # Remove the declaration that makes the workspace a uv workspace with members, which PyRat never writes
    repairs = []
    if _remove_workspace_members(os.path.join(target_workspace, "pyproject.toml")):
        repairs.append("Removed from 'pyproject.toml' the uv workspace members, which a PyRat workspace does not use")

    # Remove the project a "uv init" may have created in the package directory, as uv would work on it instead of the workspace
    package_directory = os.path.join(target_workspace, WORKSPACE_PACKAGE_NAME)
    stray_pyproject_file = os.path.join(package_directory, "pyproject.toml")
    if os.path.isfile(stray_pyproject_file):
        os.remove(stray_pyproject_file)
        repairs.append(f"Removed the 'pyproject.toml' file found in {WORKSPACE_PACKAGE_NAME}, as the project is the workspace itself")
    stray_venv_directory = os.path.join(package_directory, VENV_DIRECTORY_NAME)
    if os.path.isdir(stray_venv_directory) and not _runs_from_virtual_environment(stray_venv_directory):
        shutil.rmtree(stray_venv_directory, ignore_errors=True)
        repairs.append(f"Removed the '{VENV_DIRECTORY_NAME}' directory found in {WORKSPACE_PACKAGE_NAME}, as the workspace has its own")

    # Done
    return repairs

##########################################################################################

def _remove_workspace_members ( pyproject_file: str
                              ) ->              bool:

    """
    Removes the ``[tool.uv.workspace]`` section from the ``pyproject.toml`` file of a workspace.
    That section tells uv that the project gathers several others, which a PyRat workspace never does; uv adds it on its own when a project is created inside another one.
    The file is rewritten only if it can still be read afterwards, so that a file we did not understand is left as it is rather than damaged further.

    Args:
        pyproject_file: The ``pyproject.toml`` file of a workspace.

    Returns:
        ``True`` if the section was removed, ``False`` if there was none.
    """

    # Debug
    assert isinstance(pyproject_file, str), "Argument 'pyproject_file' must be a string"

    # Copy the file, leaving out the lines of the section and of the subsections it may have
    with open(pyproject_file, "r", encoding="utf-8") as f:
        contents = f.read()
    kept_lines = []
    in_removed_section = False
    for line in contents.splitlines(keepends=True):
        header = line.strip()
        if header.startswith("[") and header.endswith("]"):
            section = header.strip("[]").strip()
            in_removed_section = section == "tool.uv.workspace" or section.startswith("tool.uv.workspace.")
        if not in_removed_section:
            kept_lines.append(line)
    if len(kept_lines) == len(contents.splitlines()):
        return False

    # Write the result back, unless we made something uv can no longer read
    repaired_contents = "".join(kept_lines).rstrip("\n") + "\n"
    try:
        tomllib.loads(repaired_contents)
    except tomllib.TOMLDecodeError:
        return False
    with open(pyproject_file, "w", encoding="utf-8") as f:
        f.write(repaired_contents)
    return True

##########################################################################################

def _enclosing_workspace ( directory: str
                         ) ->         str | None:

    """
    Looks for a PyRat workspace among the directories that contain the given one.
    Creating a workspace inside another one would nest two uv projects, and uv then refuses to run any command in either of them.
    The directory itself is not examined, as we are asking what a new workspace created there would end up inside of.

    Args:
        directory: The directory to examine.

    Returns:
        The directory of the workspace that contains it, or ``None`` if there is none.
    """

    # Debug
    assert isinstance(directory, str), "Argument 'directory' must be a string"

    # Climb toward the root of the filesystem, stopping at the first workspace found
    current_directory = os.path.dirname(os.path.abspath(directory))
    while True:
        if _is_pyrat_workspace(current_directory):
            return current_directory
        parent_directory = os.path.dirname(current_directory)
        if parent_directory == current_directory:
            return None
        current_directory = parent_directory

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
