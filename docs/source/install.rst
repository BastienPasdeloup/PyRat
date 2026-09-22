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
   cd pyrat_project
   uv run pyrat_workspace/games/sample_game.py

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

   Initialized project `pyrat-project` at `/path/to/pyrat_project`
   Workspace initialized as a uv project using Python >=3.12,<3.14
   Workspace created in /path/to/pyrat_project
   Workspace configured to be installed in its virtual environment
   Using CPython 3.13.13
   Creating virtual environment at: .venv
   Clean relocatable virtual environment created for the workspace
   Resolved 20 packages in 178ms
   Installed 19 packages in 45ms
   PyRat added to the dependencies of the workspace
   Your workspace is ready! You can now start coding your players and run games.
   To run a game, go to the workspace using 'cd pyrat_project', then use for instance 'uv run pyrat_workspace/games/sample_game.py'.

You should have a new directory called ``pyrat_project`` in the directory where you ran the command.

.. tip::

   If you prefer another name, pass it to the command, as in ``uvx --from pyrat-game pyrat-init my_project``.

Here is what this directory contains:

.. code-block:: text

   pyrat_project
   |_ pyrat_workspace     # Your programs, installed as a package in the virtual environment
   |  |_ games            # The scripts that start a game
   |  |_ players          # The programs that control a character
   |_ .venv               # The virtual environment of the workspace, created by uv
   |_ pyproject.toml      # The description of your project and of the libraries it needs
   |_ uv.lock             # The exact versions of the installed libraries
   |_ .python-version     # The Python version used by your project
   |_ README.md           # A description of the workspace
   |_ .gitignore          # The files that Git should ignore

.. important::

   The command installs the ``pyrat_workspace`` package of your workspace in its virtual environment.
   This is what allows a script in ``pyrat_workspace/games`` to import a player from ``pyrat_workspace/players``, as in ``from pyrat_workspace.players.random1 import Random1``.
   Any directory you add in ``pyrat_workspace`` is importable the same way, with nothing to declare.
   The package is installed in editable mode, so the files that run are always the ones you edit.

Step 3 -- Check your installation
---------------------------------

Now, we are going to verify that PyRat works properly.

.. tab-set::

   .. tab-item:: From a terminal

      1. Open a terminal, and navigate to your workspace using ``cd pyrat_project``.
      2. Run the sample game:

         .. code-block:: shell

            uv run pyrat_workspace/games/sample_game.py

   .. tab-item:: From VSCode

      1. Open VSCode, and add your ``pyrat_project`` directory in your VSCode workspace.
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

Repair your workspace
---------------------

Your workspace describes everything it needs in its ``pyproject.toml`` and ``uv.lock`` files, so it can always be rebuilt.
If you rename or move it, or if one of its libraries goes missing, run this from the workspace:

.. code-block:: shell

   uv sync

This installs again everything your workspace declares, and makes your programs importable from wherever the workspace now is.

If that is not enough, run the very same command that created the workspace, from the workspace itself:

.. code-block:: shell

   uvx --from pyrat-game pyrat-init

Run from a workspace, this command does not create a new one inside it, and does not touch the programs it contains.
It replaces the ``.venv`` directory with a brand new one, in which everything the workspace declares is installed again.

.. note::

   This is also how you prepare a workspace obtained from a Git repository, as such a workspace comes with no ``.venv`` directory.

.. important::

   Run the command with ``uvx``, as shown above, and not with ``uv run pyrat-init``.
   The latter uses the ``pyrat-init`` command installed in the very virtual environment that has to be replaced, and the command refuses to remove the environment it runs from.

Troubleshooting
---------------

.. dropdown:: A game cannot import one of my players
   :icon: alert

   The ``pyrat_workspace`` package of your workspace is not installed in its virtual environment any more.
   This happens when the workspace was renamed or moved, or when it comes with no ``.venv`` directory, typically when it is cloned from a Git repository.

   Run ``uv sync`` from your workspace, which installs it again where it now is.
   If the problem persists, rebuild the environment as described in `Repair your workspace`_.

.. dropdown:: My terminal no longer finds the right Python after moving my workspace
   :icon: alert

   The scripts that activate a virtual environment remember where that environment was created, unless it was made relocatable.
   PyRat asks uv for a relocatable one, but uv writes a regular one whenever it has to create the environment itself, for instance after you deleted it.

   Rebuild the environment as described in `Repair your workspace`_, which makes it relocatable again.

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
