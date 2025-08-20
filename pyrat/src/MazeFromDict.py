#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# Please import necessary elements using the following syntax:
#     from pyrat import <element_name>

"""
This module provides a maze that is created from a fixed description as a dictionary.
It extends ``Maze`` to create a specific type of maze with a fixed structure.
This class is especially useful to allow exporting a maze to a file, and then reusing it later.
It is also useful to test a player on a fixed maze.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
import math

# PyRat imports
from pyrat.src.Maze import Maze

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class MazeFromDict (Maze):

    """
    *(This class inherits from* ``Maze`` *).*
    
    This is a maze that is created from a fixed description as a dictionary, where keys are cell indices.
    Associated values are dictionaries, where keys are neighbors of the corresponding cell, and values are the weights of the corresponding edges.
    This class is especially useful to allow exporting a maze to a file, and then reusing it later.
    It is also useful to test a player on a fixed maze, to compare its performance with other players.
    """

    #############################################################################################################################################
    #                                                               MAGIC METHODS                                                               #
    #############################################################################################################################################

    def __init__ ( self,
                   description: dict[int, dict[int, int]],
                   *args:       object,
                   **kwargs:    object
                 ) ->           None:

        """
        Initializes a new instance of the class.

        Args:
            description: Fixed maze as a dictionary.
            *args:       Arguments to pass to the parent constructor.
            **kwargs:    Keyword arguments to pass to the parent constructor.
        """

        # Inherit from parent class
        super().__init__(*args, **kwargs)

        # Debug
        assert isinstance(description, dict), "Argument 'description' must be a dictionary"
        assert all(isinstance(vertex, int) for vertex in description), "All keys of 'description' must be integers"
        assert all(isinstance(neighbor, int) for vertex in description for neighbor in description[vertex]), "All keys of subdictionaries of 'description' must be integers"
        assert all(isinstance(description[vertex][neighbor], int) for vertex in description for neighbor in description[vertex]), "All values of subdictionaries of 'description' must be integers"
        assert len(description) > 1, "The maze must have at least two vertices"
        assert all(len(description[vertex]) > 0 for vertex in description), "All vertices must have at least one neighbor"
        assert all(vertex in description[neighbor] for vertex in description for neighbor in description[vertex]), "The maze must be symmetric"
        assert all(description[vertex][neighbor] == description[neighbor][vertex] for vertex in description for neighbor in description[vertex]), "The maze must have symmetric weights"
        assert all(description[vertex][neighbor] > 0 for vertex in description for neighbor in description[vertex]), "All weights must be positive"

        # Private attributes
        self.__description = description

        # Generate the maze
        self._create_maze()

    #############################################################################################################################################
    #                                                             PROTECTED METHODS                                                             #
    #############################################################################################################################################

    def _create_maze (self) -> None:

        """
        *(This method redefines the method of the parent class with the same name).*

        Creates a maze from the description provided at initialization.
        """
        
        # Determine the vertices
        vertices = self.__description.keys()

        # Determine the edges
        edges = []
        for vertex in self.__description:
            neighbors = self.__description[vertex]
            for neighbor in neighbors:
                edges.append((vertex, neighbor, self.__description[vertex][neighbor]))

        # Determine the dimensions of the maze
        self._width = max([abs(edge[1] - edge[0]) for edge in edges])
        self._height = math.ceil((max(vertices) + 1) / self.get_width())

        # Add vertices and edges
        for vertex in vertices:
            self.add_vertex(vertex)
        for edge in edges:
            self.add_edge(edge[0], edge[1], edge[2])

#####################################################################################################################################################
#####################################################################################################################################################
