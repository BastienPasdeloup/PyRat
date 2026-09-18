##########################################################################################
########################################## INFO ##########################################
##########################################################################################

# This file defines the public interface of the PyRat library.
# Everything a PyRat program needs is imported from here, using the following syntax:
#     from pyrat import <element_name>
# The modules of the "src" directory are internal, and may change from one version to another.

##########################################################################################
######################################### IMPORTS ########################################
##########################################################################################

# Game
from .src.game.game import Game
from .src.game.game_state import GameState
from .src.game.enums import Action, GameMode, PlayerSkin, RandomMazeAlgorithm, RenderMode, StartingLocation
from .src.game.exceptions import PyRatException

# Players
from .src.players.player import Player
from .src.players.fixed_player import FixedPlayer

# Mazes
from .src.mazes.graph import Graph
from .src.mazes.maze import Maze
from .src.mazes.random_maze import RandomMaze
from .src.mazes.big_holes_random_maze import BigHolesRandomMaze
from .src.mazes.holes_on_side_random_maze import HolesOnSideRandomMaze
from .src.mazes.uniform_holes_random_maze import UniformHolesRandomMaze
from .src.mazes.maze_from_dict import MazeFromDict
from .src.mazes.maze_from_matrix import MazeFromMatrix

# Rendering
from .src.rendering.rendering_engine import RenderingEngine
from .src.rendering.shell_rendering_engine import ShellRenderingEngine
from .src.rendering.pygame_rendering_engine import PygameRenderingEngine

##########################################################################################
######################################## CONSTANTS #######################################
##########################################################################################

# Names that are part of the public interface of the library
__all__ = ["Game", "GameState", "Action", "GameMode", "PlayerSkin", "RandomMazeAlgorithm", "RenderMode", "StartingLocation", "PyRatException",
           "Player", "FixedPlayer",
           "Graph", "Maze", "RandomMaze", "BigHolesRandomMaze", "HolesOnSideRandomMaze", "UniformHolesRandomMaze", "MazeFromDict", "MazeFromMatrix",
           "RenderingEngine", "ShellRenderingEngine", "PygameRenderingEngine"]

##########################################################################################
##########################################################################################
