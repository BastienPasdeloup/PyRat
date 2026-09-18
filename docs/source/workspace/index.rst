Workspace API
=============

PyRat comes with a workspace that you should use to start working on your games.
It is created with the ``pyrat-init`` command (or the equivalent ``pyrat.init_workspace()`` function) that we ask you to run in the :doc:`installation instructions <../install>`.
This workspace contains two directories: one to store your games and one to store your players.
You can later add more directories if you want to organize your workspace differently.
It also contains the files used by `uv <https://docs.astral.sh/uv>`_ to describe the Python version and the libraries of your project, which you usually do not need to edit by hand.

.. toctree::
   :maxdepth: 1

   games/index
   players/index