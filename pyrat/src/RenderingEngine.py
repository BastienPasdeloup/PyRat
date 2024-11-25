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

# PyRat imports
from pyrat.src.Player import Player
from pyrat.src.Maze import Maze
from pyrat.src.GameState import GameState

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class RenderingEngine ():

    """
        A rendering engine is an object that can render a PyRat game.
        By defaut, this engine renders nothing, which is a valid rendering mode for a PyRat game.
        Inherit from this class to create a rendering engine that does something.
    """

    #############################################################################################################################################
    #                                                               MAGIC METHODS                                                               #
    #############################################################################################################################################

    def __init__ ( self:              Self,
                   rendering_speed:   Number = 1.0,
                   render_simplified: bool = False
                 ) ->                 None:

        """
            This function is the constructor of the class.
            When an object is instantiated, this method is called to initialize the object.
            This is where you should define the attributes of the object and set their initial values.
            In:
                * self:              Reference to the current object.
                * rendering_speed:   Speed at which the game should be rendered.
                * render_simplified: Whether to render the simplified version of the game.
            Out:
                * A new instance of the class (we indicate None as return type per convention, see PEP-484).
        """

        # Debug
        assert isinstance(render_simplified, bool), "Argument 'render_simplified' must be a boolean"
        assert isinstance(rendering_speed, Number), "Argument 'gui_speed' must be a real number"
        assert rendering_speed > 0.0, "Argument 'gui_speed' must be positive"

        # Protected attributes
        self._render_simplified = render_simplified
        self._rendering_speed = rendering_speed
        
    #############################################################################################################################################
    #                                                               PUBLIC METHODS                                                              #
    #############################################################################################################################################

    def render ( self:       Self,
                 players:    List[Player],
                 maze:       Maze,
                 game_state: GameState,
               ) ->          None:
        
        """
            This method does nothing.
            Redefine it in the child classes to render the game somehow.
            In:
                * self:       Reference to the current object.
                * players:    PLayers of the game.
                * maze:       Maze of the game.
                * game_state: State of the game.
            Out:
                * None.
        """

        # Debug
        assert isinstance(players, list), "Argument 'players' must be a list"
        assert all(isinstance(player, Player) for player in players), "All elements of 'players' must be of type 'pyrat.Player'"
        assert isinstance(maze, Maze), "Argument 'maze' must be of type 'pyrat.Maze'"
        assert isinstance(game_state, GameState), "Argument 'game_state' must be of type 'pyrat.GameState'"

        # Nothing to do
        pass

    #############################################################################################################################################

    def end ( self: Self,
            ) ->    None:
        
        """
            This method does nothing.
            Redefine it in the child classes to do something when the game ends if needed.
            In:
                * self: Reference to the current object.
            Out:
                * None.
        """

        # Nothing to do
        pass

#####################################################################################################################################################
#####################################################################################################################################################
