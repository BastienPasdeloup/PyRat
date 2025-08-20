#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# Please import necessary elements using the following syntax:
#     from pyrat import <element_name>

"""
This module provides a graph structure that can be used to represent mazes, networks, or any other graph-like structure.
It can be manipulated using the methods defined below.
These methods allow to add and remove vertices and edges, check for the existence of edges, get neighbors of a vertex, etc.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
from collections.abc import Hashable
import random
import sys

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

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class Graph ():

    """
    A graph is a mathematical structure that models pairwise relations between objects.
    It is implemented using an adjacency dictionary.
    We assume that all vertices are hashable.
    The keys of the dictionary are the vertices of the graph.
    The values of the dictionary are dictionaries themselves.
    The keys of these dictionaries are the neighbors of the corresponding vertex.
    The values of these dictionaries are the weights of the corresponding edges.
    This structure should be manipulated using the methods defined below and not directly.

    This class provides generic methods to manipulate any graph.
    For more specific graphs, such as mazes, you should use the classes that inherit from this class.
    """

    #############################################################################################################################################
    #                                                               MAGIC METHODS                                                               #
    #############################################################################################################################################

    def __init__ (self) -> None:

        """
        Initializes a new instance of the class.
        This constructor initializes the internal adjacency dictionary.
        """

        # Private attributes
        self.__adjacency = {}

    #############################################################################################################################################

    def __str__ (self) -> str:

        """
        Returns a string representation of the object.

        Returns:
            String representation of the object.
        """
        
        # Create the string
        string = "Graph object:\n"
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
                   vertex_1:  Hashable,
                   vertex_2:  Hashable,
                   weight:    float | int = 1,
                   symmetric: bool = False
                 ) ->         None:

        """
        Adds an edge to the graph.

        Args:
            vertex_1:  First vertex.
            vertex_2:  Second vertex.
            weight:    Weight of the edge. Defaults to 1.
            symmetric: Whether the edge is symmetric (undirected). Defaults to False.
        """
        
        # Debug
        assert isinstance(vertex_1, Hashable), "Argument 'vertex_1' must be hashable"
        assert isinstance(vertex_2, Hashable), "Argument 'vertex_2' must be hashable"
        assert isinstance(weight, (float, int)), "Argument 'weight' must be a real number"
        assert isinstance(symmetric, bool), "Argument 'symmetric' must be a boolean"
        assert vertex_1 in self.__adjacency, "Vertex 1 not in the graph"
        assert vertex_2 in self.__adjacency, "Vertex 2 not in the graph"
        assert not self.has_edge(vertex_1, vertex_2), "Edge already exists"
        assert not (symmetric and self.has_edge(vertex_2, vertex_1)), "Symmetric edge already exists"

        # Add edge to the adjacency dictionary
        self.__adjacency[vertex_1][vertex_2] = weight
        if symmetric:
            self.__adjacency[vertex_2][vertex_1] = weight
    
    #############################################################################################################################################

    def add_vertex ( self,
                     vertex: Hashable
                   ) ->      None:
        
        """
        Adds a vertex to the graph.

        Args:
            vertex: The vertex to add.
        """
        
        # Debug
        assert isinstance(vertex, Hashable), "Argument 'vertex' must be hashable"
        assert vertex not in self.__adjacency, "Vertex already in the graph"

        # Add vertex to the adjacency matrix
        self.__adjacency[vertex] = {}
        
    #############################################################################################################################################

    def as_dict (self) -> dict[Hashable, dict[Hashable, float | int]]:

        """
        Returns a dictionary representing the adjacency matrix.

        Returns:
            Dictionary representing the adjacency matrix.
        """
        
        # Make a copy of the adjacency matrix
        adjacency_dict = self.__adjacency.copy()
        return adjacency_dict
        
    #############################################################################################################################################

    def as_numpy_ndarray (self) -> object:

        """
        Returns a ``numpy.ndarray`` representing the graph.
        Entries are given in order in which vertices appear in the adjacency dictionary.

        Returns:
            A ``numpy.ndarray`` representing the adjacency matrix (return type is ``object`` to allow ``numpy`` to be optional).
        """
        
        # Debug
        assert "numpy" in globals(), "Numpy is not available"

        # Create the adjacency matrix
        adjacency_matrix = numpy.zeros((self.nb_vertices(), self.nb_vertices()), dtype=int)
        for i, vertex_1 in enumerate(self.__adjacency):
            for j, vertex_2 in enumerate(self.__adjacency):
                if self.has_edge(vertex_1, vertex_2):
                    adjacency_matrix[i, j] = self.get_weight(vertex_1, vertex_2)
        return adjacency_matrix

    #############################################################################################################################################

    def as_torch_tensor (self) -> object:

        """
        Returns a ``torch.tensor`` representing the graph.
        Entries are given in order in which vertices appear in the adjacency dictionary

        Returns:
            A ``torch.tensor`` representing the adjacency matrix (return type is ``object`` to allow ``torch`` to be optional).
        """
        
        # Debug
        assert "torch" in globals(), "Torch is not available"

        # Create the adjacency matrix
        adjacency_matrix = torch.zeros((self.nb_vertices(), self.nb_vertices()), dtype=int)
        for i, vertex_1 in enumerate(self.__adjacency):
            for j, vertex_2 in enumerate(self.__adjacency):
                if self.has_edge(vertex_1, vertex_2):
                    adjacency_matrix[i, j] = self.get_weight(vertex_1, vertex_2)
        return adjacency_matrix

    #############################################################################################################################################

    def edge_is_symmetric ( self,
                            vertex_1: Hashable,
                            vertex_2: Hashable,
                          ) ->        bool:
        
        """
        Checks whether an edge is symmetric.

        Args:
            vertex_1: First vertex.
            vertex_2: Second vertex.

        Returns:
            Whether the edge is symmetric.
        """

        # Debug
        assert isinstance(vertex_1, Hashable), "Argument 'vertex_1' must be hashable"
        assert isinstance(vertex_2, Hashable), "Argument 'vertex_2' must be hashable"
        assert vertex_1 in self.__adjacency, "Vertex 1 not in the graph"
        assert vertex_2 in self.__adjacency, "Vertex 2 not in the graph"
        assert self.has_edge(vertex_1, vertex_2), "Edge does not exist"

        # Check whether the edge is symmetric
        symmetric = self.has_edge(vertex_2, vertex_1)
        return symmetric

    #############################################################################################################################################

    def get_edges (self) -> list[tuple[Hashable, Hashable]]:

        """
        Returns the list of edges in the graph.
        Symmetric edges are counted once.

        Returns:
            List of edges in the graph, as tuples ``(vertex_1, vertex_2)``.
        """
        
        # Get the list of edges
        edge_list = []
        for vertex_1 in self.get_vertices():
            for vertex_2 in self.get_neighbors(vertex_1):
                if (vertex_2, vertex_1) not in edge_list:
                    edge_list.append((vertex_1, vertex_2))
        return edge_list
    
    #############################################################################################################################################

    def get_neighbors ( self,
                        vertex: Hashable
                      ) ->      list[Hashable]:

        """
        Returns the list of neighbors of a vertex.

        Args:
            vertex: Vertex of which to get neighbors.

        Returns:
            List of neighbors of the vertex.
        """
        
        # Debug
        assert isinstance(vertex, Hashable), "Argument 'vertex' must be hashable"
        assert vertex in self.__adjacency, "Vertex not in the graph"

        # Get neighbors
        neighbors = list(self.__adjacency[vertex].keys())
        return neighbors

    #############################################################################################################################################

    def get_vertices (self) -> list[Hashable]:
        
        """
        Returns the list of vertices in the graph.

        Returns:
            List of vertices in the graph.
        """

        # Get the list of vertices
        vertices = list(self.__adjacency.keys())
        return vertices

    #############################################################################################################################################

    def get_weight ( self,
                     vertex_1: Hashable,
                     vertex_2: Hashable
                   ) ->        float | int:

        """
        Returns the weight of an edge.

        Args:
            vertex_1: First vertex.
            vertex_2: Second vertex.

        Returns:
            Weight of the edge.
        """
        
        # Debug
        assert isinstance(vertex_1, Hashable), "Argument 'vertex_1' must be hashable"
        assert isinstance(vertex_2, Hashable), "Argument 'vertex_2' must be hashable"
        assert vertex_1 in self.__adjacency, "Vertex 1 not in the graph"
        assert vertex_2 in self.__adjacency, "Vertex 2 not in the graph"
        assert self.has_edge(vertex_1, vertex_2), "Edge does not exist"

        # Get weight
        weight = self.__adjacency[vertex_1][vertex_2]
        return weight

    #############################################################################################################################################

    def has_edge ( self,
                   vertex_1: Hashable,
                   vertex_2: Hashable,
                 ) ->        bool:
        
        """
        Checks whether an edge exists between two vertices.

        Args:
            vertex_1: First vertex.
            vertex_2: Second vertex.

        Returns:
            Whether an edge exists between the two vertices.
        """

        # Debug
        assert isinstance(vertex_1, Hashable), "Argument 'vertex_1' must be hashable"
        assert isinstance(vertex_2, Hashable), "Argument 'vertex_2' must be hashable"
        assert vertex_1 in self.__adjacency, "Vertex 1 not in the graph"
        assert vertex_2 in self.__adjacency, "Vertex 2 not in the graph"

        # Check whether the edge exists
        edge_exists = vertex_2 in self.get_neighbors(vertex_1)
        return edge_exists

    #############################################################################################################################################

    def is_connected (self) -> bool:

        """
        Checks whether the graph is connected using a depth-first search.

        Returns:
            ``True`` if the graph is connected, ``False`` otherwise.
        """
        
        # Debug
        assert self.nb_vertices() > 0, "Graph is empty"

        # Create a list of visited vertices
        vertices = list(self.get_vertices())
        visited = {vertex: False for vertex in self.__adjacency}
        visited[vertices[0]] = True
        stack = [vertices[0]]
                
        # Depth-first search
        while stack:
            vertex = stack.pop()
            for neighbor in self.get_neighbors(vertex):
                if not visited[neighbor]:
                    visited[neighbor] = True
                    stack.append(neighbor)
        
        # Check if all vertices have been visited
        connected = all(visited.values())
        return connected

    #############################################################################################################################################

    def minimum_spanning_tree ( self,
                                random_seed: int | None = None
                              ) ->           "Graph":

        """
        Returns the minimum spanning tree of the graph.

        Args:
            random_seed: Seed for the random number generator.

        Returns:
            Graph representing the minimum spanning tree.
        """
        
        # Debug
        assert random_seed is None or isinstance(random_seed, int), "Argument 'random_seed' must be an integer"
        assert random_seed is None or 0 <= random_seed < sys.maxsize, "Argument 'random_seed' must be non-negative"

        # Initialize a random number generator
        rng = random.Random(random_seed)

        # Shuffle vertices
        vertices_to_add = self.get_vertices()
        rng.shuffle(vertices_to_add)

        # Create the minimum spanning tree, initialized with a random vertex
        mst = Graph()
        vertex = vertices_to_add.pop(0)
        mst.add_vertex(vertex)
        
        # Add vertices until all are included
        while vertices_to_add:
            vertex = vertices_to_add.pop(0)
            neighbors = self.get_neighbors(vertex)
            rng.shuffle(neighbors)
            neighbors_in_mst = [neighbor for neighbor in neighbors if neighbor in mst.get_vertices()]
            if neighbors_in_mst:
                neighbor = neighbors_in_mst[0]
                symmetric = self.edge_is_symmetric(vertex, neighbor)
                weight = self.get_weight(neighbor, vertex)
                mst.add_vertex(vertex)
                mst.add_edge(vertex, neighbor, weight, symmetric)
            else:
                vertices_to_add.append(vertex)

        # Return the minimum spanning tree
        return mst

    #############################################################################################################################################

    def nb_edges (self) -> int:
    
        """
        Returns the number of edges in the graph.
        Symmetric edges are counted once.

        Returns:
            Number of edges in the graph.
        """
        
        # Get the number of edges
        nb = len(self.get_edges())
        return nb

    #############################################################################################################################################

    def nb_vertices (self) -> int:

        """
        Returns the number of vertices in the graph.

        Returns:
            Number of vertices in the graph.
        """
        
        # Get the number of vertices
        nb = len(self.__adjacency)
        return nb

    #############################################################################################################################################

    def remove_edge ( self,
                      vertex_1:  Hashable,
                      vertex_2:  Hashable,
                      symmetric: bool = False
                    ) ->         None:

        """
        Removes an edge from the graph.

        Args:
            vertex_1:  First vertex.
            vertex_2:  Second vertex.
            symmetric: Whether to also delete the symmetric edge. Defaults to False.
        """
        
        # Debug
        assert isinstance(vertex_1, Hashable), "Argument 'vertex_1' must be hashable"
        assert isinstance(vertex_2, Hashable), "Argument 'vertex_2' must be hashable"
        assert isinstance(symmetric, bool), "Argument 'symmetric' must be a boolean"
        assert vertex_1 in self.__adjacency, "Vertex 1 not in the graph"
        assert vertex_2 in self.__adjacency, "Vertex 2 not in the graph"
        assert self.has_edge(vertex_1, vertex_2), "Edge does not exist"
        assert (not symmetric) or (symmetric and self.edge_is_symmetric(vertex_1, vertex_2)), "Symmetric edge does not exist"

        # Remove edge and symmetric
        del self.__adjacency[vertex_1][vertex_2]
        if symmetric:
            del self.__adjacency[vertex_2][vertex_1]

    #############################################################################################################################################

    def remove_vertex ( self,
                        vertex: Hashable
                      ) ->      None:

        """
        Removes a vertex from the graph.
        Also removes all edges connected to this vertex.

        Args:
            vertex: Vertex to remove.
        """
        
        # Debug
        assert isinstance(vertex, Hashable), "Argument 'vertex' must be hashable"
        assert vertex in self.__adjacency, "Vertex not in the graph"

        # Remove the vertex and connections to it
        for neighbor in self.__adjacency:
            if vertex in self.__adjacency[neighbor]:
                del self.__adjacency[neighbor][vertex]
        del self.__adjacency[vertex]
        
#####################################################################################################################################################
#####################################################################################################################################################
