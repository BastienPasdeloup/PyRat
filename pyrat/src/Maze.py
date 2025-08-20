#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# Please import necessary elements using the following syntax:
#     from pyrat import <element_name>

"""
This module provides a base class for mazes.
It defines the basic structure and methods for a maze, which is a specific type of graph.
In a maze, each vertex is placed on a grid and can only be connected along the cardinal directions.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
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
    *(This class inherits from* ``Graph`` *).*

    A maze is a particular type of graph.
    Each vertex is a cell, indexed by a number from 0 to ``width*height-1``.
    There are edges between adjacent cells.
    Weights indicate the number of actions required to go from one cell to an adjacent one.
    In this implementation, cells are placed on a grid and can only be connected along the cardinal directions.
    """

    #############################################################################################################################################
    #                                                               MAGIC METHODS                                                               #
    #############################################################################################################################################

    def __init__ ( self,
                   width:    int | None = None,
                   height:   int | None = None,
                   *args:    object,
                   **kwargs: object
                 ) ->        None:

        """
        *(This class is abstract and meant to be subclassed, not instantiated directly).*

        Initializes a new instance of the class.

        Args:
            width:    Width of the maze, can be ``None`` if determined later.
            height:   Height of the maze, can be ``None`` if determined later.
            *args:    Additional arguments to pass to the parent constructor.
            **kwargs: Additional keyword arguments to pass to the parent constructor.
        """

        # Inherit from parent class
        super().__init__(*args, **kwargs)
        
        # Debug
        assert isinstance(width, (int, type(None))), "Argument 'width' must be an integer or None"
        assert isinstance(height, (int, type(None))), "Argument 'height' must be an integer or None"
        assert width is None or width > 0, "Width must be positive"
        assert height is None or height > 0, "Height must be positive"
        assert (width is None and height is None) or width * height >= 2, "The maze must have at least 2 cells"

        # Protected attributes
        self._width = width
        self._height = height

    #############################################################################################################################################

    def __str__ (self) -> str:

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

    def add_edge ( self,
                   vertex_1: int,
                   vertex_2: int,
                   weight:   int = 1
                 ) ->        None:

        """
        *(This method redefines the method of the parent class with the same name).*

        Adds an edge between two vertices in the maze.
        Here, we want edges to link only cells that are above or below.
        Also, weights should be positive integers.
        Edges are symmetric by default.

        Args:
            vertex_1: First vertex.
            vertex_2: Second vertex.
            weight:   Weight of the edge.
        """
        
        # Debug
        assert isinstance(vertex_1, int), "Argument 'vertex_1' must be an integer"
        assert isinstance(vertex_2, int), "Argument 'vertex_2' must be an integer"
        assert isinstance(weight, int), "Argument 'weight' must be an integer"
        assert self.i_exists(vertex_1), "Vertex 1 is not in the maze"
        assert self.i_exists(vertex_2), "Vertex 2 is not in the maze"
        assert self.coords_difference(vertex_1, vertex_2) in [(0, 1), (0, -1), (1, 0), (-1, 0)], "Vertices are not adjacent"

        # If the symmetric edge already exists, we do not add it
        if self.has_edge(vertex_2, vertex_1):
            return

        # Add edge to the graph using the parent's method
        super().add_edge(vertex_1, vertex_2, weight, True)
    
    #############################################################################################################################################

    def add_vertex ( self,
                     vertex: int
                   ) ->      None:

        """
        *(This method redefines the method of the parent class with the same name).*

        Adds a vertex to the maze.
        Only integer vertices are allowed in a maze.

        Args:
            vertex: Vertex to add.
        """
        
        # Debug
        assert isinstance(vertex, int), "Argument 'vertex' must be an integer"

        # Add vertex to the graph using the parent's method
        super().add_vertex(vertex)
        
    #############################################################################################################################################

    def as_numpy_ndarray (self) -> object:

        """
        *(This method redefines the method of the parent class with the same name).*

        Returns a ``numpy.ndarray`` representing the graph.
        Entries are given in order of the indices of the vertices.

        Returns:
            A ``numpy.ndarray`` representing the adjacency matrix (return type is ``object`` to allow ``numpy`` to be optional).
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

    def as_torch_tensor (self) -> object:

        """
        *(This method redefines the method of the parent class with the same name).*

        Returns a ``torch.tensor`` representing the graph.
        Entries are given in order of the indices of the vertices.

        Returns:
            A ``torch.tensor`` representing the adjacency matrix (return type is ``Any`` to allow ``torch`` to be optional).
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

    def coords_difference ( self,
                            vertex_1: int,
                            vertex_2: int,
                          ) ->        tuple[int, int]:
        
        """
        Computes the difference between the coordinates of two cells.

        Args:
            vertex_1: First cell.
            vertex_2: Second cell.

        Returns:
            Tuple containing ``(row_diff, col_diff)`` difference between the rows and columns of the cells.
        """
        
        # Debug
        assert isinstance(vertex_1, int), "Argument 'vertex_1' must be an integer"
        assert isinstance(vertex_2, int), "Argument 'vertex_2' must be an integer"
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

    def get_height (self) -> int:
        
        """
        Returns the height of the maze.
        This is the number of cells in a column.

        Returns:
            Height of the maze, in number of cells.
        """

        # Debug
        assert isinstance(self._height, int), "Height has not yet been set or inferred"

        # Return the attribute
        return self._height

    #############################################################################################################################################

    def get_width (self) -> int:
        
        """
        Returns the width of the maze.
        This is the number of cells in a row.

        Returns:
            Width of the maze, in number of cells.
        """

        # Debug
        assert isinstance(self._width, int), "Width has not yet been set or inferred"

        # Return the attribute
        return self._width

    #############################################################################################################################################
    
    def i_exists ( self,
                   index: int
                 ) ->     bool:
        
        """
        Checks if a given index is a valid cell in the maze.

        Args:
            index: Index of the cell.

        Returns:
            ``True`` if the cell exists, ``False`` otherwise.
        """
        
        # Debug
        assert isinstance(index, int), "Argument 'index' must be an integer"

        # Check if the cell exists
        exists = index in self.get_vertices()
        return exists
    
    #############################################################################################################################################

    def i_to_rc ( self,
                  index: int,
                ) ->     tuple[int, int]:
        
        """
        Transforms a maze index into a ``(row, col)`` pair.
        Does not check if the cell exists.

        Args:
            index: Index of the cell.

        Returns:
            Tuple containing ``(row, col)`` of the cell.
        """
        
        # Debug
        assert isinstance(index, int), "Argument 'index' must be an integer"

        # Conversion
        row = index // self.get_width()
        col = index % self.get_width()
        return row, col
    
    #############################################################################################################################################
    
    def rc_exists ( self,
                    row: int,
                    col: int,
                  ) ->   bool:
        
        """
        Checks if a given ``(row, col)`` pair corresponds to a valid cell in the maze.

        Args:
            row: Row of the cell.
            col: Column of the cell.

        Returns:
            ``True`` if the cell exists, ``False`` otherwise.
        """
        
        # Debug
        assert isinstance(row, int), "Argument 'row' must be an integer"
        assert isinstance(col, int), "Argument 'col' must be an integer"

        # Check if the cell exists
        exists = 0 <= row < self.get_height() and 0 <= col < self.get_width() and self.rc_to_i(row, col) in self.get_vertices()
        return exists
    
    #############################################################################################################################################

    def rc_to_i ( self,
                  row: int,
                  col: int,
                ) ->   int:

        """
        Transforms a ``(row, col)`` pair of maze coordinates (lexicographic order) into a maze index.
        Does not check if the cell exists.

        Args:
            row: Row of the cell.
            col: Column of the cell.

        Returns:
            Corresponding cell index in the maze.
        """
        
        # Debug
        assert isinstance(row, int), "Argument 'row' must be an integer"
        assert isinstance(col, int), "Argument 'col' must be an integer"

        # Conversion
        index = row * self.get_width() + col
        return index
    
    #############################################################################################################################################

    def locations_to_action ( self,
                              source: int,
                              target: int
                            ) ->      Action | None:

        """
        Transforms two locations into the action required to reach the target from the source.

        Args:
            source: Vertex where the player is.
            target: Vertex where the character wants to go.

        Returns:
            Value of the ``Action`` enumeration to go from the source to the target, or ``None`` if the move is impossible.
        """

        # Debug
        assert isinstance(source, int), "Argument 'source' must be an integer"
        assert isinstance(target, int), "Argument 'target' must be an integer"
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

    def locations_to_actions ( self,
                               locations: list[int]
                             ) ->         list[Action | None]:

        """
        Transforms a list of locations into a list of actions to go from one location to the next.

        Args:
            locations: List of vertices to go through.

        Returns:
            Series of values from the ``Action`` enumeration to go from one location to the next.
        """

        # Debug
        assert isinstance(locations, list), "Argument 'locations' must be a list"
        assert all(isinstance(location, int) for location in locations), "All elements of 'locations' must be integers"
        assert all(self.i_exists(location) for location in locations), "Some locations are not in the maze"
        assert None not in [self.locations_to_action(locations[i], locations[i+1]) for i in range(len(locations) - 1)], "Some moves are impossible"

        # Get the actions
        actions = [self.locations_to_action(locations[i], locations[i+1]) for i in range(len(locations) - 1)]
        return actions

    #############################################################################################################################################
    #                                                             PROTECTED METHODS                                                             #
    #############################################################################################################################################

    @abc.abstractmethod
    def _create_maze (self) -> None:
        
        """
        *(This method is abstract and must be implemented in the subclasses).*

        It should be responsible for creating the maze and, if needed, setting the ``width`` and ``height`` attributes.
        It should be called at some point by the subclass.

        Raises:
            NotImplementedError: If the method is not implemented in the subclass.
        """

        # This method must be implemented in the child classes
        # By default we raise an error
        raise NotImplementedError("This method must be implemented in the child classes.")

#####################################################################################################################################################
#####################################################################################################################################################
