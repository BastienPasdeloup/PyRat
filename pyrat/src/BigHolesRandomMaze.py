#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# Please import necessary elements using the following syntax:
#     from pyrat import <element_name>

"""
This module provides functionality for generating mazes with large holes in them, which can be used in various game scenarios.
It extends ``RandomMaze`` to create a specific type of maze with larger holes, enhancing the gameplay experience by introducing more complex navigation challenges.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# PyRat imports
from pyrat.src.RandomMaze import RandomMaze

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class BigHolesRandomMaze (RandomMaze):

    """
    *(This class inherits from* ``RandomMaze`` *).*

    This class defines a random maze with big holes here and there.
    The maze is created by removing random cells from a full maze, and making sure the maze remains connected.
    Cells are removed with a larger probability if they are close to an already existing hole.

    You can use this class to create a maze with this algorithm.
    However, if you just want to play a game, you can use the ``Game`` class instead, which will create a maze for you.
    Just make sure to set the ``random_maze_algorithm`` parameter to ``RandomMazeAlgorithm.BIG_HOLES`` when creating the game.
    """

    #############################################################################################################################################
    #                                                               MAGIC METHODS                                                               #
    #############################################################################################################################################

    def __init__ ( self,
                   *args:    object,
                   **kwargs: object
                 ) ->        None:

        """
        Initializes a new instance of the class.

        Args:
            *args:    Arguments to pass to the parent constructor.
            **kwargs: Keyword arguments to pass to the parent constructor.
        """

        # Inherit from parent class
        super().__init__(*args, **kwargs)
        
        # Generate the maze
        self._create_maze()

    #############################################################################################################################################
    #                                                             PROTECTED METHODS                                                             #
    #############################################################################################################################################

    def _add_cells (self) -> None:
        
        """
        *(This method redefines the method of the parent class with the same name).*

        Adds cells to the maze by starting from a full maze and removing cells one by one.
        """

        # Initialize maze with all cells
        for row in range(self.get_height()):
            for col in range(self.get_width()):
                self.add_vertex(self.rc_to_i(row, col))

        # Connect them
        for row in range(self.get_height()):
            for col in range(self.get_width()):
                if row > 0:
                    self.add_edge(self.rc_to_i(row, col), self.rc_to_i(row - 1, col))
                if col > 0:
                    self.add_edge(self.rc_to_i(row, col), self.rc_to_i(row, col - 1))

        # Remember the number of neighbors per vertex
        neighbors_per_vertex = {vertex: len(self.get_neighbors(vertex)) for vertex in self.get_vertices()}

        # Remove some vertices until the desired density is reached
        while self.nb_vertices() > self._target_nb_vertices:

            # The probability to be removed depends on the number of neighbors already removed
            vertices = self.get_vertices()
            selection_weights = [1 + (self.get_width() * self.get_height() - self.nb_vertices()) * (neighbors_per_vertex[vertex] - len(self.get_neighbors(vertex)))**2.0 for vertex in vertices]

            # Remove a random vertex
            vertex = self._rng.choices(vertices, selection_weights)[0]
            neighbors = self.get_neighbors(vertex)
            self.remove_vertex(vertex)

            # Make sure the maze is still connected
            if not self.is_connected():
                self.add_vertex(vertex)
                for neighbor in neighbors:
                    self.add_edge(vertex, neighbor)

#####################################################################################################################################################
#####################################################################################################################################################