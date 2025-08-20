#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# Please import necessary elements using the following syntax:
#     from pyrat import <element_name>

"""
This module provides a player that follows a predetermined list of actions.
It is used when games are saved and replayed.
This player can be useful for testing purposes, for instance to evaluate the behavior of other players against a fixed strategy.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# PyRat imports
from pyrat.src.Player import Player
from pyrat.src.Maze import Maze
from pyrat.src.GameState import GameState
from pyrat.src.enums import Action

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class FixedPlayer (Player):

    """
    *(This class inherits from* ``Player`` *).*

    This player follows a predetermined list of actions.
    This is useful to save and replay a game.
    """

    #############################################################################################################################################
    #                                                               MAGIC METHODS                                                               #
    #############################################################################################################################################

    def __init__ ( self,
                   actions:  list[Action],
                   *args:    object,
                   **kwargs: object
                 ) ->        None:

        """
        Initializes a new instance of the class.
        The player is given a predetermined list of actions.

        Args:
            actions:  List of actions to perform.
            *args:    Arguments to pass to the parent constructor.
            **kwargs: Keyword arguments to pass to the parent constructor.
        """

        # Inherit from parent class
        super().__init__(*args, **kwargs)

        # Debug
        assert isinstance(actions, list), "Argument 'actions' must be a list"
        assert all(action in Action for action in actions), "All elements of 'actions' must be of type 'pyrat.Action'"

        # Private attributes
        self.__actions = actions
       
    #############################################################################################################################################
    #                                                               PUBLIC METHODS                                                              #
    #############################################################################################################################################

    def turn ( self,
               maze:       Maze,
               game_state: GameState
             ) ->          Action:

        """
        *(This method redefines the method of the parent class with the same name).*
        
        Called at each turn of the game to return the next action to perform.

        Args:
            maze:       An object representing the maze in which the player plays.
            game_state: An object representing the state of the game.

        Returns:
            One of the possible actions.
        """

        # Get next action
        action = self.__actions.pop(0)
        return action

#####################################################################################################################################################
#####################################################################################################################################################
