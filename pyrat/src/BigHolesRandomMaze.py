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

class BigHolesRandomMaze (RandomMaze):

    """
        This class inherits from the RandomMaze class.
        Therefore, it has the attributes and methods defined in the RandomMaze class in addition to the ones defined below.

        With this maze, holes have a larger probability to appear if they are close to another hole.
        The maze is created by removing random cells from a full maze, and making sure the maze remains connected.
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

        # Initialize maze with all cells
        for row in range(self.height):
            for col in range(self.width):
                self.add_vertex(self.rc_to_i(row, col))

        # Connect them
        for row in range(self.height):
            for col in range(self.width):
                if row > 0:
                    self.add_edge(self.rc_to_i(row, col), self.rc_to_i(row - 1, col))
                if col > 0:
                    self.add_edge(self.rc_to_i(row, col), self.rc_to_i(row, col - 1))

        # Remember the number of neighbors per vertex
        neighbors_per_vertex = {vertex: len(self.get_neighbors(vertex)) for vertex in self.vertices}

        # Remove some vertices until the desired density is reached
        while self.nb_vertices > self._target_nb_vertices:

            # The probability to be removed depends on the number of neighbors already removed
            vertices = self.vertices
            selection_weights = [1 + (self.width * self.height - self.nb_vertices) * (neighbors_per_vertex[vertex] - len(self.get_neighbors(vertex)))**2.0 for vertex in vertices]

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