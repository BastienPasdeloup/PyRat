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
        This class inherits from the Maze class.
        Therefore, it has the attributes and methods defined in the Maze class in addition to the ones defined below.

        This class is abstract and cannot be instantiated.
        You should use one of the subclasses to create a maze, or create your own subclass.

        A random maze is a maze that is created randomly.
        You can specify the size of the maze, the density of cells, walls, and mud, and the range of the mud values.
        You can also specify a random seed to reproduce the same maze later.
    """

    #############################################################################################################################################
    #                                                               MAGIC METHODS                                                               #
    #############################################################################################################################################

    def __init__ ( self:            Self,
                   cell_percentage: Number,
                   wall_percentage: Number,
                   mud_percentage:  Number,
                   mud_range:       Optional[Tuple[Integral, Integral]] = None,
                   random_seed:     Optional[Integral] = None,
                   *args:           Any,
                   **kwargs:        Any
                 ) ->               None:

        """
            This function is the constructor of the class.
            When an object is instantiated, this method is called to initialize the object.
            This is where you should define the attributes of the object and set their initial values.
            Arguments *args and **kwargs are used to pass arguments to the parent constructor.
            This is useful not to declare again all the parent's attributes in the child class.
            In:
                * self:            Reference to the current object.
                * cell_percentage: Percentage of cells to be reachable.
                * wall_percentage: Percentage of walls to be present.
                * mud_percentage:  Percentage of mud to be present.
                * mud_range:       Range of the mud values (optional if mud_percentage = 0.0).
                * random_seed:     Random seed for the maze generation, set to None for a random value.
                * args:            Arguments to pass to the parent constructor.
                * kwargs:          Keyword arguments to pass to the parent constructor.
            Out:
                * A new instance of the class (we indicate None as return type per convention, see PEP-484).
        """

        # Inherit from parent class
        super().__init__(*args, **kwargs)
        
        # Debug
        assert isinstance(cell_percentage, Number), "Argument 'cell_percentage' must be a real number"
        assert isinstance(wall_percentage, Number), "Argument 'wall_percentage' must be a real number"
        assert isinstance(mud_percentage, Number), "Argument 'mud_percentage' must be a real number"
        assert isinstance(mud_range, (type(None), tuple, list)), "Argument 'mud_range' must be a tuple, a list, or None"
        assert isinstance(random_seed, (Integral, type(None))), "Argument 'random_seed' must be an integer or None"
        assert random_seed is None or 0 <= random_seed < sys.maxsize, "Argument 'random_seed' must be a positive integer or None"
        assert (mud_percentage > 0.0 and mud_range is not None and len(mud_range) == 2) or mud_percentage == 0.0, "Argument 'mud_range' must be specified if 'mud_percentage' is not 0.0"
        assert mud_range is None or isinstance(mud_range[0], Integral), "Argument 'mud_range' must be a tuple of integers"
        assert mud_range is None or isinstance(mud_range[1], Integral), "Argument 'mud_range' must be a tuple of integers"
        assert 0.0 <= cell_percentage <= 100.0, "Argument 'cell_percentage' must be a percentage"
        assert 0.0 <= wall_percentage <= 100.0, "Argument 'wall_percentage' must be a percentage"
        assert 0.0 <= mud_percentage <= 100.0, "Argument 'mud_percentage' must be a percentage"
        assert mud_range is None or 1 < mud_range[0] <= mud_range[1], "Argument 'mud_range' must be a valid interval with minimum value at least 2"
        assert int(self.width * self.height * cell_percentage / 100) > 1, "The maze must have at least two vertices"

        # Protected attributes
        self._target_nb_vertices = int(self.width * self.height * cell_percentage / 100)
        self._wall_percentage = wall_percentage
        self._mud_percentage = mud_percentage
        self._mud_range = mud_range
        self._random_seed = random_seed
        self._rng = random.Random(self._random_seed)

    #############################################################################################################################################
    #                                                             PROTECTED METHODS                                                             #
    #############################################################################################################################################

    @override
    def _create_maze ( self: Self,
                     ) ->    None:

        """
            This method redefines the abstract method of the parent class.
            It creates a random maze using the parameters given at initialization.
            It should be called by the constructor of the child classes.
            In:
                * self: Reference to the current object.
            Out:
                * None.
        """

        # Add cells, walls, and mud
        self._add_cells()
        self._add_walls()
        self._add_mud()

    #############################################################################################################################################

    @abc.abstractmethod
    def _add_cells ( self: Self,
                   ) ->    None:

        """
            This method is abstract and must be implemented in the subclasses.
            It should add cells to the maze.
            In:
                * self: Reference to the current object.
            Out:
                * None.
        """

        # This method must be implemented in the child classes
        # By default we raise an error
        raise NotImplementedError("This method must be implemented in the child classes.")

    #############################################################################################################################################

    def _add_walls ( self: Self,
                   ) ->    None:

        """
            This method adds walls to the maze.
            It uses the minimum spanning tree to determine the maximum number of walls.
            In:
                * self: Reference to the current object.
            Out:
                * None.
        """

        # Determine the maximum number of walls by computing the minimum spanning tree
        mst = self.minimum_spanning_tree(self._rng.randint(0, sys.maxsize))
        target_nb_walls = int((self.nb_edges - mst.nb_edges) * self._wall_percentage / 100)
        walls = []
        for vertex, neighbor in self.edges:
            if not mst.has_edge(vertex, neighbor):
                self.remove_edge(vertex, neighbor, True)
                walls.append((vertex, neighbor))
        
        # Remove some walls until the desired density is reached
        self._rng.shuffle(walls)
        for vertex, neighbor in walls[target_nb_walls:]:
            self.add_edge(vertex, neighbor)

    #############################################################################################################################################

    def _add_mud ( self: Self,
                 ) ->    None:

        """
            This method adds mud to the maze.
            It replaces some edges with weighted ones.
            In:
                * self: Reference to the current object.
            Out:
                * None.
        """

        # Determine the number of mud edges
        target_nb_mud = int(self.nb_edges * self._mud_percentage / 100)

        # Add mud to some edges
        edges = self.edges
        self._rng.shuffle(edges)
        for vertex, neighbor in edges[:target_nb_mud]:
            self.remove_edge(vertex, neighbor, True)
            weight = self._rng.randint(self._mud_range[0], self._mud_range[1])
            self.add_edge(vertex, neighbor, weight)

#####################################################################################################################################################
#####################################################################################################################################################