Building a Maze
===============

It may be convenient to build a custom maze for your game to test particular situations.
In this tutorial, we will see how to build a maze using the PyRat library.

Building a Graph
----------------

In PyRat, we manipulate several types of graphs.
The class :doc:`Graph </pyrat/Graph>` is the most generic one, allowing to represent any graph.
A graph is defined by a set of vertices and a set of edges.
Vertices are elements of interest, and edges are connections between these vertices.

To create a graph in PyRat, you need to instantiate a ``Graph`` object.
Then, you can add vertices and edges to it.

Here is an example of how to create a simple graph with three vertices and two edges:

.. code-block:: python

    # Pyrat imports
    from pyrat import Graph

    # Create a new graph
    graph = Graph()

    # Add vertices
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex("C")

    # Add edges
    graph.add_edge("A", "B", weight=12, symmetric=True)
    graph.add_edge("B", "C", weight=8, symmetric=False)

    # Show the graph
    print(graph)

Running this code produces the following output:

.. code-block:: text

    Graph object:
    |  Vertices: ['A', 'B', 'C']
    |  Adjacency matrix:
    |  |  A <-- (12) --> B
    |  |  B --- (8) --> C

This can be quite practical, as it allows you to create complex graphs with various properties.

Building a Maze
---------------

While a ``Graph`` can be very useful, this class does not guarantee that we are building a maze.
Indeed, a maze is a specific type of graph, where:

- Vertices are integers from 0 to ``width * height - 1``, where ``width`` and ``height`` are the dimensions of the maze.
  This allows to place the vertices in a 2D grid.
- Edges are connections between adjacent vertices (up, down, left, right).
- Edges are symmetric, meaning that if there is an edge from vertex A to vertex B, there is also an edge from vertex B to vertex A.
- Weights are integers, representing the cost to move from one vertex to another.

Which Class to Use?
^^^^^^^^^^^^^^^^^^^

In order to build a maze, the natural choice would be to use the :doc:`Maze </pyrat/Maze>` class, which inherits from the ``Graph`` class.
However, this class is abstract, meaning that it cannot be instantiated directly.
Indeed, it is designed to factorize codes that are common to all maze classes, without providing a specific implementation.
Note that this is also the case for the :doc:`RandomMaze </pyrat/RandomMaze>` class (which inherits from the ``Maze`` class), which groups common elements to all random mazes.


To create a maze, you can use one of the concrete classes that inherit from the ``Maze`` class.
These classes are:

- :doc:`BigHolesRandomMaze </pyrat/BigHolesRandomMaze>`: This class generates a random maze with big holes.
- :doc:`HolesOnSideRandomMaze </pyrat/HolesOnSideRandomMaze>`: This class generates a random maze with holes on the sides.
- :doc:`UniformHolesRandomMaze </pyrat/UniformHolesRandomMaze>`: This class generates a random maze with holes placed uniformly at random.
- :doc:`MazeFromDict </pyrat/MazeFromDict>`: This class generates a maze from a given dictionary ``dict[int, dict[int, int]]``.
- :doc:`MazeFromMatrix </pyrat/MazeFromMatrix>`: This class generates a maze from a given matrix ``numpy.ndarray`` or ``torch.tensor``.

The first three classes will create a random maze for you, following a specific algorithm.
The last two classes will create a maze from a given representation, that you need to provide.

Let's use ``MazeFromDict`` to create a maze from a dictionary representation.
As mentioned earlier, the dictionary should be of the form ``dict[int, dict[int, int]]``, where the first key is the vertex index (in lexicographic order).
The associated value is another dictionary, where the keys are the adjacent vertices and the values are the weights of the edges.

Here is an example of how to create a maze from a dictionary representation:

.. code-block:: python

    # Pyrat imports
    from pyrat import MazeFromDict

    # Define the maze as a dictionary
    maze_dict = {
        0: {1: 1, 4: 1},
        1: {0: 1, 2: 1, 5: 1},
        2: {1: 1, 6: 5},
        4: {0: 1, 5: 1},
        5: {1: 1, 4: 1, 6: 1, 9: 1},
        6: {2: 5, 5: 1, 7: 1, 10: 1},
        7: {6: 1, 11: 1},
        9: {5: 1, 10: 1},
        10: {6: 1, 9: 1, 11: 1},
        11: {7: 1, 10: 1}
    }

    # Create the maze
    maze = MazeFromDict(maze_dict)

    # Show the maze
    print(maze)

When you run this code, you will see the following output:

.. code-block:: text

    Maze object:
    |  Width: 4
    |  Height: 3
    |  Vertices: [0, 1, 2, 4, 5, 6, 7, 9, 10, 11]
    |  Adjacency matrix:
    |  |  0 <-- (1) --> 1
    |  |  0 <-- (1) --> 4
    |  |  1 <-- (1) --> 2
    |  |  1 <-- (1) --> 5
    |  |  2 <-- (5) --> 6
    |  |  4 <-- (1) --> 5
    |  |  5 <-- (1) --> 6
    |  |  5 <-- (1) --> 9
    |  |  6 <-- (1) --> 7
    |  |  6 <-- (1) --> 10
    |  |  7 <-- (1) --> 11
    |  |  9 <-- (1) --> 10
    |  |  10 <-- (1) --> 11

Now, you can use this maze in your game.
The ``Game`` class has an argument ``fixed_maze`` that allows you to pass a fixed maze.
Let's extend the code above with this script:

.. code-block:: python

    # Pyrat imports
    from pyrat import Game, MazeFromDict
    from players.Random1 import Random1

    # Define the maze as a dictionary
    maze_dict = {
        0: {1: 1, 4: 1},
        1: {0: 1, 2: 1, 5: 1},
        2: {1: 1, 6: 5},
        4: {0: 1, 5: 1},
        5: {1: 1, 4: 1, 6: 1, 9: 1},
        6: {2: 5, 5: 1, 7: 1, 10: 1},
        7: {6: 1, 11: 1},
        9: {5: 1, 10: 1},
        10: {6: 1, 9: 1, 11: 1},
        11: {7: 1, 10: 1}
    }

    # Create the maze
    maze = MazeFromDict(maze_dict)

    # Create the game with the fixed maze and one cheese
    game = Game(fixed_maze=maze, nb_cheese=1)

    # Register a player
    player = Random1()
    game.add_player(player)

    # Start the game
    game.start()

When you run this code, it will create a game with the specified maze and one piece of cheese, placed at a random location.
Here is what our maze looks like:

.. image:: /_static/custom_maze.png

As you can see, the weight 5 edge between vertices 2 and 6 translates in a mud, that takes 5 turns to cross.
Also, the missing vertices (3 and 8) lead to holes in the maze.
Finally, note that the algorithm was able to infer the width and height of the maze, which are 4 and 3 respectively.

Fixing the Cheese Locations
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Note that it is also possible to set the locations of the cheese pieces in the maze.
To do this, you can use the ``fixed_cheese`` argument of the ``Game`` class.
This argument should be a list of distinct integers, representing the indices of the vertices where the cheese pieces are located.
For instance, let's say you want to place the cheese pieces at vertices 1 and 5, you can do it like this:

.. code-block:: python

    # Pyrat imports
    from pyrat import Game, MazeFromDict
    from players.Random1 import Random1

    # Define the maze as a dictionary
    maze_dict = {
        0: {1: 1, 4: 1},
        1: {0: 1, 2: 1, 5: 1},
        2: {1: 1, 6: 5},
        4: {0: 1, 5: 1},
        5: {1: 1, 4: 1, 6: 1, 9: 1},
        6: {2: 5, 5: 1, 7: 1, 10: 1},
        7: {6: 1, 11: 1},
        9: {5: 1, 10: 1},
        10: {6: 1, 9: 1, 11: 1},
        11: {7: 1, 10: 1}
    }

    # Create the maze
    maze = MazeFromDict(maze_dict)

    # Create the game with the fixed maze and fixed cheese
    game = Game(fixed_maze=maze, fixed_cheese=[1, 5])

    # Register a player
    player = Random1()
    game.add_player(player)

    # Start the game
    game.start()

Does it Always Work?
^^^^^^^^^^^^^^^^^^^^

In the example above, we created a maze from a dictionary representation.
However, writing the dictionary by hand can be tedious, especially for large mazes.
In its current state, PyRat does not provide a nice user-friendly way to create a maze from scratch.

However, the ``MazeFromDict`` constructor will crash if your dictionary does not respect the maze properties.
As an example, let's make the edge between vertices 0 and 1 asymmetric, *i.e.*, 0 cannot reach 1, but 1 can reach 0.

.. code-block:: python

    # Pyrat imports
    from pyrat import MazeFromDict

    # Define the maze as a dictionary
    maze_dict = {
        0: {4: 1},
        1: {0: 1, 2: 1, 5: 1},
        2: {1: 1, 6: 5},
        4: {0: 1, 5: 1},
        5: {1: 1, 4: 1, 6: 1, 9: 1},
        6: {2: 5, 5: 1, 7: 1, 10: 1},
        7: {6: 1, 11: 1},
        9: {5: 1, 10: 1},
        10: {6: 1, 9: 1, 11: 1},
        11: {7: 1, 10: 1}
    }

    # Create the maze
    maze = MazeFromDict(maze_dict)

Running this code will lead to the following error:

.. code-block:: text

    Traceback (most recent call last):
        File "my_example_game.py", line 19, in <module>
            maze = MazeFromDict(maze_dict)
                   ^^^^^^^^^^^^^^^^^^^^^^^
        File "MazeFromDict.py", line 71, in __init__
            assert all(vertex in description[neighbor] for vertex in description for neighbor in description[vertex]), "The maze must be symmetric"
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError: The maze must be symmetric

To reduce the risk of errors, we advise that you first draw your maze on paper, and then write the dictionary representation by hand.