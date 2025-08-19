#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

# This file is part of the PyRat library.
# It describes a player that can be used in a PyRat game.
# It is meant to be copy-pasted in a new file to create a new player.

"""
This module provides a template for creating a new player in a PyRat game.
It defines a class that inherits from ``Player`` and provides methods that can be overridden to implement your own player.
You can use this template to create a new player by copying this file and renaming it.
You can then modify the class name and the methods to implement your own player logic.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
from typing import *
from typing_extensions import *
from numbers import *

# PyRat imports
from pyrat import Player, Maze, GameState, Action

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class TemplatePlayer (Player):

    """
    *(This class inherits from* ``Player`` *).*

    This player is basically a player that does nothing except printing the phase of the game.
    It is meant to be used as a template to create new players.
    Methods ``preprocessing()``, and ``postprocessing()`` are optional.
    Method ``turn()`` is mandatory.
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

        Args:
            args:   Arguments to pass to the parent constructor.
            kwargs: Keyword arguments to pass to the parent constructor.
        """

        # Inherit from parent class
        super().__init__(*args, **kwargs)

        # Print phase of the game
        print("Constructor")
       
    #############################################################################################################################################
    #                                                               PYRAT METHODS                                                               #
    #############################################################################################################################################

    @override
    def preprocessing ( self:       Self,
                        maze:       Maze,
                        game_state: GameState,
                      ) ->          None:
        
        """
        *(This method redefines the method of the parent class with the same name).*

        This method is called once at the beginning of the game.
        It can be used to initialize attributes or to perform any other setup that is needed before the game starts.
        It typically is given more computational resources than the ``turn()`` method.
        Therefore, it is a good place to perform any heavy computations that are needed for the player to function correctly.

        Args:
            maze:       An object representing the maze in which the player plays.
            game_state: An object representing the state of the game.
        """
        
        # Print phase of the game
        print("Preprocessing")

    #############################################################################################################################################

    @override
    def turn ( self:       Self,
               maze:       Maze,
               game_state: GameState,
             ) ->          Action:

        """
        *(This method redefines the method of the parent class with the same name).*

        This method is called at each turn of the game.
        It returns an action to perform among the possible actions, defined in the ``Action`` enumeration.
        It is generally given less computational resources than the ``preprocessing()`` method.
        Therefore, you should limit the amount of computations you perform in this method to those that require real-time information.

        Args:
            maze:       An object representing the maze in which the player plays.
            game_state: An object representing the state of the game.

        Returns:
            One of the possible action, defined in the ``Action`` enumeration.
        """

        # Print phase of the game
        print("Turn", game_state.turn)

        # Return an action
        return Action.NOTHING

#############################################################################################################################################

    @override
    def postprocessing ( self:       Self,
                         maze:       Maze,
                         game_state: GameState,
                         stats:      Dict[str, Any],
                       ) ->          None:

        """
        *(This method redefines the method of the parent class with the same name).*

        This method is called once at the end of the game.
        It can be used to perform any cleanup that is needed after the game ends.
        It is not timed, and can be used to analyze the completed game, train models, etc.

        Args:
            maze:       An object representing the maze in which the player plays.
            game_state: An object representing the state of the game.
            stats:      A dictionary containing statistics about the game.
        """

        # Print phase of the game
        print("Postprocessing")

#####################################################################################################################################################
#####################################################################################################################################################
