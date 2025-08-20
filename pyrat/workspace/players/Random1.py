#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

# This file is part of the PyRat library.
# It describes a player that can be used in a PyRat game.
# It is meant to be used as a library, and not to be executed directly.
# Please import this file from a game script using the following syntax:
#     from players.Random1 import Random1

"""
This module provides a player that performs random actions in a PyRat game.
It is a simple player that does not take into account the maze structure.
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

class Random1 (Player):

    """
    *(This class inherits from* ``Player`` *).*

    This player controls a PyRat character by performing random actions.
    More precisely, at each turn, a random choice among all possible actions is selected.
    Note that this doesn't take into account the structure of the maze.
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
        action = self.find_next_action()
        return action

    #############################################################################################################################################
    #                                                               OTHER METHODS                                                               #
    #############################################################################################################################################

    def find_next_action (self) -> Action:

        """
        This method returns an action to perform among the possible actions, defined in the ``Action`` enumeration.
        Here, the action is chosen randomly.

        Returns:
            One of the possible actions.
        """

        # Choose a random action to perform
        action = random.choice(list(Action))
        return action

#####################################################################################################################################################
#####################################################################################################################################################
