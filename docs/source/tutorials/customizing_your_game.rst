Customizing Your Game
=====================

A great aspect of PyRat is that you can customize your game to fit your needs.
In this tutorial, we will explore how to modify the game by customizing the game elements.

For instance, in the course we give at IMT Atlantique, we start with simple objectives with one piece of cheese with no mud.
This allows students to study graph traversal algorithms such as breadth-first search (BFS) and depth-first search (DFS).
Then, adding mud allows to study Dijkstra's algorithm.
Increasing the number of cheese pieces allows to study the traveling salesperson problem (TSP) and heuristics.

Arguments of the ``Game`` Constructor
-------------------------------------

The best way to customize your game is to create a new game file in the ``games`` directory.
As we saw in previous tutorials, you need to instantiate an object from the :doc:`Game </pyrat/Game>` class.
The constructor of the ``Game`` class takes several arguments that allow you to customize the game:

Random Control
^^^^^^^^^^^^^^

Many elements are determined randomly in the game.
It can be the shape of the maze, the distribution of cheese, or the initial positions of players.
To control this randomness, you can use the following arguments:

- ``random_seed``: Global random seed for all elements, or ``None`` for a random value.
- ``random_seed_maze``: Random seed for maze generation, or ``None`` for a random value.
- ``random_seed_cheese``: Random seed for cheese distribution, or ``None`` for a random value.
- ``random_seed_players``: Random seed for initial player locations, or ``None`` for a random value.

A seed is a number that initializes the random number generator.
Using the same seed will always produce the same random elements, which is useful for debugging or testing purposes.
If you set a seed to ``None`` (or do not set the argument), PyRat will use a random value, which means that the game will be different each time you run it.

The ``random_seed`` argument allows you to control the overall randomness of the game, while the other seed arguments let you fine-tune specific aspects.

When generating elements at random, you can specify the properties of the maze and cheese distribution using the following arguments:

- ``maze_width``: Width of the maze (number of cells).
- ``maze_height``: Height of the maze (number of cells).
- ``cell_percentage``: Percentage of accessible cells in the maze (0% = useless maze, 100% = full rectangle).
- ``wall_percentage``: Percentage of walls in the maze (0% = empty, 100% = max walls while connected).
- ``mud_percentage``: Percentage of adjacent cell pairs separated by mud.
- ``mud_range``: Interval of turns needed to cross mud.
- ``random_maze_algorithm``: Algorithm to generate the maze.
- ``nb_cheese``: Number of pieces of cheese in the maze.

On the contrary, if you want to work on a custom maze or cheese distribution, the following arguments can be used:

- ``fixed_maze``: Fixed maze in any PyRat-accepted representation (``Maze``, ``dict``, ``numpy.ndarray``, or ``torch.tensor``).
- ``fixed_cheese``: Fixed list of cheese locations.

Game-Related Arguments
^^^^^^^^^^^^^^^^^^^^^^

In addition to the random control and maze/cheese generation, you can customize other game-related aspects using the following arguments:

- ``preprocessing_time``: Time given to players before the game starts.
- ``turn_time``: Time after which players miss a turn.
- ``game_mode``: Indicates concurrency mode for players.

These elements will customize the game mechanics and how players interact with the game.
In particular, the ``turn_time`` and ``preprocessing_time`` arguments allow you to control the time players have to make decisions, which can be crucial for studying algorithms.

Graphical Elements
^^^^^^^^^^^^^^^^^^

In addition to the game mechanics, you can also customize the graphical elements of the game using the following arguments:

- ``render_mode``: Method to display the game.
- ``render_simplified``: If ``True``, hides non-essential elements in rendering.
- ``rendering_speed``: Controls the speed of the game when rendering.
- ``trace_length``: Maximum trace length to display (GUI rendering only).
- ``fullscreen``: If ``True``, renders the game in fullscreen (GUI only).
- ``clear_shell_each_turn``: If ``True``, clears the shell each turn (shell rendering only).

Other Arguments
^^^^^^^^^^^^^^^

Finally, there are some other arguments that can be used for debugging or replaying games:

- ``continue_on_error``: If ``True``, continues the game if a player crashes.
- ``save_path``: Path where games are saved.
- ``save_game``: If ``True``, saves the game.

Customization of Players
------------------------

:doc:`Players </pyrat/Player>` can also be customized to a certain extent.
When creating a new player, you can specify the following arguments:

- ``name``: Name of the player.
  Note that the name must be unique among players in the game.
- ``skin``: Skin of the player, given as a possible value of the :doc:`PlayerSkin </pyrat/enums>` enumeration.

When creating a new game, you also specify the initial positions of players using the ``game.add_player()`` method.
This method takes the following arguments:

- ``team``: Team to which the player belongs.
  As long as there is more than one team, players will be able to compete against each other.
- ``position``: Initial position of the player.
  This can be a cell in the maze or a value described in the :doc:`StartingLocation </pyrat/enums>` enumeration.

You can have as many players and teams as you want.
By default, all players will start at the center of the maze, to give them a fair chance to explore the maze.

Example
-------

The PyRat workspace comes with a ``games`` directory containing a file named ``sample_game.py``.
In this file, you can find an example of how to create a game with custom parameters.
We also give a skin to the players and place them in teams.
Have a look at the :doc:`code of the game script </workspace/games/sample_game>` to see how it works.