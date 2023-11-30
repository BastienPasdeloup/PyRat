#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This file contains useful elements to define a particular player.
    It is meant to be used as a library, and not to be executed directly.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External typing imports
from typing import *
from typing_extensions import *
from numbers import *

# Other external imports
import random

# Internal imports
from pyrat2024 import Player, Maze, GameState
from utils import locations_to_action

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class Random2 (Player):

    """
        This player is an improvement of the Random1 player.
        Contrary to that previous version, here we take into account the maze structure.
        More precisely, we select at each turn a random move among those that don't hit a wall.
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self: Self,
                   name: str = "Random 2",
                   skin: str = "default"
                 ) ->    Self:

        """
            This function is the constructor of the class.
            In:
                * self: Reference to the current object.
                * name: Name of the player.
                * skin: Skin of the player.
            Out:
                * A new instance of the class.
        """

        # Inherit from parent class
        super().__init__(name, skin)
       
    #############################################################################################################################################
    #                                                               PUBLIC METHODS                                                              #
    #############################################################################################################################################

    def turn ( self:       Self,
               maze:       Maze,
               game_state: GameState,
             ) ->       str:

        """
            This method redefines the abstract method of the parent class.
            It is called at each turn of the game.
            It returns a random action that does not lead to a wall.
            In:
                * self:       Reference to the current object.
                * maze:       An object representing the maze in which the player plays.
                * game_state: An object representing the state of the game.
            Out:
                * action: One of the possible actions
        """

        # Choose a random neighbor
        neighbors = maze.get_neighbors(game_state.player_locations[self.name])
        neighbor = random.choice(neighbors)
        
        # Retrieve the corresponding action
        action = locations_to_action(maze, game_state.player_locations[self.name], neighbor)
        return action

#####################################################################################################################################################
#####################################################################################################################################################