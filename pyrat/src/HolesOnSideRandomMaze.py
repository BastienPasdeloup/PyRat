#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This file is part of the PyRat library.
    It is meant to be used as a library, and not to be executed directly.
    Please import necessary elements using the following syntax:
        from pyrat import <element_name>
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
from typing import *
from typing_extensions import *
from numbers import *

# PyRat imports
from pyrat.src.RandomMaze import RandomMaze

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class HolesOnSideRandomMaze (RandomMaze):

    """
        This class inherits from the RandomMaze class.
        Therefore, it has the attributes and methods defined in the RandomMaze class in addition to the ones defined below.

        With this maze, holes are distributed on the sides of the maze.
        The maze is created by adding cells from the center of the maze
    """

    #############################################################################################################################################
    #                                                               MAGIC METHODS                                                               #
    #############################################################################################################################################

    def __init__ ( self:     Self,
                   *args:    Any,
                   **kwargs: Any
                 ) ->        None:

        """
            This function is the constructor of the class.
            When an object is instantiated, this method is called to initialize the object.
            This is where you should define the attributes of the object and set their initial values.
            Arguments *args and **kwargs are used to pass arguments to the parent constructor.
            This is useful not to declare again all the parent's attributes in the child class.
            In:
                * self:   Reference to the current object.
                * args:   Arguments to pass to the parent constructor.
                * kwargs: Keyword arguments to pass to the parent constructor.
            Out:
                * A new instance of the class (we indicate None as return type per convention, see PEP-484).
        """

        # Inherit from parent class
        super().__init__(*args, **kwargs)
        
        # Generate the maze
        self._create_maze()

    #############################################################################################################################################
    #                                                             PROTECTED METHODS                                                             #
    #############################################################################################################################################

    @override
    def _add_cells ( self: Self,
                   ) ->    None:
        
        """
            This method redefines the abstract method of the parent class.
            It adds cells to the maze by starting from a full maze and removing cells one by one.
            In:
                * self: Reference to the current object.
            Out:
                * None.
        """

        # Add cells from the middle of the maze
        vertices_to_add = [self.rc_to_i(self.height // 2, self.width // 2)]

        # Make some sort of breadth-first search to add cells
        while self.nb_vertices < self._target_nb_vertices:

            # Get a random vertex
            vertex = vertices_to_add.pop(self._rng.randint(0, len(vertices_to_add) - 1))

            # Add it if it is not already in the maze
            if vertex in self.vertices:
                continue
            self.add_vertex(vertex)

            # Add neighbors
            row, col = self.i_to_rc(vertex)
            if 0 < row < self.height:
                vertices_to_add.append(self.rc_to_i(row - 1, col))
            if 0 <= row < self.height - 1:
                vertices_to_add.append(self.rc_to_i(row + 1, col))
            if 0 < col < self.width:
                vertices_to_add.append(self.rc_to_i(row, col - 1))
            if 0 <= col < self.width - 1:
                vertices_to_add.append(self.rc_to_i(row, col + 1))
        
        # Connect the vertices
        for i, vertex_1 in enumerate(self.vertices):
            for j, vertex_2 in enumerate(self.vertices, i + 1):
                if self.coords_difference(vertex_1, vertex_2) in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                    self.add_edge(vertex_1, vertex_2)

#####################################################################################################################################################
#####################################################################################################################################################