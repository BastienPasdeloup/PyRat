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
import numpy
import torch

# PyRat imports
from pyrat.src.FixedMaze import FixedMaze

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class MazeFromMatrix (FixedMaze):

    """
        This class inherits from the FixedMaze class.
        Therefore, it has the attributes and methods defined in the FixedMaze class in addition to the ones defined below.

        This is a maze that is created from a fixed description as a numpy ndarray or a torch tensor.
        Indices of rows and columns are the indices of the corresponding cells.
        Entries are the weights of the corresponding edges.
        Rows and columns with only 0 values will be ignored.
        This class can be useful to test a player on a fixed maze, to compare its performance with other players.
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self:        Self,
                   description: Union[numpy.ndarray, torch.Tensor],
                   *args:       Any,
                   **kwargs:    Any
                 ) ->           Self:

        """
            This function is the constructor of the class.
            In:
                * self:        Reference to the current object.
                * description: Fixed maze as a matrix.
                * args:        Arguments to pass to the parent constructor.
                * kwargs:      Keyword arguments to pass to the parent constructor.
            Out:
                * A new instance of the class.
        """

        # Inherit from parent class
        super().__init__(*args, **kwargs)

        # Debug
        assert isinstance(description, (numpy.ndarray, torch.Tensor)) # Type check for description
        assert len(description.shape) == 2 # Check that the description is a matrix
        assert description.shape[0] == description.shape[1] # Check that the matrix is square
        assert description.shape[0] > 1 # The maze has at least two vertices
        assert all(isinstance(weight, Integral) for weight in description.flatten().tolist()) # Weights are integers
        assert (description == description.T).all() # Check that the matrix is symmetric
        assert (description >= 0).all() # Check that the weights are non-negative
        assert (description > 0).any() # Check that the maze has at least one edge

        # Private attributes
        self.__description = description

        # Generate the maze
        self._create_maze()

    #############################################################################################################################################
    #                                                             PROTECTED METHODS                                                             #
    #############################################################################################################################################

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

        # Build the maze
        self._initialize_maze(vertices, edges)

#####################################################################################################################################################
#####################################################################################################################################################
