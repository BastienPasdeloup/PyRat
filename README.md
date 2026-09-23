<!-- ################################################################################# -->
<!-- ###################################### INFO ##################################### -->
<!-- ################################################################################# -->

<!-- This file contains the public text that appears on the PyRat GitHub repository. -->
<!-- It contains a short description and installation details. -->

<!-- ################################################################################# -->
<!-- #################################### CONTENTS ################################### -->
<!-- ################################################################################# -->

<div align="center">
    <table>
        <tr>
            <td align="center">
                <img height="350px" src="https://raw.githubusercontent.com/BastienPasdeloup/PyRat/refs/heads/master/pyrat/gui/drawings/pyrat.png">
            </td>
            <td align="center">
                <h1>PyRat</h1>
                <br />
                <p>This repository contains the software used in the<br>computer science course at IMT Atlantique.</p>
                <br />
                <p>The course is available at this address:<br><a rel="nofollow"></a><a href="https://hub.imt-atlantique.fr/ueinfo-fise1a" rel="nofollow">https://hub.imt-atlantique.fr/ueinfo-fise1a</a>.</p>
                <br />
                <p>The documentation is available at this address:<br><a rel="nofollow"></a><a href="https://bastienpasdeloup.github.io/PyRat" rel="nofollow">https://bastienpasdeloup.github.io/PyRat</a>.</p>
                <br />
            </td>
        </tr>
    </table>
</div>

# Prerequisites

- This installation procedure assumes that you have basic knowledge about shell manipulation.

- PyRat uses [uv](https://docs.astral.sh/uv) to manage Python and the libraries it needs. \
  You do not need to install Python yourself: uv takes care of it, and PyRat workspaces are configured to use Python 3.13 (Python 3.12 is also supported).

- Finally, we will test PyRat installation using Visual Studio Code (VSCode), as this is the main tool we use in the associated course.
  Please make sure it is already installed, or install it from the [official website](https://code.visualstudio.com).
  Note that you can use a different tool if you want, but we just provide indications for that one here.

# Install uv

If uv is not installed on your machine yet, install it as follows:
- **Linux:** `curl -LsSf https://astral.sh/uv/install.sh | sh`.
- **MacOS:** `curl -LsSf https://astral.sh/uv/install.sh | sh`.
- **Windows (PowerShell):** `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`.

Other installation methods are described in the [uv documentation](https://docs.astral.sh/uv/getting-started/installation). \
Then, close and reopen your terminal, and check that uv is available by running `uv --version`.

# Setup your PyRat workspace

We are now going to create a workspace for PyRat. \
This is a directory that contains minimal working examples to get started, and in which PyRat is installed. \
To do so, follow these steps:
1) Open a terminal, and navigate (use the `cd` command) to the directory where you want to create your PyRat workspace.
2) Run the following command (it is the same on all systems): `uvx --from pyrat-game pyrat-init`.

You should see something like this:
```text
Workspace created in /path/to/pyrat_workspace, as a uv project using Python >=3.12,<3.14
Git repository created for the workspace
Using CPython 3.13.13
Creating virtual environment at: .venv
Resolved 20 packages in 178ms
Installed 19 packages in 45ms
Virtual environment created, with PyRat installed in it
Your workspace is ready! You can now start coding your players and run games.
To run a game, go to the workspace using 'cd pyrat_workspace', then use for instance 'uv run games/sample_game.py'.
```

You should have a new directory called `pyrat_workspace` in the directory where you ran the command. \
It contains a `players` directory and a `games` directory, which is where your own programs live. \
If you prefer another name for the workspace, pass it to the command, as in `uvx --from pyrat-game pyrat-init my_project`.

# Check your installation

Now, we are going to verify that PyRat works properly. \
To do so, follow these steps:
1) Open a terminal, and navigate to your workspace using `cd pyrat_workspace`.
2) Run the sample game as follows: `uv run games/sample_game.py`.

You can also run your games from VSCode. \
To do so, follow these steps:
1) Open VSCode, and add your `pyrat_workspace` directory in your VSCode workspace.
2) Open the file `sample_game.py` in directory `games/`.
3) Make sure VSCode is using the interpreter located in the `.venv` directory of your workspace.
4) Run `sample_game.py`.

In both cases, you should see something like this:

<img src="https://bastienpasdeloup.github.io/PyRat/_images/pyrat_interface.png" />

# Add other libraries to your workspace

Your workspace is a uv project, so you can add any library you need to it. \
To do so, run `uv add` from your workspace, as in `uv add numpy`. \
The library is then available in your players and games, with no need to activate anything.

# Rebuild your workspace

A workspace describes everything it needs in its `pyproject.toml` and `uv.lock` files, so it can always be rebuilt. \
Run this from the workspace, for instance after cloning it on another machine, or if one of its libraries goes missing:

```shell
uv sync
```

This installs again everything the workspace declares, in a virtual environment created for the machine it runs on.

Renaming or moving a workspace needs nothing: its programs keep importing each other, wherever the workspace is.

# Troubleshooting

- In case of a problem, please check the existing [GitHub issues](https://github.com/BastienPasdeloup/PyRat/issues) first.

- If the problem persists, you can add an issue of your own.

- For students at IMT Atlantique, you can also ask your questions on the [Discord server](https://discord.gg/eMnFArZ8ht) of the course.

- Finally, you can contact [Bastien Pasdeloup](mailto:bastien.pasdeloup@imt-atlantique.fr) directly.

<!-- ################################################################################# -->
<!-- ################################################################################# -->
