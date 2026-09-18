PyRat API
=========

This section gives the documentation for functions and classes in the PyRat library.
All modules below are part of the PyRat library and can be used to create and manipulate mazes, players, etc.
To use any of them, you can import them as follows: ``from pyrat import <class_name>``.

.. code-block:: python

    # A typical import line in one of your programs
    from pyrat import Game, Player, Action, GameState, Maze

.. _class-diagram:

The big picture
---------------

The diagram below shows all the classes of the library, which class inherits from which, and how the game, the players, the mazes and the rendering engines fit together.
Your own players (in green) are the only classes you write: they inherit from ``Player``, receive a ``Maze`` and a ``GameState`` at each turn, and return an ``Action``.

.. container:: class-diagram only-light

   .. raw:: html
      :file: ../_static/class_diagram_light_inline.svg

.. container:: class-diagram only-dark

   .. raw:: html
      :file: ../_static/class_diagram_dark_inline.svg

.. container:: only-light

   .. tip::

      The diagram is interactive: hover it to magnify the area under the cursor, click on the name of a class to open its documentation page, or on one of its attributes or methods to jump directly to its description.
      You can also :raw-html:`<a class="reference external" href="../_static/class_diagram_light.svg" target="_blank" rel="noopener">open the diagram at full size</a>` in a new tab.
.. container:: only-dark

   .. tip::

      The diagram is interactive: hover it to magnify the area under the cursor, click on the name of a class to open its documentation page, or on one of its attributes or methods to jump directly to its description.
      You can also :raw-html:`<a class="reference external" href="../_static/class_diagram_dark.svg" target="_blank" rel="noopener">open the diagram at full size</a>` in a new tab.
.. dropdown:: How to read the diagram

   The diagram follows the conventions of `UML class diagrams <https://en.wikipedia.org/wiki/Class_diagram>`_.
   If you are not familiar with them, here is all you need to know.

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Boxes

         Each box is a class, with three compartments: its name, its attributes, and its methods.
         A name in *italics* denotes an abstract class, that cannot be instantiated directly, and an *italic* method is a method that subclasses must implement.
         Boxes marked «enumeration» list constants, that you use as ``Action.NORTH``, ``RenderMode.GUI``, etc.

      .. grid-item-card:: Visibility

         The symbol before each attribute or method tells who is meant to use it:
         ``+`` is public (you can use it), ``#`` is protected (meant for subclasses), and ``-`` is private (internal to the class).
         Methods are listed with the names of their arguments and their return type.

      .. grid-item-card:: Arrows

         - A solid line with a hollow triangle is **inheritance**: the classes below the line are subclasses of the class at the triangle.
           For instance, ``FixedPlayer`` is a ``Player``.
         - A line with a filled diamond is **composition**: the ``Game`` creates and owns its maze and its rendering engine.
         - A line with a hollow diamond is **aggregation**: the ``Game`` groups players, but you create them yourself and register them with ``add_player()``.
           The label at the far end of these lines gives the attribute of ``Game`` that holds the objects, and how many of them there are.
         - A dashed arrow is a **dependency**: the class at the tail creates, receives or returns the class at the head.

      .. grid-item-card:: Colors

         Orange boxes are the classes of the library, grouped by package in gray frames.
         Blue boxes are the enumerations.
         The green dashed box stands for the players you write, which inherit from ``Player``.
         The gray note describes internal components, that are not part of the public API.

.. dropdown:: Which class does the game create?

   Several settings of :doc:`Game <Game>` decide which concrete class is instantiated behind the scenes.
   The diagram shows all the candidates, and the table below tells which one is chosen.

   .. list-table::
      :header-rows: 1
      :widths: 28 40 32

      * - Setting of ``Game``
        - Value
        - Class created
      * - ``random_maze_algorithm``
        - ``RandomMazeAlgorithm.BIG_HOLES`` (default)
        - :doc:`BigHolesRandomMaze`
      * -
        - ``RandomMazeAlgorithm.UNIFORM_HOLES``
        - :doc:`UniformHolesRandomMaze`
      * -
        - ``RandomMazeAlgorithm.HOLES_ON_SIDE``
        - :doc:`HolesOnSideRandomMaze`
      * - ``fixed_maze``
        - A dictionary
        - :doc:`MazeFromDict`
      * -
        - A ``numpy`` array or a ``torch`` tensor
        - :doc:`MazeFromMatrix`
      * -
        - A ``Maze`` object
        - Used as is (a copy is made)
      * - ``render_mode``
        - ``RenderMode.GUI`` (default)
        - :doc:`PygameRenderingEngine`
      * -
        - ``RenderMode.ANSI`` or ``RenderMode.ASCII``
        - :doc:`ShellRenderingEngine` (with or without colors)
      * -
        - ``RenderMode.NO_RENDERING``
        - :doc:`RenderingEngine` (renders nothing)

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

Errors
------

.. grid:: 1 1 1 1
   :gutter: 2

   .. grid-item-card:: :doc:`PyRatException`

      The exception raised when a game cannot proceed, for instance because a player crashed or returned something that is not an action.

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
   PyRatException
   PygameRenderingEngine
   RandomMaze
   RenderingEngine
   ShellRenderingEngine
   UniformHolesRandomMaze
   enums
