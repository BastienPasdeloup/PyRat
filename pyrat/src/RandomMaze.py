#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# Please import necessary elements using the following syntax:
#     from pyrat import <element_name>

"""
This module provides a base class for random mazes.
It extends ``Maze`` to create a specific type of maze with random cells, walls, and mud.
However, it does not implement the maze generation algorithm itself and is meant to be subclassed.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
import sys
import random
import abc

# PyRat imports
from pyrat.src.Maze import Maze

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class RandomMaze (Maze, abc.ABC):

    """
    *(This class inherits from* ``Maze`` *).*
    
    A random maze is a maze that is created randomly.
    You can specify the size of the maze, the density of cells, walls, and mud, and the range of the mud values.
    You can also specify a random seed to reproduce the same maze later.
    """

    #############################################################################################################################################
    #                                                               MAGIC METHODS                                                               #
    #############################################################################################################################################

    def __init__ ( self,
                   cell_percentage: float,
                   wall_percentage: float,
                   mud_percentage:  float,
                   mud_range:       tuple[int, int] | None = None,
                   random_seed:     int | None = None,
                   *args:           object,
                   **kwargs:        object
                 ) ->               None:

        """
        *(This class is abstract and meant to be subclassed, not instantiated directly).*

        Initializes a new instance of the class.

        Args:
            cell_percentage: Percentage of cells to be reachable.
            wall_percentage: Percentage of walls to be present.
            mud_percentage:  Percentage of mud to be present.
            mud_range:       Range of the mud values (optional if mud_percentage = 0.0).
            random_seed:     Random seed for the maze generation, set to None for a random value.
            args:            Arguments to pass to the parent constructor.
            kwargs:          Keyword arguments to pass to the parent constructor.
        """

        # Inherit from parent class
        super().__init__(*args, **kwargs)
        
        # Debug
        assert isinstance(cell_percentage, float), "Argument 'cell_percentage' must be a real number"
        assert isinstance(wall_percentage, float), "Argument 'wall_percentage' must be a real number"
        assert isinstance(mud_percentage, float), "Argument 'mud_percentage' must be a real number"
        assert isinstance(mud_range, (type(None), tuple, list)), "Argument 'mud_range' must be a tuple, a list, or None"
        assert isinstance(random_seed, (int, type(None))), "Argument 'random_seed' must be an integer or None"
        assert random_seed is None or 0 <= random_seed < sys.maxsize, "Argument 'random_seed' must be a positive integer or None"
        assert (mud_percentage > 0.0 and mud_range is not None and len(mud_range) == 2) or mud_percentage == 0.0, "Argument 'mud_range' must be specified if 'mud_percentage' is not 0.0"
        assert mud_range is None or isinstance(mud_range[0], int), "Argument 'mud_range' must be a tuple of integers"
        assert mud_range is None or isinstance(mud_range[1], int), "Argument 'mud_range' must be a tuple of integers"
        assert 0.0 <= cell_percentage <= 100.0, "Argument 'cell_percentage' must be a percentage"
        assert 0.0 <= wall_percentage <= 100.0, "Argument 'wall_percentage' must be a percentage"
        assert 0.0 <= mud_percentage <= 100.0, "Argument 'mud_percentage' must be a percentage"
        assert mud_range is None or 1 < mud_range[0] <= mud_range[1], "Argument 'mud_range' must be a valid interval with minimum value at least 2"
        assert int(self.get_width() * self.get_height() * cell_percentage / 100) > 1, "The maze must have at least two vertices"

        # Protected attributes
        self._target_nb_vertices = int(self.get_width() * self.get_height() * cell_percentage / 100)
        self._wall_percentage = wall_percentage
        self._mud_percentage = mud_percentage
        self._mud_range = mud_range
        self._random_seed = random_seed
        self._rng = random.Random(self._random_seed)

    #############################################################################################################################################
    #                                                             PROTECTED METHODS                                                             #
    #############################################################################################################################################

    @abc.abstractmethod
    def _add_cells (self) -> None:

        """
        *(This method is abstract and must be implemented in the child classes).*

        It should add cells to the maze.

        Raises:
            NotImplementedError: If the method is not implemented in the child class.
        """

        # This method must be implemented in the child classes
        # By default we raise an error
        raise NotImplementedError("This method must be implemented in the child classes.")

    #############################################################################################################################################

    def _add_mud (self) -> None:

        """
        This method adds mud to the maze.
        It replaces some edges with weighted ones.
        """

        # Determine the number of mud edges
        target_nb_mud = int(self.nb_edges() * self._mud_percentage / 100)

        # Add mud to some edges
        edges = self.get_edges()
        self._rng.shuffle(edges)
        for vertex, neighbor in edges[:target_nb_mud]:
            self.remove_edge(vertex, neighbor, True)
            weight = self._rng.randint(self._mud_range[0], self._mud_range[1])
            self.add_edge(vertex, neighbor, weight)

    #############################################################################################################################################

    def _add_walls (self) -> None:

        """
        This method adds walls to the maze.
        It uses the minimum spanning tree to determine the maximum number of walls.
        """

        # Determine the maximum number of walls by computing the minimum spanning tree
        mst = self.minimum_spanning_tree(self._rng.randint(0, sys.maxsize))
        target_nb_walls = int((self.nb_edges() - mst.nb_edges()) * self._wall_percentage / 100)
        walls = []
        for vertex, neighbor in self.get_edges():
            if not mst.has_edge(vertex, neighbor):
                self.remove_edge(vertex, neighbor, True)
                walls.append((vertex, neighbor))
        
        # Remove some walls until the desired density is reached
        self._rng.shuffle(walls)
        for vertex, neighbor in walls[target_nb_walls:]:
            self.add_edge(vertex, neighbor)

    #############################################################################################################################################

    def _create_maze (self) -> None:

        """
        *(This method redefines the abstract method of the parent class with the same name).*

        It creates a random maze using the parameters given at initialization.
        It should be called by the constructor of the child classes.
        """

        # Add cells, walls, and mud
        self._add_cells()
        self._add_walls()
        self._add_mud()

#####################################################################################################################################################
#####################################################################################################################################################