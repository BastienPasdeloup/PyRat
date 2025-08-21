<!-- ##################################################################################################################################################### -->
<!-- ######################################################################## INFO ####################################################################### -->
<!-- ##################################################################################################################################################### -->

<!--
    This file contains the public text that appears on the PyRat GitHub repository.
    It contains a short description and installation details.
-->

<!-- ##################################################################################################################################################### -->
<!-- ###################################################################### CONTENTS ##################################################################### -->
<!-- ##################################################################################################################################################### -->

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
                <p>The course contents is available at this address:<br><a rel="nofollow"></a><a href="https://hub.imt-atlantique.fr/ueinfo-fise1a" rel="nofollow">https://hub.imt-atlantique.fr/ueinfo-fise1a</a>.</p>
                <br />
                <p>The documentation is available at this address::<br><a rel="nofollow"></a><a href="https://bastienpasdeloup.github.io/PyRat" rel="nofollow">https://bastienpasdeloup.github.io/PyRat</a>.</p>
                <br />
            </td>
        </tr>
    </table>
</div>

# Prerequisites

- This installation procedure assumes that you have basic knowledge about shell manipulation.

- Also, it assumes that you have already created a virtual environment where to install PyRat.
  If not, please do this first as described in the [official documentation](https://docs.python.org/3/library/venv.html).

- Finally, we will test PyRat installation using Visual Studio Code (VSCode), as this is the main tool we use in the associated course.
  Please make sure it is already installed, or install it from the [official website](https://code.visualstudio.com).
  Note that you can use a different tool if you want, but we just provide indications for that one here.

# Install the PyRat package

Installation of the PyRat software can be done directly using `pip`. \
To do so, follow steps:
1) Open a terminal.
2) Activate your virtual environment (change `path_to_venv` to the actual path):
   - **Linux:** `source path_to_venv/bin/activate`.
   - **MacOS:** `source path_to_venv/bin/activate"`.
   - **Windows (cmd):** `path_to_venv\Scripts\activate.bat`.
   - **Windows (PowerShell):** `path_to_venv\Scripts\Activate.ps1`.
3) Install PyRat through `pip` as follows: `pip install pyrat-game`.

You should see something like this:
```text
Downloading pyrat_game-6.0.0-py3-none-any.whl (4.2 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.2/4.2 MB 9.6 MB/s eta 0:00:00
Installing collected packages: pyrat-game
Successfully installed pyrat-game-6.0.0
```

# Setup your PyRat workspace

We are now going to create a workspace for PyRat. \
This is a directory that contains minimal working examples to get started. \
To do so, follow these steps:
1) Open a terminal, and navigate (use the `cd` command) to the directory where you want to create your PyRat workspace.
2) Activate your virtual environment where PyRat is installed (see above).
3) Run the following command:
   - **Linux:** `python3 -c "import pyrat; pyrat.create_workspace('.')"`
   - **MacOS:** `python3 -c "import pyrat; pyrat.create_workspace('.')"`
   - **Windows (cmd):** `python -c "import pyrat; pyrat.create_workspace('.')"`
   - **Windows (PowerShell):** `python -c "import pyrat; pyrat.create_workspace('.')"`

You should see something like this:
```text
Workspace created in /path/to/pyrat_workspace`
Workspace added to Python path
```

# Check your installation

Now, we are going to verify that PyRat works properly. \
To do so, follow these steps:
1) Open VSCode, and add your `pyrat_workspace` directory in your VSCode workspace.
2) Open the file `sample_game.py` in directory `pyrat_workspace/games/`.
3) Make sure VSCode is using your virtual environment where PyRat is installed.
3) Run `sample_game.py`.

You should see something like this:

<img src="https://bastienpasdeloup.github.io/PyRat/_images/pyrat_interface.png" />

# Troubleshooting

- In case of a problem, please check the existing [GitHub issues](https://github.com/BastienPasdeloup/PyRat/issues) first.

- If the problem persists, you can add an issue of your own.

- For students at IMT Atlantique, you can also ask your questions on the [Discord server](https://discord.gg/eMnFArZ8ht) of the course.

- Finally, you can contact [Bastien Pasdeloup](mailto:bastien.pasdeloup@imt-atlantique.fr) directly.

<!-- ##################################################################################################################################################### -->
<!-- ##################################################################################################################################################### -->
