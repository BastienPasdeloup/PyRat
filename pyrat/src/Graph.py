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
        It should be manipulated using the methods defined below and not directly.
    """

    #############################################################################################################################################
    #                                                               MAGIC METHODS                                                               #
    #############################################################################################################################################

    def __init__ ( self: Self,
                 ) ->    None:

        """
            This function is the constructor of the class.
            When an object is instantiated, this method is called to initialize the object.
            This is where you should define the attributes of the object and set their initial values.
            In:
                * self: Reference to the current object.
            Out:
                * A new instance of the class (we indicate None as return type per convention, see PEP-484).
        """

        # Private attributes
        self.__adjacency = {}

    #############################################################################################################################################

    def __str__ ( self: Self,
                ) ->    str:

        """
            This method returns a string representation of the object.
            This defines what will be shown when calling print on the object.
            In:
                * self: Reference to the current object.
            Out:
                * string: String representation of the object.
        """
        
        # Create the string
        string = "Graph object:\n"
        string += "|  Vertices: {}\n".format(self.vertices)
        string += "|  Adjacency matrix:\n"
        for vertex_1, vertex_2 in self.edges:
            weight = self.get_weight(vertex_1, vertex_2)
            symmetric = self.edge_is_symmetric(vertex_1, vertex_2)
            string += "|  |  {} {} ({}) --> {}\n".format(vertex_1, "<--" if symmetric else "---", weight, vertex_2)
        return string.strip()

    #############################################################################################################################################
    #                                                            ATTRIBUTE ACCESSORS                                                            #
    #############################################################################################################################################

    @property
    def vertices ( self: Self,
                 ) ->    List[Hashable]:
        
        """
            Returns the list of vertices in the graph.
            In:
                * self: Reference to the current object.
            Out:
                * vertices: List of vertices in the graph.
        """

        # Get the list of vertices
        vertices = list(self.__adjacency.keys())
        return vertices

    #############################################################################################################################################

    @property
    def nb_vertices ( self: Self,
                    ) ->    Integral:

        """
            Returns the number of vertices in the graph.
            In:
                * self: Reference to the current object.
            Out:
                * nb_vertices: Number of vertices in the graph.
        """
        
        # Get the number of vertices
        nb_vertices = len(self.__adjacency)
        return nb_vertices

    #############################################################################################################################################

    @property
    def edges ( self: Self,
              ) ->    List[Tuple[Hashable, Hashable]]:

        """
            Returns the list of edges in the graph.
            Symmetric edges are counted once.
            In:
                * self: Reference to the current object.
            Out:
                * edge_list: List of edges in the graph, as tuples (vertex_1, vertex_2).
        """
        
        # Get the list of edges
        edge_list = []
        for vertex_1 in self.vertices:
            for vertex_2 in self.get_neighbors(vertex_1):
                if (vertex_2, vertex_1) not in edge_list:
                    edge_list.append((vertex_1, vertex_2))
        return edge_list
    
    #############################################################################################################################################

    @property
    def nb_edges ( self: Self,
                 ) ->    Integral:
    
        """
            Returns the number of edges in the graph.
            Symmetric edges are counted once.
            In:
                * self: Reference to the current object.
            Out:
                * nb_edges: Number of edges in the graph.
        """
        
        # Get the number of edges
        nb_edges = len(self.edges)
        return nb_edges

    #############################################################################################################################################
    #                                                               PUBLIC METHODS                                                              #
    #############################################################################################################################################

    def add_vertex ( self:   Self,
                     vertex: Hashable
                   ) ->      None:

        """
            Adds a vertex to the graph.
            In:
                * self:   Reference to the current object.
                * vertex: Vertex to add.
            Out:
                * None.
        """
        
        # Debug
        assert isinstance(vertex, Hashable), "Argument 'vertex' must be hashable"
        assert vertex not in self.__adjacency, "Vertex already in the graph"

        # Add vertex to the adjacency matrix
        self.__adjacency[vertex] = {}
        
    #############################################################################################################################################

    def add_edge ( self:      Self,
                   vertex_1:  Hashable,
                   vertex_2:  Hashable,
                   weight:    Number = 1,
                   symmetric: bool = False
                 ) ->         None:

        """
            Adds an edge to the graph.
            By default, it is unweighted, encoded using a weight of 1.0.
            The edge can be directed or not.
            In:
                * self:      Reference to the current object.
                * vertex_1:  First vertex.
                * vertex_2:  Second vertex.
                * weight:    Weight of the edge.
                * symmetric: Whether the edge is symmetric.
            Out:
                * None.
        """
        
        # Debug
        assert isinstance(vertex_1, Hashable), "Argument 'vertex_1' must be hashable"
        assert isinstance(vertex_2, Hashable), "Argument 'vertex_2' must be hashable"
        assert isinstance(weight, Number), "Argument 'weight' must be a real number"
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

    def get_neighbors ( self:   Self,
                        vertex: Hashable
                      ) ->      List[Hashable]:

        """
            Returns the list of neighbors of a vertex.
            In:
                * self:   Reference to the current object.
                * vertex: Vertex of which to get neighbors.
            Out:
                * neighbors: List of neighbors of the vertex.
        """
        
        # Debug
        assert isinstance(vertex, Hashable), "Argument 'vertex' must be hashable"
        assert vertex in self.__adjacency, "Vertex not in the graph"

        # Get neighbors
        neighbors = list(self.__adjacency[vertex].keys())
        return neighbors

    #############################################################################################################################################

    def get_weight ( self:     Self,
                     vertex_1: Hashable,
                     vertex_2: Hashable
                   ) ->        Number:

        """
            Returns the weight of an edge.
            In:
                * self:     Reference to the current object.
                * vertex_1: First vertex.
                * vertex_2: Second vertex.
            Out:
                * weight: Weight of the edge.
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

    def as_dict ( self: Self,
                ) ->    Dict[Hashable, Dict[Hashable, Number]]:

        """
            Returns a dictionary representing the adjacency matrix.
            In:
                * self: Reference to the current object.
            Out:
                * adjacency_dict: Dictionary representing the adjacency matrix.
        """
        
        # Make a copy of the adjacency matrix
        adjacency_dict = self.__adjacency.copy()
        return adjacency_dict
        
    #############################################################################################################################################

    def as_numpy_ndarray ( self: Self,
                         ) ->    Any:

        """
            Returns a numpy ndarray representing the graph.
            Entries are given in order of the vertices.
            In:
                * self: Reference to the current object.
            Out:
                * adjacency_matrix: Numpy ndarray representing the adjacency matrix.
        """
        
        # Debug
        assert "numpy" in globals(), "Numpy is not available"

        # Create the adjacency matrix
        adjacency_matrix = numpy.zeros((self.nb_vertices, self.nb_vertices), dtype=int)
        for i, vertex_1 in enumerate(self.__adjacency):
            for j, vertex_2 in enumerate(self.__adjacency):
                if self.has_edge(vertex_1, vertex_2):
                    adjacency_matrix[i, j] = self.get_weight(vertex_1, vertex_2)
        return adjacency_matrix

    #############################################################################################################################################

    def as_torch_tensor ( self: Self,
                        ) ->    Any:

        """
            Returns a torch tensor representing the maze.
            Entries are given in order of the vertices.
            In:
                * self: Reference to the current object.
            Out:
                * adjacency_matrix: Torch tensor representing the adjacency matrix.
        """
        
        # Debug
        assert "torch" in globals(), "Torch is not available"

        # Create the adjacency matrix
        adjacency_matrix = torch.zeros((self.nb_vertices, self.nb_vertices), dtype=int)
        for i, vertex_1 in enumerate(self.__adjacency):
            for j, vertex_2 in enumerate(self.__adjacency):
                if self.has_edge(vertex_1, vertex_2):
                    adjacency_matrix[i, j] = self.get_weight(vertex_1, vertex_2)
        return adjacency_matrix

    #############################################################################################################################################

    def remove_vertex ( self:   Self,
                        vertex: Hashable
                      ) ->      None:

        """
            Removes a vertex from the graph.
            Also removes all edges connected to this vertex.
            In:
                * self:   Reference to the current object.
                * vertex: Vertex to remove.
            Out:
                * None.
        """
        
        # Debug
        assert isinstance(vertex, Hashable), "Argument 'vertex' must be hashable"
        assert vertex in self.__adjacency, "Vertex not in the graph"

        # Remove the vertex and connections to it
        for neighbor in self.__adjacency:
            if vertex in self.__adjacency[neighbor]:
                del self.__adjacency[neighbor][vertex]
        del self.__adjacency[vertex]
        
    #############################################################################################################################################

    def remove_edge ( self:      Self,
                      vertex_1:  Hashable,
                      vertex_2:  Hashable,
                      symmetric: bool = False
                    ) ->         None:

        """
            Removes an edge from the graph.
            In:
                * self:      Reference to the current object.
                * vertex_1:  First vertex.
                * vertex_2:  Second vertex.
                * symmetric: Also delete the symmetric edge.
            Out:
                * None.
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

    def is_connected ( self: Self,
                     ) ->    bool:

        """
            Checks whether the graph is connected.
            Uses a depth-first search.
            In:
                * self: Reference to the current object.
            Out:
                * connected: Whether the graph is connected.
        """
        
        # Debug
        assert self.nb_vertices > 0, "Graph is empty"

        # Create a list of visited vertices
        vertices = list(self.vertices)
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

    def minimum_spanning_tree ( self:        Self,
                                random_seed: Optional[Integral] = None
                              ) ->           Self:

        """
            Returns the minimum spanning tree of the graph.
            In:
                * self: Reference to the current object.
                * random_seed: Seed for the random number generator.
            Out:
                * minimum_spanning_tree: Graph representing the minimum spanning tree.
        """
        
        # Debug
        assert random_seed is None or isinstance(random_seed, Integral), "Argument 'random_seed' must be an integer"
        assert random_seed is None or 0 <= random_seed < sys.maxsize, "Argument 'random_seed' must be non-negative"

        # Initialize a random number generator
        rng = random.Random(random_seed)

        # Shuffle vertices
        vertices_to_add = self.vertices
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
            neighbors_in_mst = [neighbor for neighbor in neighbors if neighbor in mst.vertices]
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

    def has_edge ( self:      Self,
                   vertex_1:  Hashable,
                   vertex_2:  Hashable,
                 ) ->         bool:
        
        """
            Checks whether an edge exists between two vertices.
            In:
                * self:     Reference to the current object.
                * vertex_1: First vertex.
                * vertex_2: Second vertex.
            Out:
                * edge_exists: Whether an edge exists between the two vertices.
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

    def edge_is_symmetric ( self:     Self,
                            vertex_1: Hashable,
                            vertex_2: Hashable,
                          ) ->        bool:
        
        """
            Checks whether an edge is symmetric.
            In:
                * self:     Reference to the current object.
                * vertex_1: First vertex.
                * vertex_2: Second vertex.
            Out:
                * symmetric: Whether the edge is symmetric.
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

#####################################################################################################################################################
#####################################################################################################################################################
