#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# Please import necessary elements using the following syntax:
#     from pyrat import <element_name>

"""
This module provides a maze that is created by adding cells from the center of the maze.
It extends ``RandomMaze`` to create a specific type of maze with holes distributed on the sides of the maze.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# PyRat imports
from pyrat.src.RandomMaze import RandomMaze

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class HolesOnSideRandomMaze (RandomMaze):

    """
    *(This class inherits from* ``RandomMaze`` *).*
    
    With this maze, holes are distributed on the sides of the maze.
    The maze is created by adding cells from the center of the maze
    
    You can use this class to create a maze with this algorithm.
    However, if you just want to play a game, you can use the ``Game`` class instead, which will create a maze for you.
    Just make sure to set the ``random_maze_algorithm`` parameter to ``RandomMazeAlgorithm.HOLES_ON_SIDE`` when creating the game.
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

        It adds cells to the maze by starting from a full maze and removing cells one by one.
        """

        # Add cells from the middle of the maze
        vertices_to_add = [self.rc_to_i(self.get_height() // 2, self.get_width() // 2)]

        # Make some sort of breadth-first search to add cells
        while self.nb_vertices() < self._target_nb_vertices:

            # Get a random vertex
            vertex = vertices_to_add.pop(self._rng.randint(0, len(vertices_to_add) - 1))

            # Add it if it is not already in the maze
            if vertex in self.get_vertices():
                continue
            self.add_vertex(vertex)

            # Add neighbors
            row, col = self.i_to_rc(vertex)
            if 0 < row < self.get_height():
                vertices_to_add.append(self.rc_to_i(row - 1, col))
            if 0 <= row < self.get_height() - 1:
                vertices_to_add.append(self.rc_to_i(row + 1, col))
            if 0 < col < self.get_width():
                vertices_to_add.append(self.rc_to_i(row, col - 1))
            if 0 <= col < self.get_width() - 1:
                vertices_to_add.append(self.rc_to_i(row, col + 1))
        
        # Connect the vertices
        for i, vertex_1 in enumerate(self.get_vertices()):
            for j, vertex_2 in enumerate(self.get_vertices(), i + 1):
                if self.coords_difference(vertex_1, vertex_2) in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                    self.add_edge(vertex_1, vertex_2)

#####################################################################################################################################################
#####################################################################################################################################################