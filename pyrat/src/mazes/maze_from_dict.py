##########################################################################################
########################################## INFO ##########################################
##########################################################################################

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

##########################################################################################
######################################### IMPORTS ########################################
##########################################################################################

# External imports
import math

# PyRat imports
from pyrat.src.mazes.maze import Maze
from pyrat.src.game.exceptions import PyRatException

##########################################################################################
######################################### CLASSES ########################################
##########################################################################################

class MazeFromDict (Maze):

    """
    *(This class inherits from* ``Maze`` *).*
    
    This is a maze that is created from a fixed description as a dictionary, where keys are cell indices.
    Associated values are dictionaries, where keys are neighbors of the corresponding cell, and values are the weights of the corresponding edges.
    This class is especially useful to allow exporting a maze to a file, and then reusing it later.
    It is also useful to test a player on a fixed maze, to compare its performance with other players.
    """

    ##################################################################################
    #                                   CONSTRUCTOR                                  #
    ##################################################################################

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

        Raises:
            PyRatException: If a width or a height is given, as they are inferred from the description.
        """

        # The width and height are inferred from the description, so they must not be given
        given_dimensions = [f"{key}={kwargs[key]!r}" for key in ("width", "height") if key in kwargs] + [f"{value!r} (positional)" for value in args[:2]]
        if given_dimensions:
            raise PyRatException(f"Arguments 'width' and 'height' must not be given to MazeFromDict, as they are inferred from 'description', got {', '.join(given_dimensions)}")

        # Inherit from parent class
        super().__init__(*args, **kwargs)

        # Check validity
        if not isinstance(description, dict):
            raise PyRatException(f"Argument 'description' must be a dictionary, got a value of type {type(description).__name__}")
        if not all(isinstance(vertex, int) and not isinstance(vertex, bool) for vertex in description):
            raise PyRatException(f"All keys of 'description' must be integers, got key {next(f'{vertex!r} of type {type(vertex).__name__}' for vertex in description if not (isinstance(vertex, int) and not isinstance(vertex, bool)))}")
        if not all(isinstance(description[vertex], dict) for vertex in description):
            raise PyRatException(f"All values of 'description' must be dictionaries associating neighbors with weights, got {next(f'{description[vertex]!r:.100} of type {type(description[vertex]).__name__} in description[{vertex!r}]' for vertex in description if not isinstance(description[vertex], dict))}")
        if not all(isinstance(neighbor, int) and not isinstance(neighbor, bool) for vertex in description for neighbor in description[vertex]):
            raise PyRatException(f"All keys of subdictionaries of 'description' must be integers, got neighbor {next(f'{neighbor!r} of type {type(neighbor).__name__} in description[{vertex!r}]' for vertex in description for neighbor in description[vertex] if not (isinstance(neighbor, int) and not isinstance(neighbor, bool)))}")
        if not all(isinstance(description[vertex][neighbor], int) and not isinstance(description[vertex][neighbor], bool) for vertex in description for neighbor in description[vertex]):
            raise PyRatException(f"All values of subdictionaries of 'description' must be integers, got weight {next(f'{description[vertex][neighbor]!r} of type {type(description[vertex][neighbor]).__name__} in description[{vertex!r}][{neighbor!r}]' for vertex in description for neighbor in description[vertex] if not (isinstance(description[vertex][neighbor], int) and not isinstance(description[vertex][neighbor], bool)))}")
        if not (len(description) > 1):
            raise PyRatException(f"The maze must have at least two vertices, got {len(description)} key(s) in 'description'")
        if not all(vertex >= 0 for vertex in description):
            raise PyRatException(f"All keys of 'description' must be non-negative, as cells are numbered from 0, got key {next(vertex for vertex in description if not vertex >= 0)!r}")
        if not all(len(description[vertex]) > 0 for vertex in description):
            raise PyRatException(f"All vertices must have at least one neighbor, got vertex {next(vertex for vertex in description if not len(description[vertex]) > 0)!r} with no neighbor in 'description'")
        if not all(vertex not in description[vertex] for vertex in description):
            raise PyRatException(f"A vertex cannot be its own neighbor, got vertex {next(vertex for vertex in description if vertex in description[vertex])!r} among its own neighbors in 'description'")
        if not all(neighbor in description for vertex in description for neighbor in description[vertex]):
            raise PyRatException(f"All neighbors must also be keys of 'description', got neighbor {next(f'{neighbor!r} of vertex {vertex!r}' for vertex in description for neighbor in description[vertex] if neighbor not in description)}, which is not a key")
        if not all(vertex in description[neighbor] for vertex in description for neighbor in description[vertex]):
            raise PyRatException(f"The maze must be symmetric, got {next(f'{neighbor!r} as a neighbor of {vertex!r}, but {vertex!r} is not a neighbor of {neighbor!r}' for vertex in description for neighbor in description[vertex] if vertex not in description[neighbor])}")
        if not all(description[vertex][neighbor] == description[neighbor][vertex] for vertex in description for neighbor in description[vertex]):
            raise PyRatException(f"The maze must have symmetric weights, got {next(f'weight {description[vertex][neighbor]!r} from {vertex!r} to {neighbor!r}, but {description[neighbor][vertex]!r} from {neighbor!r} to {vertex!r}' for vertex in description for neighbor in description[vertex] if description[vertex][neighbor] != description[neighbor][vertex])}")
        if not all(description[vertex][neighbor] > 0 for vertex in description for neighbor in description[vertex]):
            raise PyRatException(f"All weights must be positive, got {next(f'weight {description[vertex][neighbor]!r} from {vertex!r} to {neighbor!r}' for vertex in description for neighbor in description[vertex] if not description[vertex][neighbor] > 0)}")

        # Private attributes
        self.__description = description

        # Generate the maze
        self._create_maze()

    ##################################################################################
    #                                PROTECTED METHODS                               #
    ##################################################################################

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

##########################################################################################
##########################################################################################
