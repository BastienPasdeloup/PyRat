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
import abc
import numpy
import torch

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
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self:     Self,
                   width:    Optional[Integral] = None,
                   height:   Optional[Integral] = None,
                   *args:    Any,
                   **kwargs: Any
                 ) ->        Self:

        """
            This function is the constructor of the class.
            In:
                * self:   Reference to the current object.
                * width:  Width of the maze, initialized to None in case it is determined afterward.
                * height: Height of the maze, initialized to None in case it is determined afterward.
                * args:   Arguments to pass to the parent constructor.
                * kwargs: Keyword arguments to pass to the parent constructor.
            Out:
                * A new instance of the class.
        """

        # Inherit from parent class
        super().__init__(*args, **kwargs)
        
        # Debug
        assert isinstance(width, (Integral, type(None))) # Type check for width
        assert isinstance(height, (Integral, type(None))) # Type check for height
        assert width is None or width > 0 # Width is positive
        assert height is None or height > 0 # Height is positive
        assert (width is None and height is None) or width * height >= 2 # The maze has at least two vertices

        # Protected attributes
        self._width = width
        self._height = height

    #############################################################################################################################################
    #                                                                  GETTERS                                                                  #
    #############################################################################################################################################

    @property
    def width ( self: Self
              ) ->    Integral:
        
        """
            Getter for _width.
            In:
                * self: Reference to the current object.
            Out:
                * self._width: The _width attribute.
        """

        # Debug
        assert isinstance(self._width, Integral) # Width has been set or inferred previously

        # Return the attribute
        return self._width

    #############################################################################################################################################
    
    @property
    def height ( self: Self
               ) ->    Integral:
        
        """
            Getter for _height.
            In:
                * self: Reference to the current object.
            Out:
                * self._height: The _height attribute.
        """

        # Debug
        assert isinstance(self._height, Integral) # Height has been set or inferred previously

        # Return the attribute
        return self._height

    #############################################################################################################################################
    #                                                               PUBLIC METHODS                                                              #
    #############################################################################################################################################

    def i_to_rc ( self:  Self,
                  index: Integral,
                ) ->     Tuple[Integral, Integral]:
        
        """
            Transforms a maze index in a pair (row, col).
            Does not check if the cell exists.
            In:
                * self:  Reference to the current object.
                * index: Index of the cell.
            Out:
                * row: Row of the cell.
                * col: Column of the cell.
        """
        
        # Debug
        assert isinstance(index, Integral) # Type check for index

        # Conversion
        row = index // self.width
        col = index % self.width
        return row, col
    
    #############################################################################################################################################
    
    def rc_to_i ( self: Self,
                  row:  Integral,
                  col:  Integral,
                ) ->    Integral:
        
        """
            Transforms a (row, col) pair of maze coordiates (lexicographic order) in a maze index.
            Does not check if the cell exists.
            In:
                * self: Reference to the current object.
                * row:  Row of the cell.
                * col:  Column of the cell.
            Out:
                * index: Corresponding cell index in the maze.
        """
        
        # Debug
        assert isinstance(row, Integral) # Type check for row
        assert isinstance(col, Integral) # Type check for col

        # Conversion
        index = row * self.width + col
        return index
    
    #############################################################################################################################################
    
    def rc_exists ( self: Self,
                    row:  Integral,
                    col:  Integral,
                  ) ->    bool:
        
        """
            Checks if a given (row, col) pair corresponds to a valid cell in the maze.
            In:
                * self: Reference to the current object.
                * row:  Row of the cell.
                * col:  Column of the cell.
            Out:
                * exists: True if the cell exists, False otherwise.
        """
        
        # Debug
        assert isinstance(row, Integral) # Type check for row
        assert isinstance(col, Integral) # Type check for col

        # Check if the cell exists
        exists = 0 <= row < self.height and 0 <= col < self.width and self.rc_to_i(row, col) in self.get_vertices()
        return exists
    
    #############################################################################################################################################
    
    def i_exists ( self:  Self,
                   index: Integral
                 ) ->     bool:
        
        """
            Checks if a given index pair is a valid cell in the maze.
            In:
                * self:  Reference to the current object.
                * index: Index of the cell.
            Out:
                * exists: True if the cell exists, False otherwise.
        """
        
        # Debug
        assert isinstance(index, Integral) # Type check for index

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
            In:
                * self:     Reference to the current object.
                * vertex_1: First cell.
                * vertex_2: Second cell.
            Out:
                * row_diff: Difference between the rows of the cells.
                * col_diff: Difference between the columns of the cells.
        """
        
        # Debug
        assert isinstance(vertex_1, Integral) # Type check for vertex_1
        assert isinstance(vertex_2, Integral) # Type check for vertex_2
        assert self.i_exists(vertex_1) # Vertex 1 is in the maze
        assert self.i_exists(vertex_2) # Vertex 2 is in the maze

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
            Here, we want vertices of a maze to be integers only.
            This is a particular type of graph.
            We do not duplicate asserts already made in the parent method.
            In:
                * self:   Reference to the current object.
                * vertex: Vertex to add.
            Out:
                * None.
        """
        
        # Debug
        assert isinstance(vertex, Integral) # Type check for vertex

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
            In:
                * self:     Reference to the current object.
                * vertex_1: First vertex.
                * vertex_2: Second vertex.
                * weight:   Weight of the edge.
            Out:
                * None.
        """
        
        # Debug
        assert isinstance(vertex_1, Integral) # Type check for vertex_1
        assert isinstance(vertex_2, Integral) # Type check for vertex_2
        assert isinstance(weight, Integral) # Type check for weight
        assert self.i_exists(vertex_1) # Vertex 1 is in the maze
        assert self.i_exists(vertex_2) # Vertex 2 is in the maze
        assert self.coords_difference(vertex_1, vertex_2) in [(0, 1), (0, -1), (1, 0), (-1, 0)] # Vertices are adjacent on the grid

        # If the symmetric edge already exists, we do not add it
        if self.has_edge(vertex_2, vertex_1):
            return

        # Add edge to the graph using the parent's method
        super().add_edge(vertex_1, vertex_2, weight, True)
    
    #############################################################################################################################################

    def as_numpy_ndarray ( self: Self,
                         ) ->    numpy.ndarray:

        """
            This redefines a method of the parent class.
            Returns a numpy ndarray representing the maze.
            Here, we have an entry for each cell in the maze.
            In:
                * self: Reference to the current object.
            Out:
                * adjacency_matrix: Numpy ndarray representing the adjacency matrix.
        """
        
        # Create the adjacency matrix
        adjacency_matrix = numpy.zeros((self.width * self.height, self.width * self.height), dtype=int)
        for vertex in self.get_vertices():
            for neighbor in self.get_neighbors(vertex):
                adjacency_matrix[vertex, neighbor] = self.get_weight(vertex, neighbor)
        return adjacency_matrix

    #############################################################################################################################################

    def as_torch_tensor ( self: Self,
                        ) ->    torch.Tensor:

        """
            This redefines a method of the parent class.
            Returns a torch tensor representing the maze.
            Here, we have an entry for each cell in the maze.
            In:
                * self: Reference to the current object.
            Out:
                * adjacency_matrix: Torch tensor representing the adjacency matrix.
        """
        
        # Create the adjacency matrix
        adjacency_matrix = torch.zeros((self.width * self.height, self.width * self.height), dtype=torch.int)
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
            Function to transform two locations into an action to reach the target from the source.
            In:
                * self:   Reference to the current object.
                * source: Vertex on which the player is.
                * target: Vertex where the character wants to go.
            Out:
                * action: Action to go from the source to the target, or None if the move is impossible.
        """

        # Debug
        assert isinstance(source, Integral) # Type check for source
        assert isinstance(target, Integral) # Type check for target
        assert self.i_exists(source) # Source is in the maze
        assert self.i_exists(target) # Target is in the maze

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
    #                                                             PROTECTED METHODS                                                             #
    #############################################################################################################################################

    @abc.abstractmethod
    def _create_maze ( self: Self,
                     ) ->    None:
        
        """
            This method is abstract and must be implemented in the subclasses.
            It should be in charge of creating the maze and, if needed, to set the width and height attributes.
            In:
                * self: Reference to the current object.
            Out:
                * None.
        """

        # This method must be implemented in the child classes
        # By default we raise an error
        raise NotImplementedError("This method must be implemented in the child classes.")

    #############################################################################################################################################
    #                                                              PRIVATE METHODS                                                              #
    #############################################################################################################################################

    def __str__ ( self: Self,
                ) ->    str:

        """
            This method returns a string representation of the object.
            In:
                * self: Reference to the current object.
            Out:
                * string: String representation of the object.
        """
        
        # Create the string
        string = "Maze object:\n"
        string += "|  Width: " + str(self.width) + "\n"
        string += "|  Height: " + str(self.height) + "\n"
        string += "|  Vertices: " + str(self.get_vertices()) + "\n"
        string += "|  Adjacency matrix:\n"
        for vertex_1, vertex_2, weight, symmetric in self.get_edge_list():
            string += "|  |  {} {} ({}) --> {}\n".format(vertex_1, "<--" if symmetric else "---", weight, vertex_2)
        return string.strip()

#####################################################################################################################################################
#####################################################################################################################################################
