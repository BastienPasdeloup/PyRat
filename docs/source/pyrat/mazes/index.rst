``mazes``
=========

The ``mazes`` subpackage describes the place a game is played in.
It contains the graph structure a maze is built upon, the base class of all mazes, the mazes you describe yourself, and the ones PyRat generates at random.

.. grid:: 1 1 2 2
   :gutter: 2

   .. grid-item-card:: :doc:`Maze <../Maze>`

      The base class of all mazes, with the methods shared by every maze.

   .. grid-item-card:: :doc:`Graph <../Graph>`

      The graph structure a maze is built upon, useful when you write your own path-finding code.

   .. grid-item-card:: :doc:`MazeFromDict <../MazeFromDict>`

      A maze described explicitly by a dictionary, for instance one produced by the :doc:`Maze Builder <../../maze_builder>`.

   .. grid-item-card:: :doc:`MazeFromMatrix <../MazeFromMatrix>`

      A maze described by an adjacency matrix, handy when you generate mazes with ``numpy`` or ``torch``.

   .. grid-item-card:: :doc:`RandomMaze <../RandomMaze>`

      The base class of the randomly generated mazes.

   .. grid-item-card:: :doc:`UniformHolesRandomMaze <../UniformHolesRandomMaze>`

      A random maze whose holes are spread uniformly.

   .. grid-item-card:: :doc:`BigHolesRandomMaze <../BigHolesRandomMaze>`

      A random maze whose holes are grouped into large areas.

   .. grid-item-card:: :doc:`HolesOnSideRandomMaze <../HolesOnSideRandomMaze>`

      A random maze whose holes are pushed towards the sides.

.. toctree::
   :maxdepth: 1

   ../Maze
   ../Graph
   ../MazeFromDict
   ../MazeFromMatrix
   ../RandomMaze
   ../UniformHolesRandomMaze
   ../BigHolesRandomMaze
   ../HolesOnSideRandomMaze
