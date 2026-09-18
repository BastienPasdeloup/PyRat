Tutorials
=========

This section provides various tutorials for using the PyRat library.
These tutorials cover different use cases and help you understand how to implement your own games using the PyRat API.

Start here
----------

If you are new to PyRat, follow these tutorials in order.
Together, they take you from the players provided in your workspace to a game configured the way you want.

.. grid:: 1 1 2 2
   :gutter: 3

   .. grid-item-card:: The Random Programs
      :link: the_random_programs
      :link-type: doc

      The four example players of your workspace, from the simplest to the smartest, each one fixing a weakness of the previous one.

      +++
      The best place to start.

   .. grid-item-card:: Customizing Your Game
      :link: customizing_your_game
      :link-type: doc

      Change the maze size, the amount of mud, the number of cheese pieces, the skins of your players, and more.

      +++
      Make the game yours.

   .. grid-item-card:: Game Modes
      :link: game_modes
      :link-type: doc

      How time is shared between players, and which mode to use for debugging, for a match, or for running many games.

      +++
      Choose the right mode.

   .. grid-item-card:: Stopping a Game
      :link: stopping_a_game
      :link-type: doc

      How to interrupt a game cleanly from your own code.

      +++
      A short one.

Going further
-------------

When you are familiar with the basics, these tutorials cover more advanced needs.

.. grid:: 1 1 2 2
   :gutter: 3

   .. grid-item-card:: Building a Maze
      :link: building_a_maze
      :link-type: doc

      Describe your own maze, or generate one with the random maze algorithms provided by PyRat.

      +++
      Control the terrain.

   .. grid-item-card:: Postprocessing
      :link: postprocessing
      :link-type: doc

      Run code once the game is over, for instance to analyze what your player did.

      +++
      After the game.

.. tip::

   Looking for a specific class or function instead?
   The :doc:`PyRat API <../pyrat/index>` documents every element of the library, and the :doc:`Workspace API <../workspace/index>` documents the programs that come with your workspace.

.. toctree::
   :hidden:
   :maxdepth: 1

   the_random_programs
   customizing_your_game
   game_modes
   stopping_a_game
   building_a_maze
   postprocessing
