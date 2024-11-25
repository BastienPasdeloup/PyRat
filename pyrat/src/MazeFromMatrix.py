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
import math

# PyRat imports
from pyrat.src.Maze import Maze

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class MazeFromMatrix (Maze):

    """
        This class inherits from the Maze class.
        Therefore, it has the attributes and methods defined in the Maze class in addition to the ones defined below.

        This is a maze that is created from a fixed description as a numpy ndarray or a torch tensor.
        Indices of rows and columns are the indices of the corresponding cells.
        Entries are the weights of the corresponding edges.
        Rows and columns with only 0 values will be ignored.
        This class can be useful to test a player on a fixed maze, to compare its performance with other players.
    """

    #############################################################################################################################################
    #                                                               MAGIC METHODS                                                               #
    #############################################################################################################################################

    def __init__ ( self:        Self,
                   description: Any,
                   *args:       Any,
                   **kwargs:    Any
                 ) ->           None:

        """
            This function is the constructor of the class.
            When an object is instantiated, this method is called to initialize the object.
            This is where you should define the attributes of the object and set their initial values.
            Arguments *args and **kwargs are used to pass arguments to the parent constructor.
            This is useful not to declare again all the parent's attributes in the child class.
            In:
                * self:        Reference to the current object.
                * description: Fixed maze as a matrix (numpy.ndarray or torch.tensor).
                * args:        Arguments to pass to the parent constructor.
                * kwargs:      Keyword arguments to pass to the parent constructor.
            Out:
                * A new instance of the class (we indicate None as return type per convention, see PEP-484).
        """

        # Inherit from parent class
        super().__init__(*args, **kwargs)

        # Debug
        assert str(type(description)) in ["<class 'numpy.ndarray'>", "<class 'torch.Tensor'>"], "Argument 'description' must be a numpy.ndarray or a torch.Tensor"
        assert len(description.shape) == 2, "Argument 'description' must be a 2D matrix"
        assert description.shape[0] == description.shape[1], "Argument 'description' must be a square matrix"
        assert description.shape[0] > 1, "The maze must have at least two vertices"
        assert all(isinstance(weight, Integral) for weight in description.flatten().tolist()), "All entries of 'description' must be integers"
        assert (description == description.T).all(), "Argument 'description' must be a symmetric matrix"
        assert (description >= 0).all(), "All entries of 'description' must be non-negative"
        assert (description > 0).any(), "The maze must have at least one edge"

        # Private attributes
        self.__description = description

        # Generate the maze
        self._create_maze()

    #############################################################################################################################################
    #                                                             PROTECTED METHODS                                                             #
    #############################################################################################################################################

    @override
    def _create_maze ( self: Self,
                     ) ->    None:

        """
            This method redefines the abstract method of the parent class.
            Creates a maze from the description provided at initialization.
            In:
                * self: Reference to the current object.
            Out:
                * None.
        """

        # Determine the vertices
        vertices = []
        for vertex in range(self.__description.shape[0]):
            neighbors = [neighbor for neighbor in range(self.__description.shape[1]) if self.__description[vertex, neighbor] > 0]
            if len(neighbors) > 0:
                vertices.append(vertex)

        # Determine the edges
        edges = []
        for vertex in range(self.__description.shape[0]):
            for neighbor in range(self.__description.shape[1]):
                if self.__description[vertex, neighbor] > 0:
                    edges.append((vertex, neighbor, self.__description[vertex, neighbor].item()))

        # Determine the dimensions of the maze
        self._width = max([abs(edge[1] - edge[0]) for edge in edges])
        self._height = math.ceil((max(vertices) + 1) / self.width)

        # Add vertices and edges
        for vertex in vertices:
            self.add_vertex(vertex)
        for edge in edges:
            self.add_edge(edge[0], edge[1], edge[2])

#####################################################################################################################################################
#####################################################################################################################################################
