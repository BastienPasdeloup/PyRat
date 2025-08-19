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
    This player follows a predetermined list of actions.
    This is useful to save and replay a game.
    """

    #############################################################################################################################################
    #                                                               MAGIC METHODS                                                               #
    #############################################################################################################################################

    def __init__ ( self:     Self,
                   actions:  List[Action],
                   *args:    Any,
                   **kwargs: Any
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

    @override
    def turn ( self:       Self,
               maze:       Maze,
               game_state: GameState
             ) ->          Action:

        """
        Redefines the abstract method of the parent class.
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
