PyRat API
=========

This section gives the documentation for functions and classes in the PyRat library.
All modules below are part of the PyRat library and can be used to create and manipulate mazes, players, etc.
To use any of them, you can import them as follows: ``from pyrat import <module_name>``.

.. code-block:: python

    # A typical import line in one of your programs
    from pyrat import Game, Player, Action, GameState, Maze

Running a game
--------------

.. grid:: 1 1 3 3
   :gutter: 2

   .. grid-item-card:: :doc:`Game`

      The central class: it builds the maze, registers the players, runs the turns and returns the statistics.

   .. grid-item-card:: :doc:`GameState`

      The snapshot your player receives at each turn: scores, locations, remaining cheese, mud, turn number.

   .. grid-item-card:: :doc:`enums`

      All the constants you pass around, such as ``Action``, ``GameMode``, ``RenderMode`` and ``PlayerSkin``.

Writing a player
----------------

.. grid:: 1 1 2 2
   :gutter: 2

   .. grid-item-card:: :doc:`Player`

      The class your own players inherit from, with the ``preprocessing()``, ``turn()`` and ``postprocessing()`` methods.

   .. grid-item-card:: :doc:`FixedPlayer`

      A player that replays a predefined list of actions, used in particular by the game replays saved by PyRat.

Describing a maze
-----------------

.. grid:: 1 1 3 3
   :gutter: 2

   .. grid-item-card:: :doc:`Maze`

      The base class of all mazes, with the methods shared by every maze.

   .. grid-item-card:: :doc:`Graph`

      The graph structure a maze is built upon, useful when you write your own path-finding code.

   .. grid-item-card:: :doc:`MazeFromDict`

      A maze described explicitly by a dictionary, for instance one produced by the :doc:`Maze Builder <../maze_builder>`.

   .. grid-item-card:: :doc:`MazeFromMatrix`

      A maze described by an adjacency matrix, handy when you generate mazes with ``numpy`` or ``torch``.

   .. grid-item-card:: :doc:`RandomMaze`

      The base class of the randomly generated mazes.

   .. grid-item-card:: :doc:`UniformHolesRandomMaze`

      A random maze whose holes are spread uniformly.

.. grid:: 1 1 2 2
   :gutter: 2

   .. grid-item-card:: :doc:`BigHolesRandomMaze`

      A random maze whose holes are grouped into large areas.

   .. grid-item-card:: :doc:`HolesOnSideRandomMaze`

      A random maze whose holes are pushed towards the sides.

Rendering
---------

.. grid:: 1 1 3 3
   :gutter: 2

   .. grid-item-card:: :doc:`RenderingEngine`

      The base class of all rendering engines.

   .. grid-item-card:: :doc:`PygameRenderingEngine`

      The graphical interface, shown in a window.

   .. grid-item-card:: :doc:`ShellRenderingEngine`

      The text interface, drawn directly in your terminal.

Utilities
---------

.. grid:: 1 1 1 1
   :gutter: 2

   .. grid-item-card:: :doc:`utils`

      Helper functions, in particular ``init_workspace()``, which creates your workspace.

.. toctree::
   :hidden:
   :maxdepth: 1

   BigHolesRandomMaze
   FixedPlayer
   Game
   GameState
   Graph
   HolesOnSideRandomMaze
   Maze
   MazeFromDict
   MazeFromMatrix
   Player
   PygameRenderingEngine
   RandomMaze
   RenderingEngine
   ShellRenderingEngine
   UniformHolesRandomMaze
   enums
   utils
