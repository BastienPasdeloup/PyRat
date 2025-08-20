#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# Please import necessary elements using the following syntax:
#     from pyrat import <element_name>

"""
This module provides a rendering engine for the PyRat game.
It defines the base class for rendering engines, which can be used to render the game in different ways.
The default implementation does nothing, but subclasses can override the `render` method to provide custom rendering logic.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

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
    By default, this engine renders nothing, which is a valid rendering mode for a PyRat game.
    Inherit from this class to create a rendering engine that does something.
    """

    #############################################################################################################################################
    #                                                               MAGIC METHODS                                                               #
    #############################################################################################################################################

    def __init__ ( self,
                   rendering_speed:   float = 1.0,
                   render_simplified: bool = False
                 ) ->                 None:

        """
        Initializes a new instance of the class.
        
        Args:
            rendering_speed:   Speed at which the game should be rendered.
            render_simplified: Whether to render the simplified version of the game.
        """

        # Debug
        assert isinstance(render_simplified, bool), "Argument 'render_simplified' must be a boolean"
        assert isinstance(rendering_speed, float), "Argument 'gui_speed' must be a real number"
        assert rendering_speed > 0.0, "Argument 'gui_speed' must be positive"

        # Protected attributes
        self._render_simplified = render_simplified
        self._rendering_speed = rendering_speed
        
    #############################################################################################################################################
    #                                                               PUBLIC METHODS                                                              #
    #############################################################################################################################################

    def end (self) -> None:
        
        """
        This method does nothing.
        Redefine it in the child classes to do something when the game ends if needed.
        """

        # Nothing to do
        pass

    #############################################################################################################################################
    
    def render ( self,
                 players:    list[Player],
                 maze:       Maze,
                 game_state: GameState,
               ) ->          None:
        
        """
        This method does nothing.
        Redefine it in the child classes to render the game somehow.

        Args:
            players:    Players of the game.
            maze:       Maze of the game.
            game_state: State of the game.
        """

        # Debug
        assert isinstance(players, list), "Argument 'players' must be a list"
        assert all(isinstance(player, Player) for player in players), "All elements of 'players' must be of type 'pyrat.Player'"
        assert isinstance(maze, Maze), "Argument 'maze' must be of type 'pyrat.Maze'"
        assert isinstance(game_state, GameState), "Argument 'game_state' must be of type 'pyrat.GameState'"

        # Nothing to do
        pass

#####################################################################################################################################################
#####################################################################################################################################################
