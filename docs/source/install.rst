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

   Initialized project `pyrat-workspace` at `/path/to/pyrat_workspace`
   Workspace initialized as a uv project using Python >=3.12,<3.14
   Workspace created in /path/to/pyrat_workspace
   Using CPython 3.13.13
   Creating virtual environment at: .venv
   Resolved 19 packages in 132ms
   Installed 18 packages in 48ms
   PyRat added to the dependencies of the workspace
   Workspace added to Python path
   Your workspace is ready! You can now start coding your players and run games.
   To run a game, go to the workspace using 'cd pyrat_workspace', then use for instance 'uv run games/sample_game.py'.

You should have a new directory called ``pyrat_workspace`` in the directory where you ran the command.

.. tip::

   If you prefer another name, pass it to the command, as in ``uvx --from pyrat-game pyrat-init my_workspace``.

Here is what this directory contains:

.. code-block:: text

   pyrat_workspace
   |_ games            # The scripts that start a game
   |_ players          # The programs that control a character
   |_ .venv            # The virtual environment of the workspace, created by uv
   |_ pyproject.toml   # The description of your project and of the libraries it needs
   |_ uv.lock          # The exact versions of the installed libraries
   |_ .python-version  # The Python version used by your project
   |_ README.md        # A description of the workspace
   |_ .gitignore       # The files that Git should ignore

.. important::

   The command registers the path of your workspace in its virtual environment.
   This is what allows a script in ``games`` to import a player from ``players``.
   The path is registered relatively to the ``.venv`` directory, so you can move or rename your workspace later on without breaking anything.
   If you get your workspace from a Git repository, or if you delete its ``.venv`` directory, just run the same command again on that directory to recreate it.

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
      2. Open the file ``sample_game.py`` in directory ``pyrat_workspace/games/``.
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

Troubleshooting
---------------

.. dropdown:: A script in ``games`` cannot import a player from ``players``
   :icon: alert

   The path of your workspace is no longer registered in its virtual environment.
   This happens when the workspace comes with no ``.venv`` directory, typically when it is cloned from a Git repository.

   Run ``uvx --from pyrat-game pyrat-init`` again on that directory.
   It does not touch your files: it only recreates the ``.venv`` and registers the path again.

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
