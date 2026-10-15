##########################################################################################
########################################## INFO ##########################################
##########################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# Please import necessary elements using the following syntax:
#     from pyrat import <element_name>

"""
This module provides a rendering engine for the PyRat game.
It defines the base class for rendering engines, which can be used to render the game in different ways.
The default implementation does nothing, but subclasses can override the `render` method to provide custom rendering logic.
"""

##########################################################################################
######################################### IMPORTS ########################################
##########################################################################################

# PyRat imports
from pyrat.src.players.player import Player
from pyrat.src.mazes.maze import Maze
from pyrat.src.game.game_state import GameState
from pyrat.src.game.exceptions import PyRatException

##########################################################################################
######################################### CLASSES ########################################
##########################################################################################

class RenderingEngine ():

    """
    A rendering engine is an object that can render a PyRat game.
    By default, this engine renders nothing, which is a valid rendering mode for a PyRat game.
    Inherit from this class to create a rendering engine that does something.
    """

    ##################################################################################
    #                                   CONSTRUCTOR                                  #
    ##################################################################################

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

        # Check validity
        if not isinstance(render_simplified, bool):
            raise PyRatException(f"Argument 'render_simplified' must be a boolean, got {render_simplified!r} of type {type(render_simplified).__name__}")
        if not isinstance(rendering_speed, float):
            raise PyRatException(f"Argument 'rendering_speed' must be a real number, got {rendering_speed!r} of type {type(rendering_speed).__name__}")
        if not (rendering_speed > 0.0):
            raise PyRatException(f"Argument 'rendering_speed' must be positive, got {rendering_speed!r}")

        # Protected attributes
        self._render_simplified = render_simplified
        self._rendering_speed = rendering_speed
        
    ##################################################################################
    #                                 PUBLIC METHODS                                 #
    ##################################################################################

    def end (self) -> None:
        
        """
        This method does nothing.
        Redefine it in the child classes to do something when the game ends if needed.
        """

        # Nothing to do
        pass

    ##################################################################################
    
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

        # Check validity
        if not isinstance(players, list):
            raise PyRatException(f"Argument 'players' must be a list, got an object of type {type(players).__name__}")
        if not all(isinstance(player, Player) for player in players):
            raise PyRatException(f"All elements of 'players' must be of type 'pyrat.Player', got an element of type {type(next(player for player in players if not isinstance(player, Player))).__name__}")
        if not isinstance(maze, Maze):
            raise PyRatException(f"Argument 'maze' must be of type 'pyrat.Maze', got an object of type {type(maze).__name__}")
        if not isinstance(game_state, GameState):
            raise PyRatException(f"Argument 'game_state' must be of type 'pyrat.GameState', got an object of type {type(game_state).__name__}")

        # Nothing to do
        pass

##########################################################################################
##########################################################################################
