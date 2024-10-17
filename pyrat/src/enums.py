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
import enum

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class Action (enum.Enum):

    """
        This enumeration defines all the possible actions a player can take in a maze.
        Values:
            * NOTHING: No action.
            * NORTH:   Move north.
            * SOUTH:   Move south.
            * EAST:    Move east.
            * WEST:    Move west.
    """

    NOTHING = "nothing"
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"

#####################################################################################################################################################

class RenderMode (enum.Enum):

    """
        This enumeration defines all accepted rendering modes.
        Values:
            * GUI:          The game will be rendered graphically in a window.
            * ANSI:         The game will be rendered in the terminal using ANSI characters.
            * ASCII:        The game will be rendered in the terminal using ASCII characters.
            * NO_RENDERING: The game will not be rendered.
    """

    GUI = "gui"
    ANSI = "ansi"
    ASCII = "ascii"
    NO_RENDERING = "no_rendering"

#####################################################################################################################################################

class GameMode (enum.Enum):

    """
        This enumeration defines all accepted game modes.
        Values:
            * MATCH:       Players have their own process and play simultaneously, with timeouts that can be missed (default in multi-team games).
            * SYNCHRONOUS: Players have their own process and play simultaneously, but actions are applied when all players are ready.
            * SEQUENTIAL:  All players are asked for a decision, and then actions are applied simultaneously, but there is no multiprocessing (default in single-team games).
            * SIMULATION:  The game is run as fast as possible, i.e., there is no rendering, no multiprocessing, and no timeouts.
    """

    MATCH = "match"
    SYNCHRONOUS = "synchronous"
    SEQUENTIAL = "sequential"
    SIMULATION = "simulation"

#####################################################################################################################################################

class StartingLocation (enum.Enum):

    """
        This enumeration defines all named starting locations for players.
        The player will start at the closest existing cell to the desired location.
        Values:
            * CENTER:       The player will start at the center of the maze.
            * TOP_LEFT:     The player will start at the top left corner of the maze.
            * TOP_RIGHT:    The player will start at the top right corner of the maze.
            * BOTTOM_LEFT:  The player will start at the bottom left corner of the maz.
            * BOTTOM_RIGHT: The player will start at the bottom right corner of the maze.
            * RANDOM:       The player will start at a random location.
            * SAME:         The player will start at the same location as the previously registered player.
    """

    CENTER = "center"
    TOP_LEFT = "top_left"
    TOP_RIGHT = "top_right"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_RIGHT = "bottom_right"
    RANDOM = "random"
    SAME = "same"

#####################################################################################################################################################

class PlayerSkin (enum.Enum):

    """
        This enumeration defines all available player skins.
        The value should correspond to the directory name containing the skin.
        Values:
            * RAT:    The player is a rat.
            * PYTHON: The player is a python.
            * GHOST:  The player is a ghost from Pacman.
            * MARIO:  The player is Super Mario.
    """

    RAT = "rat"
    PYTHON = "python"
    GHOST = "ghost"
    MARIO = "mario"

#####################################################################################################################################################

class RandomMazeAlgorithm (enum.Enum):

    """
        This enumeration defines all the possible algorithms to generate a random maze.
        Values:
            * HOLES_ON_SIDE: Missing cells tend to be on the sides of the maze.
            * UNIFORM_HOLES: Missing cells are uniformly distributed.
            * BIG_HOLES:     Missing cells tend to be grouped together.
    """

    HOLES_ON_SIDE = "holes_on_side"
    UNIFORM_HOLES = "uniform_holes"
    BIG_HOLES = "big_holes"

#####################################################################################################################################################
#####################################################################################################################################################