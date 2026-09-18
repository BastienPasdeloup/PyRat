Workspace API
=============

PyRat comes with a workspace that you should use to start working on your games.
It is created with the ``pyrat-init`` command (or the equivalent ``pyrat.init_workspace()`` function) that we ask you to run in the :doc:`installation instructions <../install>`.

Your workspace is organized around two directories, documented in this section.

.. grid:: 1 1 2 2
   :gutter: 3

   .. grid-item-card:: Players
      :link: players/index
      :link-type: doc

      The programs that control a character during a game.
      A player is a class that inherits from ``Player``, and decides which action to take at each turn.

      +++
      Your workspace comes with five of them.

   .. grid-item-card:: Games
      :link: games/index
      :link-type: doc

      The scripts that set up a game and make players compete in it.
      This is what you run to actually see a game.

      +++
      Your workspace comes with two of them.

You can later add more directories if you want to organize your workspace differently.
Your workspace also contains the files used by `uv <https://docs.astral.sh/uv>`_ to describe the Python version and the libraries of your project, which you usually do not need to edit by hand.

.. tip::

   The programs documented in this section are the ones created in your workspace.
   Reading their source code, linked on each page, is the fastest way to understand how a PyRat program is written.

.. toctree::
   :hidden:
   :maxdepth: 1

   games/index
   players/index
