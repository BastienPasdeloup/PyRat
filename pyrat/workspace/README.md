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

- `players/` contains the programs that control a character in a game. \
  A few random players are provided as examples, as well as a `TemplatePlayer.py` file to start your own.

- `games/` contains the scripts that create a game and make players compete in it. \
  Start with `sample_game.py` to check that everything works.

- `pyproject.toml`, `.python-version` and `uv.lock` are the files used by uv to describe your project. \
  They are updated by uv, you usually do not need to edit them by hand.

- `.venv/` is the virtual environment of your workspace, created by uv. \
  This is where PyRat and the other libraries you add are installed.

- `.gitignore` lists the files that Git should not version, such as `.venv/` and `__pycache__/`. \
  Your workspace is thus ready to be put under version control.

# Run a game

From this directory, run a game as follows:

```shell
uv run games/sample_game.py
```

Note that uv installs what is missing before running the script, so you do not need to activate the virtual environment yourself.

If you prefer to run your games from Visual Studio Code, open this directory in VSCode, and select the interpreter located in the `.venv` directory of this workspace.

# Add a library

If you need a library that is not installed yet, add it to your workspace as follows (here with `numpy` as an example):

```shell
uv add numpy
```

# More information

- The PyRat documentation is available at [https://bastienpasdeloup.github.io/PyRat](https://bastienpasdeloup.github.io/PyRat).

- The course is available at [https://hub.imt-atlantique.fr/ueinfo-fise1a](https://hub.imt-atlantique.fr/ueinfo-fise1a).

<!-- ################################################################################# -->
<!-- ################################################################################# -->
