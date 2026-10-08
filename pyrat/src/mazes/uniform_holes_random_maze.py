##########################################################################################
########################################## INFO ##########################################
##########################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# Please import necessary elements using the following syntax:
#     from pyrat import <element_name>

"""
This module provides a maze that is created by removing random cells from a full maze uniformly.
It makes sure the maze remains connected.
"""

##########################################################################################
######################################### IMPORTS ########################################
##########################################################################################

# PyRat imports
from pyrat.src.mazes.random_maze import RandomMaze
from pyrat.src.game.exceptions import PyRatException

##########################################################################################
######################################### CLASSES ########################################
##########################################################################################

class UniformHolesRandomMaze (RandomMaze):

    """
    *(This class inherits from* ``RandomMaze`` *).*        
    
    With this maze, holes are uniformly distributed in the maze.
    The maze is created by removing random cells from a full maze, and making sure the maze remains connected.
    """

    ##################################################################################
    #                                   CONSTRUCTOR                                  #
    ##################################################################################

    def __init__ ( self,
                   cell_percentage: float,
                   *args:           object,
                   **kwargs:        object
                 ) ->               None:

        """
        Initializes a new instance of the class, and generates the maze.

        Args:
            cell_percentage: Percentage of cells to be reachable.
            args:            Arguments to pass to the parent constructor.
            kwargs:          Keyword arguments to pass to the parent constructor.
        """

        # Check validity
        if not isinstance(cell_percentage, float):
            raise PyRatException("Argument 'cell_percentage' must be a real number")
        if not (0.0 <= cell_percentage <= 100.0):
            raise PyRatException("Argument 'cell_percentage' must be a percentage")

        # Protected attributes
        # They must be set before calling the parent constructor, which generates the maze
        self._cell_percentage = cell_percentage

        # Inherit from parent class
        super().__init__(*args, **kwargs)

    ##################################################################################
    #                                PROTECTED METHODS                               #
    ##################################################################################

    def _add_cells (self) -> None:
        
        """
        *(This method redefines the method of the parent class with the same name).*

        It adds cells to the maze by starting from a full maze and removing cells one by one.
        """

        # Determine the number of cells to keep
        self._target_nb_vertices = int(self.get_width() * self.get_height() * self._cell_percentage / 100)
        if not (self._target_nb_vertices > 1):
            raise PyRatException("The maze must have at least two vertices")

        # Start from a full maze, with all cells connected to their neighbors
        super()._add_cells()

        # Remove some vertices until the desired density is reached
        while self.nb_vertices() > self._target_nb_vertices:

            # Remove a random vertex
            vertex = self._rng.choice(self.get_vertices())
            neighbors = self.get_neighbors(vertex)
            self.remove_vertex(vertex)

            # Make sure the maze is still connected
            if not self.is_connected():
                self.add_vertex(vertex)
                for neighbor in neighbors:
                    self.add_edge(vertex, neighbor)

##########################################################################################
##########################################################################################
