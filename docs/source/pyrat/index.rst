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

The packages of the library
---------------------------

The classes of the library are grouped in four subpackages, which also appear as gray frames in the diagram above.
Each one has its own page, listing the classes it contains.

.. grid:: 1 1 2 2
   :gutter: 3

   .. grid-item-card:: ``game``
      :link: game/index
      :link-type: doc

      What runs a game: the class you instantiate to start one, what your player is given at each turn, the constants you pass around, and the exception raised when a game cannot go on.

      +++
      ``Game``, ``GameState``, ``enums``, ``PyRatException``.

   .. grid-item-card:: ``players``
      :link: players/index
      :link-type: doc

      What a character in a game is: the class your own programs inherit from, and one ready-made player.

      +++
      ``Player``, ``FixedPlayer``.

   .. grid-item-card:: ``mazes``
      :link: mazes/index
      :link-type: doc

      The place a game is played in: the graph a maze is built upon, the mazes you describe yourself, and the ones PyRat generates at random.

      +++
      ``Maze``, ``Graph``, and five kinds of maze.

   .. grid-item-card:: ``rendering``
      :link: rendering/index
      :link-type: doc

      What shows a game while it is played, in a window or directly in your terminal.

      +++
      ``RenderingEngine`` and its two implementations.

.. toctree::
   :hidden:
   :maxdepth: 2

   game/index
   players/index
   mazes/index
   rendering/index
