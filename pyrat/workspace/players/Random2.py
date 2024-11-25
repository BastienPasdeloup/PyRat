#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This file contains useful elements to define a particular player.
    In order to use this player, you need to instanciate it and add it to a game.
    Please refer to example games to see how to do it properly.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
from typing import *
from typing_extensions import *
from numbers import *
import random

# PyRat imports
from pyrat import Player, Maze, GameState, Action

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

    def __init__ ( self:     Self,
                   *args:    Any,
                   **kwargs: Any
                 ) ->        None:

        """
            This function is the constructor of the class.
            When an object is instantiated, this method is called to initialize the object.
            This is where you should define the attributes of the object and set their initial values.
            Arguments *args and **kwargs are used to pass arguments to the parent constructor.
            This is useful not to declare again all the parent's attributes in the child class.
            In:
                * self:   Reference to the current object.
                * args:   Arguments to pass to the parent constructor.
                * kwargs: Keyword arguments to pass to the parent constructor.
            Out:
                * A new instance of the class (we indicate None as return type per convention, see PEP-484).
        """

        # Inherit from parent class
        super().__init__(*args, **kwargs)
       
    #############################################################################################################################################
    #                                                               PYRAT METHODS                                                               #
    #############################################################################################################################################

    @override
    def turn ( self:       Self,
               maze:       Maze,
               game_state: GameState,
             ) ->          Action:

        """
            This method redefines the abstract method of the parent class.
            It is called at each turn of the game.
            It returns an action to perform among the possible actions, defined in the Action enumeration.
            In:
                * self:       Reference to the current object.
                * maze:       An object representing the maze in which the player plays.
                * game_state: An object representing the state of the game.
            Out:
                * action: One of the possible actions.
        """

        # Return an action
        action = self.find_next_action(maze, game_state)
        return action

    #############################################################################################################################################
    #                                                               OTHER METHODS                                                               #
    #############################################################################################################################################

    def find_next_action ( self:       Self,
                           maze:       Maze,
                           game_state: GameState,
                         ) ->          Action:

        """
            This method returns an action to perform among the possible actions, defined in the Action enumeration.
            Here, the action is chosen randomly among those that don't hit a wall.
            In:
                * self:       Reference to the current object.
                * maze:       An object representing the maze in which the player plays.
                * game_state: An object representing the state of the game.
            Out:
                * action: One of the possible actions.
        """

        # Choose a random neighbor
        neighbors = maze.get_neighbors(game_state.player_locations[self.name])
        neighbor = random.choice(neighbors)
        
        # Retrieve the corresponding action
        action = maze.locations_to_action(game_state.player_locations[self.name], neighbor)
        return action

#####################################################################################################################################################
#####################################################################################################################################################
