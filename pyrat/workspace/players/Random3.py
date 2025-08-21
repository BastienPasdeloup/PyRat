#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

# This file is part of the PyRat library.
# It describes a player that can be used in a PyRat game.
# It is meant to be used as a library, and not to be executed directly.
# Please import this file from a game script using the following syntax:
#     from players.Random3 import Random3

"""
This module provides a player that performs random actions in a PyRat game.
It is an improvement of the ``Random2`` player.
Here, we illustrate how attributes can be used to keep track of visited cells.
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

class Random3 (Player):

    """
    *(This class inherits from* ``Player`` *).*

    This player is an improvement of the ``Random2`` player.
    Here, we add elements that help us explore better the maze.
    More precisely, we keep a set of cells that have already been visited in the game.
    Then, at each turn, we choose in priority a random move among those that lead us to an unvisited cell.
    If no such move exists, we move randomly.
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
        Here, the constructor is only used to initialize a set that will keep track of visited cells.
        This set can later be updated at each turn of the game to avoid going back to cells that have already been visited.

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
        Here, we just initialize the set of visited cells.

        Args:
            maze:       An object representing the maze in which the player plays.
            game_state: An object representing the state of the game.
        """

        # Initialize visited cells
        self.visited_cells = set()

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
        action = self.find_next_action(maze, game_state)
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
        If no such action exists, we choose randomly among all possible actions that don't hit a wall.
        
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
    
#####################################################################################################################################################
#####################################################################################################################################################
