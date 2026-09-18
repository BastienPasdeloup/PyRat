Workspace API
=============

PyRat comes with a workspace that you should use to start working on your games.
It is created with the ``pyrat-init`` command that we ask you to run in the :doc:`installation instructions <../install>`.

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
Finally, it contains a ``.gitignore`` file listing what Git should not version (the virtual environment, temporary files, etc.), so that it is ready to be put under version control.

.. tip::

   The programs documented in this section are the ones created in your workspace.
   Reading their source code, linked on each page, is the fastest way to understand how a PyRat program is written.

.. _workspace-diagram:

The big picture
---------------

The diagram below shows the programs of your workspace, and how they relate to the PyRat library: the players inherit from ``Player``, and the game scripts create a ``Game`` in which they make some of these players compete, using the enumerations of the library to choose their skin and their starting location.

.. container:: class-diagram only-light

   .. raw:: html
      :file: ../_static/workspace_diagram_light_inline.svg

.. container:: class-diagram only-dark

   .. raw:: html
      :file: ../_static/workspace_diagram_dark_inline.svg

.. container:: only-light

   .. tip::

      The diagram is interactive: hover it to magnify the area under the cursor, click on the name of a class or of a script to open its documentation page, or on one of the attributes or methods of a class to jump directly to its description.
      You can also :raw-html:`<a class="reference external" href="../_static/workspace_diagram_light.svg" target="_blank" rel="noopener">open the diagram at full size</a>` in a new tab.
      The notation is the one of the :ref:`class diagram of the library <class-diagram>`, which explains how to read it.
.. container:: only-dark

   .. tip::

      The diagram is interactive: hover it to magnify the area under the cursor, click on the name of a class or of a script to open its documentation page, or on one of the attributes or methods of a class to jump directly to its description.
      You can also :raw-html:`<a class="reference external" href="../_static/workspace_diagram_dark.svg" target="_blank" rel="noopener">open the diagram at full size</a>` in a new tab.
      The notation is the one of the :ref:`class diagram of the library <class-diagram>`, which explains how to read it.
.. toctree::
   :hidden:
   :maxdepth: 1

   games/index
   players/index
