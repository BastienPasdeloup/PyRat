#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

# This file is part of the PyRat library.
# It describes a player that can be used in a PyRat game.
# It is meant to be used as a library, and not to be executed directly.
# Please import this file from a game script using the following syntax:
#     from players.Random4 import Random4

"""
This module provides a player that performs random actions in a PyRat game.
It is an improvement of the ``Random3`` player.
Here, we illustrate how to use the ``preprocessing()`` method to do things at the beginning of the game.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
import random

# PyRat imports
from pyrat import Player, Maze, GameState, Action

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class Random4 (Player):

    """
    *(This class inherits from* ``Player`` *).*

    This player is an improvement of the ``Random3`` player.
    A limitation of ``Random3`` is that it can easily enter its fallback mode when visiting a dead-end.
    In this case, it may move randomly for a long time before reaching an unvisited cell
    To improve our algorithm, we are going to create a new maze attribute that is the same as the original maze, but with the dead-end cells removed.
    Since the maze is only provided at the beginning of the game, we will use the ``preprocessing()`` method to create this new maze.
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self,
                   *args:    object,
                   **kwargs: object
                 ) ->        None:

        """
        Initializes a new instance of the class.
        Here, in addition to the attributes developed in the ``Random3`` player, we also create an attribute for our reduced maze.

        Args:
            args:   Arguments to pass to the parent constructor.
            kwargs: Keyword arguments to pass to the parent constructor.
        """

        # Inherit from parent class
        super().__init__(*args, **kwargs)

        # We create an attribute to keep track of visited cells
        # We will initialize it in the ``preprocessing()`` method to allow the game to be reset
        # Otherwise, the set would keep the cells visited in previous games
        self.visited_cells = None

        # We also create an attribute for the reduced maze
        self.reduced_maze = None
       
    #############################################################################################################################################
    #                                                               PYRAT METHODS                                                               #
    #############################################################################################################################################

    def preprocessing ( self,
                        maze:       Maze,
                        game_state: GameState,
                      ) ->          None:
        
        """
        *(This method redefines the method of the parent class with the same name).*

        This method is called once at the beginning of the game.
        Here, we use it to create a reduced maze that contains only the cells that are not dead-ends.
        We define a dead-end as a cell that has only one neighbor and does not contain cheese or the player.
        Note that this is not the best way to define a dead-end, but it is a simple one.

        Args:
            maze:       An object representing the maze in which the player plays.
            game_state: An object representing the state of the game.
        """

        # Initialize visited cells
        self.visited_cells = set()

        # Reduce the maze
        my_location = game_state.player_locations[self.get_name()]
        self.reduced_maze = self.remove_dead_ends(maze, [my_location] + game_state.cheese)

    #############################################################################################################################################

    def turn ( self,
               maze:       Maze,
               game_state: GameState,
             ) ->          Action:

        """
        *(This method redefines the method of the parent class with the same name).*

        It is called at each turn of the game.
        It returns an action to perform among the possible actions, defined in the ``Action`` enumeration.
        We also update the set of visited cells at each turn.
        Now, we work with the reduced maze to find the next action.

        Args:
            maze:       An object representing the maze in which the player plays.
            game_state: An object representing the state of the game.
        
        Returns:
            One of the possible actions.
        """

        # Mark current cell as visited
        my_location = game_state.player_locations[self.get_name()]
        if my_location not in self.visited_cells:
            self.visited_cells.add(my_location)

        # Return an action
        action = self.find_next_action(self.reduced_maze, game_state)
        return action
    
    #############################################################################################################################################
    #                                                               OTHER METHODS                                                               #
    #############################################################################################################################################

    def find_next_action ( self,
                           maze:       Maze,
                           game_state: GameState,
                         ) ->          Action:

        """
        This method returns an action to perform among the possible actions, defined in the ``Action`` enumeration.
        Here, the action is chosen randomly among those that don't hit a wall, and that lead to an unvisited cell if possible.
        If no such action exists, we come back to the last cell in the trajectory and pop it.
        
        Args:
            maze:       An object representing the maze in which the player plays.
            game_state: An object representing the state of the game.

        Returns:
            One of the possible actions that leads to a valid neighbor.
        """

        # Go to an unvisited neighbor in priority
        my_location = game_state.player_locations[self.get_name()]
        neighbors = maze.get_neighbors(my_location)
        unvisited_neighbors = [neighbor for neighbor in neighbors if neighbor not in self.visited_cells]
        if len(unvisited_neighbors) > 0:
            neighbor = random.choice(unvisited_neighbors)
            
        # If there is no unvisited neighbor, choose one randomly
        else:
            neighbor = random.choice(neighbors)
        
        # Retrieve the corresponding action
        action = maze.locations_to_action(my_location, neighbor)
        return action
    
    #############################################################################################################################################

    def remove_dead_ends ( self,
                           maze:              Maze,
                           locations_to_keep: list[tuple[int, int]]
                         ) ->                 Maze:
        
        """
        This method returns a new maze that contains only the cells that are not dead-ends.
        A dead-end is defined as a cell that has only one neighbor and does not contain cheese or the player.

        Args:
            maze:              An object representing the maze in which the player plays.
            locations_to_keep: A list of locations to keep in the reduced maze.

        Returns:
            A new maze with only the cells that are not dead-ends.
        """

        # Initialize the reduced maze as the original one
        # We do not need to make a copy of the maze, as the game sends a copy of the maze at each turn.
        updated_maze = maze
        
        # Iteratively remove dead-ends from the maze
        # We still keep dead ends that contain locations to keep
        removed_something = True
        while removed_something:
            removed_something = False
            for vertex in updated_maze.get_vertices():
                if len(updated_maze.get_neighbors(vertex)) == 1 and vertex not in locations_to_keep:
                    updated_maze.remove_vertex(vertex)
                    removed_something = True

        # Return the updated maze
        return updated_maze

#####################################################################################################################################################
#####################################################################################################################################################
