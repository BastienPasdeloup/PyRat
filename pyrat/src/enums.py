#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# Please import necessary elements using the following syntax:
#     from pyrat import <element_name>

"""
This module contains the enumerations used in PyRat.
An enumeration is a symbolic name for a set of values, which can be used to make the code more readable and maintainable.
It is recommended to use these enumerations instead of hard-coded strings or integers to avoid errors and improve code clarity.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
import enum

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class Action (enum.Enum):

    """
    This enumeration defines all the possible actions a player can take in a maze.
    In the classes inheriting from ``Player``, the ``turn()`` method should return one of these actions.

    Possible actions are:
        * ``NOTHING``: No action.
        * ``NORTH``:   Move north.
        * ``SOUTH``:   Move south.
        * ``EAST``:    Move east.
        * ``WEST``:    Move west.
    """

    NOTHING = "nothing"
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"

#####################################################################################################################################################

class GameMode (enum.Enum):

    """
    This enumeration defines all accepted game modes.
    The game mode defines how time is shared between players and how actions are applied.
    To set the game mode, use the ``game_mode`` parameter of the ``Game`` class.

    Possible game modes are:
        * ``MATCH``:       Players have their own process and play simultaneously, with timeouts that can be missed (default in multi-team games). \
                           In other words, each player has a limited time to make a decision, and if they do not make a decision in time, their action is set to ``Action.NOTHING`` for the turn. \
                           The durations of the preprocessing and turn phases are defined by the ``preprocessing_time`` and ``turn_time`` parameters of the ``Game`` class.
        * ``SYNCHRONOUS``: Players have their own process and play simultaneously, but actions are applied when all players have made their decision. \
                           Contrary to the ``MATCH`` mode, there is no timeout, so players can take as much time as they want to make their decision. \
                           Preprocessing and turn phases are still given a minimum duration, but they can be longer if players take more time to make their decision. \
                           This is useful for debugging, as it allows you to see the game state after each player's decision.
        * ``SEQUENTIAL``:  All players are asked for a decision, and then actions are applied simultaneously, but there is no multiprocessing (default in single-team games).
        * ``SIMULATION``:  The game is run as fast as possible, *i.e.*, there is no rendering, no multiprocessing, and no timeouts. \
                           You should use this mode when running multiple games to collect statistics, as it is the fastest mode.
    """

    MATCH = "match"
    SYNCHRONOUS = "synchronous"
    SEQUENTIAL = "sequential"
    SIMULATION = "simulation"

#####################################################################################################################################################

class PlayerSkin (enum.Enum):

    """
    This enumeration defines all available player skins, *i.e.*, the visual appearance of the player.
    To set the skin of a player, use the ``skin`` parameter of the ``Player`` class when instantiating it.

    Possible skins are:
        * ``RAT``:    The player is a rat.
        * ``PYTHON``: The player is a python.
        * ``GHOST``:  The player is a ghost from Pacman.
        * ``MARIO``:  The player is Super Mario.
    """

    RAT = "rat"
    PYTHON = "python"
    GHOST = "ghost"
    MARIO = "mario"

#####################################################################################################################################################

class RandomMazeAlgorithm (enum.Enum):

    """
    This enumeration defines all the possible algorithms to generate a random maze.
    To set the algorithm, use the ``random_maze_algorithm`` parameter of the ``Game`` class.

    Possible algorithms are:
        * ``HOLES_ON_SIDE``: Missing cells tend to be on the sides of the maze.
        * ``UNIFORM_HOLES``: Missing cells are uniformly distributed.
        * ``BIG_HOLES``:     Missing cells tend to be grouped together.
    """

    HOLES_ON_SIDE = "holes_on_side"
    UNIFORM_HOLES = "uniform_holes"
    BIG_HOLES = "big_holes"

#####################################################################################################################################################

class RenderMode (enum.Enum):

    """
    This enumeration defines all accepted rendering modes, *i.e.*, how the game is visualized.
    To set the rendering mode, use the ``render_mode`` parameter of the ``Game`` class.

    Possible rendering modes are:
        * ``GUI``:          The game will be rendered graphically in a window.
        * ``ANSI``:         The game will be rendered in the terminal using ANSI characters.
        * ``ASCII``:        The game will be rendered in the terminal using ASCII characters.
        * ``NO_RENDERING``: The game will not be rendered.
    """

    GUI = "gui"
    ANSI = "ansi"
    ASCII = "ascii"
    NO_RENDERING = "no_rendering"

#####################################################################################################################################################

class StartingLocation (enum.Enum):

    """
    This enumeration defines all named starting locations for players.
    If the chosen location is not available, the player will be placed at the closest available location.
    To set the starting location of a player, use the ``location`` parameter of the ``Game.add_player()`` method.
    
    Possible starting locations are:
        * ``CENTER``:       The player will start at the center of the maze.
        * ``TOP_LEFT``:     The player will start at the top left corner of the maze.
        * ``TOP_RIGHT``:    The player will start at the top right corner of the maze.
        * ``BOTTOM_LEFT``:  The player will start at the bottom left corner of the maz.
        * ``BOTTOM_RIGHT``: The player will start at the bottom right corner of the maze.
        * ``RANDOM``:       The player will start at a random location.
        * ``SAME``:         The player will start at the same location as the last player added.
    """

    CENTER = "center"
    TOP_LEFT = "top_left"
    TOP_RIGHT = "top_right"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_RIGHT = "bottom_right"
    RANDOM = "random"
    SAME = "same"

#####################################################################################################################################################
#####################################################################################################################################################