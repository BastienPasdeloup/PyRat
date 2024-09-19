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

<img align="left" width="120px" src="pyrat/gui/drawings/pyrat.png" />

# PyRat

This repository contains the software used in the computer science course at IMT Atlantique.

The course contents is available at this address:<br />https://hub.imt-atlantique.fr/ueinfo-fise1a/.

# Install

### Standard installation procedure

Installation of the PyRat software can be done directly using `pip`.
Do not clone or download the repository.
Instead please follow the following instructions:

1) First, make sure that Git is installed.
    Check the instructions corresponding to your operating system [here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

2) Install the PyRat software using the following command:<br />`python -m pip install --user git+https://github.com/BastienPasdeloup/PyRat.git`

### Alternate installation procedure without installing Git

If you do not wish to install Git, you can follow these instructions instead:

1) Click on the green "<> Code" button on top of this page, and click on "Download ZIP".

2) Extract the downloaded archive and navigate (using the `cd` command if on Linux/OSX or `dir` command if on Windows) there in a terminal.
    Then, run the following command:<br />`python -m pip install .`

# Setup your workspace

Whatever installation method you chose, now follow the following instructions to prepare your PyRat workspace:

3) Open a terminal and navigate (using the `cd` command if on Linux/OSX or `dir` command if on Windows) to the directory where you want to create your PyRat workspace.

4) Then, run the following command to create a PyRat workspace in the current directory:<br />`python -c "import pyrat; pyrat.create_workspace('.')"`

5) Finally, run the following command to generate the PyRat documentation:<br />`python -c "import pyrat; pyrat.generate_documentation('pyrat_workspace')"`

# Check installation

Once installed, please head to the course website, and [follow instructions to start your first PyRat game](http://localhost:1313/ueinfo-fise1a/s5/project/session1/practical/#12-----the-pyrat-workspace).

<!-- ##################################################################################################################################################### -->
<!-- ##################################################################################################################################################### -->
