<!-- ################################################################################# -->
<!-- ###################################### INFO ##################################### -->
<!-- ################################################################################# -->

<!-- This file is provided as a starting point by the PyRat library. -->
<!-- It describes the contents of a PyRat workspace, and how to work in it. -->

<!-- ################################################################################# -->
<!-- #################################### CONTENTS ################################### -->
<!-- ################################################################################# -->

# PyRat workspace

This directory is your PyRat workspace. \
It is a [uv](https://docs.astral.sh/uv) project, which means that uv takes care of the Python version and of the libraries you need.

# Contents of the workspace

- `pyrat_workspace/` contains your programs. \
  It is installed as a package in the virtual environment of your workspace, which is what lets your programs import each other.

- `pyrat_workspace/players/` contains the programs that control a character in a game. \
  A few random players are provided as examples, as well as a `template_player.py` file to start your own.

- `pyrat_workspace/games/` contains the scripts that create a game and make players compete in it. \
  Start with `sample_game.py` to check that everything works.

- Any other directory you create in `pyrat_workspace/` can be imported the same way, with nothing to declare. \
  For instance, a file `pyrat_workspace/utils/tools.py` is imported using `from pyrat_workspace.utils.tools import Tools`.

- `pyproject.toml`, `.python-version` and `uv.lock` are the files used by uv to describe your project. \
  They are updated by uv, you usually do not need to edit them by hand. \
  uv installs your workspace in its virtual environment, so the files that run are always the ones you edit.

- `.venv/` is the virtual environment of your workspace, created by uv. \
  This is where PyRat and the other libraries you add are installed.

- `.gitignore` lists the files that Git should not version, such as `.venv/` and `__pycache__/`. \
  Your workspace is thus ready to be put under version control.

# Run a game

From this directory, run a game as follows:

```shell
uv run pyrat_workspace/games/sample_game.py
```

Note that uv installs what is missing before running the script, so you do not need to activate the virtual environment yourself.

If you prefer to run your games from Visual Studio Code, open this directory in VSCode, and select the interpreter located in the `.venv` directory of this workspace.

# Add a library

If you need a library that is not installed yet, add it to your workspace as follows (here with `numpy` as an example):

```shell
uv add numpy
```

# Repair your workspace

Your workspace describes everything it needs in `pyproject.toml` and `uv.lock`, so it can always be rebuilt. \
If you rename or move it, or if one of the libraries it uses goes missing, run this from the workspace:

```shell
uv sync
```

This installs again everything your workspace declares, and makes your programs importable from wherever the workspace now is.

If that is not enough, for instance because your terminal no longer finds the right Python, rebuild the environment from scratch:

```shell
uvx --from pyrat-game pyrat-init
```

Run from a workspace, this command leaves your programs untouched. \
It replaces the `.venv` directory with a brand new one, in which everything your workspace declares is installed again.

# More information

- The PyRat documentation is available at [https://bastienpasdeloup.github.io/PyRat](https://bastienpasdeloup.github.io/PyRat).

- The course is available at [https://hub.imt-atlantique.fr/ueinfo-fise1a](https://hub.imt-atlantique.fr/ueinfo-fise1a).

<!-- ################################################################################# -->
<!-- ################################################################################# -->
