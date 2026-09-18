##########################################################################################
########################################## INFO ##########################################
##########################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.

"""
This package contains the graph structures used by PyRat, and the mazes built upon them.
    * ``graph`` defines a generic graph, with an adjacency dictionary.
    * ``maze`` defines a maze, which is a graph whose vertices are cells placed on a grid.
    * ``random_maze`` is the base class of the randomly generated mazes.
    * ``big_holes_random_maze``, ``holes_on_side_random_maze`` and ``uniform_holes_random_maze`` are the three algorithms generating random mazes.
    * ``maze_from_dict`` and ``maze_from_matrix`` build a maze from a fixed description.
"""

##########################################################################################
##########################################################################################
