Install PyRat
=============

This section provides instructions on how to install the PyRat library and set up your workspace.
This is essential to start developing games using the PyRat API.

.. note::

   You can also find these installation instructions in the `README <https://github.com/BastienPasdeloup/PyRat>`_ file on the GitHub repository.

In short
--------

If you are in a hurry, and already have `uv <https://docs.astral.sh/uv>`_ installed, this is the whole installation:

.. code-block:: shell

   uvx --from pyrat-game pyrat-init
   cd pyrat_workspace
   uv run games/sample_game.py

The rest of this page explains each of these steps.

Prerequisites
-------------

- This installation procedure assumes that you have basic knowledge about shell manipulation.

- PyRat uses `uv <https://docs.astral.sh/uv>`_ to manage Python and the libraries it needs.
  You do not need to install Python yourself: uv takes care of it, and PyRat workspaces are configured to use Python 3.13 (Python 3.12 is also supported).

- Finally, we will test PyRat installation using Visual Studio Code (VSCode), as this is the main tool we use in the associated course.
  Please make sure it is already installed, or install it from the `official website <https://code.visualstudio.com>`_.
  Note that you can use a different tool if you want, but we just provide indications for that one here.

Step 1 -- Install uv
--------------------

If uv is not installed on your machine yet, install it as follows.

.. tab-set::
   :sync-group: os

   .. tab-item:: Linux
      :sync: linux

      .. code-block:: shell

         curl -LsSf https://astral.sh/uv/install.sh | sh

   .. tab-item:: MacOS
      :sync: macos

      .. code-block:: shell

         curl -LsSf https://astral.sh/uv/install.sh | sh

   .. tab-item:: Windows (PowerShell)
      :sync: windows

      .. code-block:: powershell

         powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

Other installation methods are described in the `uv documentation <https://docs.astral.sh/uv/getting-started/installation>`_.

.. important::

   Close and reopen your terminal after installing uv, otherwise the ``uv`` command will not be found.
   You can then check that everything went well by running ``uv --version``.

Step 2 -- Setup your PyRat workspace
------------------------------------

We are now going to create a workspace for PyRat.
This is a directory that contains minimal working examples to get started, and in which PyRat is installed.

1. Open a terminal, and navigate (use the ``cd`` command) to the directory where you want to create your PyRat workspace.

2. Run the following command, which is the same on all systems:

   .. code-block:: shell

      uvx --from pyrat-game pyrat-init

You should see something like this:

.. code-block:: text

   Workspace created in /path/to/pyrat_workspace, as a uv project using Python >=3.12,<3.14
   Git repository created for the workspace
   Using CPython 3.13.13
   Creating virtual environment at: .venv
   Resolved 20 packages in 178ms
   Installed 19 packages in 45ms
   Virtual environment created, with PyRat installed in it
   Your workspace is ready! You can now start coding your players and run games.
   To run a game, go to the workspace using 'cd pyrat_workspace', then use for instance 'uv run games/sample_game.py'.

You should have a new directory called ``pyrat_workspace`` in the directory where you ran the command.

.. tip::

   If you prefer another name, pass it to the command, as in ``uvx --from pyrat-game pyrat-init my_project``.

Here is what this directory contains:

.. code-block:: text

   pyrat_workspace
   |_ games                   # The scripts that start a game
   |_ players                 # The programs that control a character
   |_ .venv                   # The virtual environment of the workspace, created by uv
   |_ pyproject.toml          # The description of your project and of the libraries it needs
   |_ uv.lock                 # The exact versions of the installed libraries
   |_ README.md               # A description of the workspace
   |_ .gitignore              # The files that Git should ignore

.. important::

   The command installs your workspace in its own virtual environment, which adds it to the directories Python imports from.
   This is what allows a script in ``games`` to import a player from ``players``, as in ``from players.random1 import Random1``.
   Any directory you add to your workspace is importable the same way, with nothing to declare.

   The location of your workspace is recorded twice: once by uv, as for any installed project, and once by a file PyRat installs in your virtual environment, which finds your workspace from that environment rather than writing its path down.
   The second one is what lets you rename or move your workspace with no command to run afterwards.
   Neither of them puts anything in your workspace, which holds nothing but your programs and the files uv needs.

Step 3 -- Check your installation
---------------------------------

Now, we are going to verify that PyRat works properly.

.. tab-set::

   .. tab-item:: From a terminal

      1. Open a terminal, and navigate to your workspace using ``cd pyrat_workspace``.
      2. Run the sample game:

         .. code-block:: shell

            uv run games/sample_game.py

   .. tab-item:: From VSCode

      1. Open VSCode, and add your ``pyrat_workspace`` directory in your VSCode workspace.
      2. Open the file ``sample_game.py`` in directory ``games/``.
      3. Make sure VSCode is using the interpreter located in the ``.venv`` directory of your workspace.
      4. Run ``sample_game.py``.

In both cases, you should see something like this:

.. image:: _static/pyrat_interface.png

.. card:: What now?

   Have a look at the :doc:`Quick Overview <overview>` to understand what you are seeing, then follow :doc:`The Random Programs <tutorials/the_random_programs>` to write your first player.

Add other libraries to your workspace
-------------------------------------

Your workspace is a uv project, so you can add any library you need to it.
To do so, run ``uv add`` from your workspace:

.. code-block:: shell

   uv add numpy

The library is then available in your players and games, with no need to activate anything.

Rebuild your workspace
----------------------

Your workspace describes everything it needs in its ``pyproject.toml`` and ``uv.lock`` files, so it can always be rebuilt.
Run this from the workspace, for instance after cloning it on another machine, or if one of its libraries goes missing:

.. code-block:: shell

   uv sync

This installs again everything your workspace declares, in a virtual environment created for your machine.

.. note::

   Renaming or moving your workspace needs nothing.
   Your workspace is found from the virtual environment it contains, so your programs keep importing each other wherever the workspace is.

Troubleshooting
---------------

.. dropdown:: A game cannot import one of my players
   :icon: alert

   Your workspace has no virtual environment yet, which is the case when it was just cloned from a Git repository, as a ``.venv`` directory is never versioned.

   Run ``uv sync`` from your workspace, as described in `Rebuild your workspace`_.

   Check also that you are running your program with the interpreter of your workspace, which is the one in its ``.venv`` directory.
   In VSCode, this is the interpreter you select for the directory you opened.

.. dropdown:: The ``uv`` command is not found
   :icon: alert

   Either uv is not installed (see Step 1), or your terminal was opened before installing it.
   Close and reopen your terminal, then try ``uv --version`` again.

.. dropdown:: Something else goes wrong
   :icon: question

   - Please check the existing `GitHub issues <https://github.com/BastienPasdeloup/PyRat/issues>`_ first.

   - If the problem persists, you can add an issue of your own.

   - For students at IMT Atlantique, you can also ask your questions on the `Discord server <https://discord.gg/eMnFArZ8ht>`_ of the course.

   - Finally, you can contact `Bastien Pasdeloup <mailto:bastien.pasdeloup@imt-atlantique.fr>`_ directly.
