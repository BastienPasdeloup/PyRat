#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# Please import necessary elements using the following syntax:
#     from pyrat import <element_name>

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
from typing import *
from typing_extensions import *
from numbers import *
import abc

# Numpy is an optional dependency
try:
    import numpy
except ImportError:
    pass

# Torch is an optional dependency
try:
    import torch
except ImportError:
    pass

# PyRat imports
from pyrat.src.Graph import Graph
from pyrat.src.enums import Action

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class Maze (Graph, abc.ABC):

    """
    This class inherits from the Graph class.
    Therefore, it has the attributes and methods defined in the Graph class in addition to the ones defined below.
    
    This class is abstract and cannot be instantiated.
    You should use one of the subclasses to create a maze, or create your own subclass.
    
    A maze is a particular type of graph.
    Each vertex is a cell, indexed by a number from 0 to width*height-1.
    There are edges between adjacent cells.
    Weights indicate the number of actions required to go from one cell to an adjacent one.
    In this implementation, cells are placed on a grid and can only be connected along the cardinal directions.
    """

    #############################################################################################################################################
    #                                                               MAGIC METHODS                                                               #
    #############################################################################################################################################

    def __init__ ( self:     Self,
                   width:    Optional[Integral] = None,
                   height:   Optional[Integral] = None,
                   *args:    Any,
                   **kwargs: Any
                 ) ->        None:

        """
        Initializes a new instance of the class.

        Args:
            width:    Width of the maze, can be None if determined later.
            height:   Height of the maze, can be None if determined later.
            *args:    Additional arguments to pass to the parent constructor.
            **kwargs: Additional keyword arguments to pass to the parent constructor.
        """

        # Inherit from parent class
        super().__init__(*args, **kwargs)
        
        # Debug
        assert isinstance(width, (Integral, type(None))), "Argument 'width' must be an integer or None"
        assert isinstance(height, (Integral, type(None))), "Argument 'height' must be an integer or None"
        assert width is None or width > 0, "Width must be positive"
        assert height is None or height > 0, "Height must be positive"
        assert (width is None and height is None) or width * height >= 2, "The maze must have at least 2 cells"

        # Protected attributes
        self._width = width
        self._height = height

    #############################################################################################################################################

    def __str__ ( self: Self,
                ) ->    str:

        """
        Returns a string representation of the object.
        Defines what is shown when calling print on the object.

        Returns:
            String representation of the object.
        """
        
        # Create the string
        string = "Maze object:\n"
        string += "|  Width: {}\n".format(self.get_width())
        string += "|  Height: {}\n".format(self.get_height())
        string += "|  Vertices: {}\n".format(self.get_vertices())
        string += "|  Adjacency matrix:\n"
        for vertex_1, vertex_2 in self.get_edges():
            weight = self.get_weight(vertex_1, vertex_2)
            symmetric = self.edge_is_symmetric(vertex_1, vertex_2)
            string += "|  |  {} {} ({}) --> {}\n".format(vertex_1, "<--" if symmetric else "---", weight, vertex_2)
        return string.strip()

    #############################################################################################################################################
    #                                                               PUBLIC METHODS                                                              #
    #############################################################################################################################################

    def i_to_rc ( self:  Self,
                  index: Integral,
                ) ->     Tuple[Integral, Integral]:
        
        """
        Transforms a maze index into a (row, col) pair.
        Does not check if the cell exists.

        Args:
            index: Index of the cell.

        Returns:
            Tuple containing (row, col) of the cell.
        """
        
        # Debug
        assert isinstance(index, Integral), "Argument 'index' must be an integer"

        # Conversion
        row = index // self.get_width()
        col = index % self.get_width()
        return row, col
    
    #############################################################################################################################################

    def get_width ( self: Self
                  ) ->    Integral:
        
        """
        Returns the width of the maze.
        This is the number of cells in a row.

        Returns:
            Width of the maze.
        """

        # Debug
        assert isinstance(self._width, Integral), "Width has not yet been set or inferred"

        # Return the attribute
        return self._width

    #############################################################################################################################################
    
    def get_height ( self: Self
                   ) ->    Integral:
        
        """
        Returns the height of the maze.
        This is the number of cells in a column.

        Returns:
            Height of the maze.
        """

        # Debug
        assert isinstance(self._height, Integral), "Height has not yet been set or inferred"

        # Return the attribute
        return self._height

    #############################################################################################################################################
    
    def rc_to_i ( self: Self,
                  row:  Integral,
                  col:  Integral,
                ) ->    Integral:
        
        """
        Transforms a (row, col) pair of maze coordinates (lexicographic order) into a maze index.
        Does not check if the cell exists.

        Args:
            row: Row of the cell.
            col: Column of the cell.

        Returns:
            Corresponding cell index in the maze.
        """
        
        # Debug
        assert isinstance(row, Integral), "Argument 'row' must be an integer"
        assert isinstance(col, Integral), "Argument 'col' must be an integer"

        # Conversion
        index = row * self.get_width() + col
        return index
    
    #############################################################################################################################################
    
    def rc_exists ( self: Self,
                    row:  Integral,
                    col:  Integral,
                  ) ->    bool:
        
        """
        Checks if a given (row, col) pair corresponds to a valid cell in the maze.

        Args:
            row: Row of the cell.
            col: Column of the cell.

        Returns:
            True if the cell exists, False otherwise.
        """
        
        # Debug
        assert isinstance(row, Integral), "Argument 'row' must be an integer"
        assert isinstance(col, Integral), "Argument 'col' must be an integer"

        # Check if the cell exists
        exists = 0 <= row < self.get_height() and 0 <= col < self.get_width() and self.rc_to_i(row, col) in self.get_vertices()
        return exists
    
    #############################################################################################################################################
    
    def i_exists ( self:  Self,
                   index: Integral
                 ) ->     bool:
        
        """
        Checks if a given index is a valid cell in the maze.

        Args:
            index: Index of the cell.

        Returns:
            True if the cell exists, False otherwise.
        """
        
        # Debug
        assert isinstance(index, Integral), "Argument 'index' must be an integer"

        # Check if the cell exists
        exists = index in self.get_vertices()
        return exists
    
    #############################################################################################################################################

    def coords_difference ( self:     Self,
                            vertex_1: Integral,
                            vertex_2: Integral,
                          ) ->        Tuple[Integral, Integral]:
        
        """
        Computes the difference between the coordinates of two cells.

        Args:
            vertex_1: First cell.
            vertex_2: Second cell.

        Returns:
            Tuple containing (row_diff, col_diff) difference between the rows and columns of the cells.
        """
        
        # Debug
        assert isinstance(vertex_1, Integral), "Argument 'vertex_1' must be an integer"
        assert isinstance(vertex_2, Integral), "Argument 'vertex_2' must be an integer"
        assert self.i_exists(vertex_1), "Vertex 1 is not in the maze"
        assert self.i_exists(vertex_2), "Vertex 2 is not in the maze"

        # Get coordinates
        row_1, col_1 = self.i_to_rc(vertex_1)
        row_2, col_2 = self.i_to_rc(vertex_2)

        # Compute difference
        row_diff = row_2 - row_1
        col_diff = col_2 - col_1
        return row_diff, col_diff
    
    #############################################################################################################################################

    def add_vertex ( self:   Self,
                     vertex: Integral
                   ) ->      None:

        """
        Redefines the method of the parent class.
        Only integer vertices are allowed in a maze.

        Args:
            vertex: Vertex to add.
        """
        
        # Debug
        assert isinstance(vertex, Integral), "Argument 'vertex' must be an integer"

        # Add vertex to the graph using the parent's method
        super().add_vertex(vertex)
        
    #############################################################################################################################################

    def add_edge ( self:     Self,
                   vertex_1: Integral,
                   vertex_2: Integral,
                   weight:   Integral = 1
                 ) ->        None:

        """
        Redefines the method of the parent class.
        Here, we want edges to link only cells that are above or below.
        Also, weights should be positive integers.
        Edges are symmetric by default.
        We do not duplicate asserts already made in the parent method.

        Args:
            vertex_1: First vertex.
            vertex_2: Second vertex.
            weight:   Weight of the edge.
        """
        
        # Debug
        assert isinstance(vertex_1, Integral), "Argument 'vertex_1' must be an integer"
        assert isinstance(vertex_2, Integral), "Argument 'vertex_2' must be an integer"
        assert isinstance(weight, Integral), "Argument 'weight' must be an integer"
        assert self.i_exists(vertex_1), "Vertex 1 is not in the maze"
        assert self.i_exists(vertex_2), "Vertex 2 is not in the maze"
        assert self.coords_difference(vertex_1, vertex_2) in [(0, 1), (0, -1), (1, 0), (-1, 0)], "Vertices are not adjacent"

        # If the symmetric edge already exists, we do not add it
        if self.has_edge(vertex_2, vertex_1):
            return

        # Add edge to the graph using the parent's method
        super().add_edge(vertex_1, vertex_2, weight, True)
    
    #############################################################################################################################################

    def as_numpy_ndarray ( self: Self,
                         ) ->    Any:

        """
        Returns a numpy ndarray representing the maze adjacency matrix.
        Each entry corresponds to the weight of the edge between two cells.

        Returns:
            Numpy ndarray representing the adjacency matrix.
        """
        
        # Debug
        assert "numpy" in globals(), "Numpy is not available"

        # Create the adjacency matrix
        adjacency_matrix = numpy.zeros((self.get_width() * self.get_height(), self.get_width() * self.get_height()), dtype=int)
        for vertex in self.get_vertices():
            for neighbor in self.get_neighbors(vertex):
                adjacency_matrix[vertex, neighbor] = self.get_weight(vertex, neighbor)
        return adjacency_matrix

    #############################################################################################################################################

    def as_torch_tensor ( self: Self,
                        ) ->    Any:

        """
        Returns a torch tensor representing the maze adjacency matrix.
        Each entry corresponds to the weight of the edge between two cells.

        Returns:
            Torch tensor representing the adjacency matrix.
        """
        
        # Debug
        assert "torch" in globals(), "Torch is not available"

        # Create the adjacency matrix
        adjacency_matrix = torch.zeros((self.get_width() * self.get_height(), self.get_width() * self.get_height()), dtype=torch.int)
        for vertex in self.get_vertices():
            for neighbor in self.get_neighbors(vertex):
                adjacency_matrix[vertex, neighbor] = self.get_weight(vertex, neighbor)
        return adjacency_matrix

    #############################################################################################################################################

    def locations_to_action ( self:   Self,
                              source: Integral,
                              target: Integral
                            ) ->      Optional[Action]: 

        """
        Transforms two locations into the action required to reach the target from the source.

        Args:
            source: Vertex where the player is.
            target: Vertex where the character wants to go.

        Returns:
            Action to go from the source to the target, or None if the move is impossible.
        """

        # Debug
        assert isinstance(source, Integral), "Argument 'source' must be an integer"
        assert isinstance(target, Integral), "Argument 'target' must be an integer"
        assert self.i_exists(source), "Source is not in the maze"
        assert self.i_exists(target), "Target is not in the maze"

        # Get the coordinates difference
        difference = self.coords_difference(source, target)

        # Translate in a move
        if difference == (0, 0):
            action = Action.NOTHING
        elif difference == (0, -1):
            action = Action.WEST
        elif difference == (0, 1):
            action = Action.EAST
        elif difference == (1, 0):
            action = Action.SOUTH
        elif difference == (-1, 0):
            action = Action.NORTH
        else:
            action = None
        return action

    #############################################################################################################################################

    def locations_to_actions ( self:      Self,
                               locations: List[Integral]
                             ) ->         List[Optional[Action]]:

        """
        Transforms a list of locations into a list of actions to go from one location to the next.

        Args:
            locations: List of vertices to go through.

        Returns:
            List of actions to go from one location to the next.
        """

        # Debug
        assert isinstance(locations, list), "Argument 'locations' must be a list"
        assert all(isinstance(location, Integral) for location in locations), "All elements of 'locations' must be integers"
        assert all(self.i_exists(location) for location in locations), "Some locations are not in the maze"
        assert None not in [self.locations_to_action(locations[i], locations[i+1]) for i in range(len(locations) - 1)], "Some moves are impossible"

        # Get the actions
        actions = [self.locations_to_action(locations[i], locations[i+1]) for i in range(len(locations) - 1)]
        return actions

    #############################################################################################################################################
    #                                                             PROTECTED METHODS                                                             #
    #############################################################################################################################################

    @abc.abstractmethod
    def _create_maze ( self: Self,
                     ) ->    None:
        
        """
        This method is abstract and must be implemented in the subclasses.
        It should be responsible for creating the maze and, if needed, setting the width and height attributes.
        It should be called at some point by the subclass.
        """

        # This method must be implemented in the child classes
        # By default we raise an error
        raise NotImplementedError("This method must be implemented in the child classes.")

#####################################################################################################################################################
#####################################################################################################################################################
