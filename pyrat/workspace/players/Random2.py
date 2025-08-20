#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

# This file is part of the PyRat library.
# It describes a player that can be used in a PyRat game.
# It is meant to be used as a library, and not to be executed directly.
# Please import this file from a game script using the following syntax:
#     from players.Random2 import Random2

"""
This module provides a player that performs random actions in a PyRat game.
Contrary to the ``Random1`` player, this one takes into account the maze structure to avoid hitting walls.
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

class Random2 (Player):

    """
    *(This class inherits from* ``Player`` *).*

    This player is an improvement of the ``Random1`` player.
    Contrary to that previous version, here we take into account the maze structure.
    More precisely, we select at each turn a random move among those that don't hit a wall.
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
        Here, the constructor is only used to initialize the player.
        It transmits the arguments to the parent constructor, which is responsible for initializing the name and the skin of the player.

        Args:
            args:   Arguments to pass to the parent constructor.
            kwargs: Keyword arguments to pass to the parent constructor.
        """

        # Inherit from parent class
        super().__init__(*args, **kwargs)
       
    #############################################################################################################################################
    #                                                               PYRAT METHODS                                                               #
    #############################################################################################################################################

    def turn ( self,
               maze:       Maze,
               game_state: GameState,
             ) ->          Action:

        """
        *(This method redefines the method of the parent class with the same name).*

        It is called at each turn of the game.
        It returns an action to perform among the possible actions, defined in the ``Action`` enumeration.

        Args:
            maze:       An object representing the maze in which the player plays.
            game_state: An object representing the state of the game.
        
        Returns:
            One of the possible actions.
        """

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
        Here, the action is chosen randomly among those that don't hit a wall.

        Args:
            maze:       An object representing the maze in which the player plays.
            game_state: An object representing the state of the game.

        Returns:
            One of the possible actions that leads to a valid neighbor.
        """

        # Choose a random neighbor
        my_location = game_state.player_locations[self.get_name()]
        neighbors = maze.get_neighbors(my_location)
        neighbor = random.choice(neighbors)
        
        # Retrieve the corresponding action
        action = maze.locations_to_action(my_location, neighbor)
        return action

#####################################################################################################################################################
#####################################################################################################################################################
