#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# Please import necessary elements using the following syntax:
#     from pyrat import <element_name>

"""
This module provides the main game loop and manages the game state.
It initializes the game with the specified parameters, manages players, and handles the game rendering.
It is the core of the PyRat game engine, allowing players to interact with the maze and each other.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
import copy
import math
import multiprocessing
import multiprocessing.managers as mpmanagers
import time
import traceback
import sys
import os
import datetime
import random

# PyRat imports
from pyrat.src.Maze import Maze
from pyrat.src.HolesOnSideRandomMaze import HolesOnSideRandomMaze
from pyrat.src.UniformHolesRandomMaze import UniformHolesRandomMaze
from pyrat.src.BigHolesRandomMaze import BigHolesRandomMaze
from pyrat.src.MazeFromDict import MazeFromDict
from pyrat.src.MazeFromMatrix import MazeFromMatrix
from pyrat.src.Player import Player
from pyrat.src.GameState import GameState
from pyrat.src.RenderingEngine import RenderingEngine
from pyrat.src.ShellRenderingEngine import ShellRenderingEngine
from pyrat.src.PygameRenderingEngine import PygameRenderingEngine
from pyrat.src.enums import RenderMode, GameMode, Action, StartingLocation, PlayerSkin, RandomMazeAlgorithm
from pyrat.src.utils import is_valid_directory

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class Game ():

    """
    A game is a class that allows to play a game of PyRat.
    It is initialized with the parameters of the game.
    Players should then be added to the game using the ``add_player()`` method.
    Finally, the ``start()`` method should be called to start the game.
    Once the game is over, it will provide statistics about the game.

    Set your own parameters to define interesting objectives for the players.
    However, make sure that parameters make sense together.
    For instance, you cannot set a number of cheese that is larger than the number of cells in the maze.

    To ease creating games, we provide a set of default parameters.
    These are used when the parameters are not set in the constructor:
    """

    DEFAULT_RANDOM_SEED = None
    DEFAULT_RANDOM_SEED_MAZE = None
    DEFAULT_RANDOM_SEED_CHEESE = None
    DEFAULT_RANDOM_SEED_PLAYERS = None
    DEFAULT_MAZE_WIDTH = 15
    DEFAULT_MAZE_HEIGHT = 13
    DEFAULT_CELL_PERCENTAGE = 80.0
    DEFAULT_WALL_PERCENTAGE = 60.0
    DEFAULT_MUD_PERCENTAGE = 20.0
    DEFAULT_MUD_RANGE = (4, 9)
    DEFAULT_FIXED_MAZE = None
    DEFAULT_RANDOM_MAZE_ALGORITHM = RandomMazeAlgorithm.BIG_HOLES
    DEFAULT_NB_CHEESE = 21
    DEFAULT_FIXED_CHEESE = None
    DEFAULT_RENDER_MODE = RenderMode.GUI
    DEFAULT_RENDER_SIMPLIFIED = False
    DEFAULT_RENDERING_SPEED = 1.0
    DEFAULT_TRACE_LENGTH = 0
    DEFAULT_FULLSCREEN = False
    DEFAULT_CLEAR_SHELL_EACH_TURN = True
    DEFAULT_SAVE_PATH = "."
    DEFAULT_SAVE_GAME = False
    DEFAULT_PREPROCESSING_TIME = 3.0
    DEFAULT_TURN_TIME = 0.1
    DEFAULT_GAME_MODE_SINGLE_TEAM = GameMode.SEQUENTIAL
    DEFAULT_GAME_MODE_MULTI_TEAM = GameMode.MATCH
    DEFAULT_CONTINUE_ON_ERROR = False
    
    #############################################################################################################################################
    #                                                               MAGIC METHODS                                                               #
    #############################################################################################################################################

    def __init__ ( self,
                   random_seed:           int | None = None,
                   random_seed_maze:      int | None = None,
                   random_seed_cheese:    int | None = None,
                   random_seed_players:   int | None = None,
                   maze_width:            int | None = None,
                   maze_height:           int | None = None,
                   cell_percentage:       float | None = None,
                   wall_percentage:       float | None = None,
                   mud_percentage:        float | None = None,
                   mud_range:             tuple[int, int] | None = None,
                   fixed_maze:            Maze | dict[int, dict[int, int]] | object | None = None, # Object for numpy.ndarray or torch.tensor (not listed to have an optional dependency on these libraries)
                   nb_cheese:             int | None = None,
                   fixed_cheese:          list[int] | None = None,
                   random_maze_algorithm: RandomMazeAlgorithm | None = None,
                   render_mode:           RenderMode | None = None,
                   render_simplified:     bool | None = None,
                   rendering_speed:       float | None = None,
                   trace_length:          int | None = None,
                   fullscreen:            bool | None = None,
                   clear_shell_each_turn: bool | None = None,
                   save_path:             str | None = None,
                   save_game:             bool | None = None,
                   preprocessing_time:    float | None = None,
                   turn_time:             float | None = None,
                   game_mode:             GameMode | None = None,
                   continue_on_error:     bool | None = None
                 ) ->                     None:

        """
        Initializes a new instance of the class.
        Any unset parameter will be set to its default value defined in the class.

        Args:
            random_seed:           Global random seed for all elements, or ``None`` for a random value.
            random_seed_maze:      Random seed for maze generation, or ``None`` for a random value.
            random_seed_cheese:    Random seed for cheese distribution, or ``None`` for a random value.
            random_seed_players:   Random seed for initial player locations, or ``None`` for a random value.
            maze_width:            Width of the maze (number of cells).
            maze_height:           Height of the maze (number of cells).
            cell_percentage:       Percentage of accessible cells in the maze (0% = useless maze, 100% = full rectangle).
            wall_percentage:       Percentage of walls in the maze (0% = empty, 100% = max walls while connected).
            mud_percentage:        Percentage of adjacent cell pairs separated by mud.
            mud_range:             Interval of turns needed to cross mud.
            fixed_maze:            Fixed maze in any PyRat-accepted representation (``Maze``, ``dict``, ``numpy.ndarray``, or ``torch.tensor``).
            random_maze_algorithm: Algorithm to generate the maze.
            nb_cheese:             Number of pieces of cheese in the maze.
            fixed_cheese:          Fixed list of cheese locations.
            render_mode:           Method to display the game.
            render_simplified:     If ``True``, hides non-essential elements in rendering.
            rendering_speed:       Controls the speed of the game when rendering.
            trace_length:          Maximum trace length to display (GUI rendering only).
            fullscreen:            If ``True``, renders the game in fullscreen (GUI only).
            clear_shell_each_turn: If ``True``, clears the shell each turn (shell rendering only).
            save_path:             Path where games are saved.
            save_game:             If ``True``, saves the game.
            preprocessing_time:    Time given to players before the game starts.
            turn_time:             Time after which players miss a turn.
            game_mode:             Indicates concurrency mode for players.
            continue_on_error:     If ``True``, continues the game if a player crashes.
        """
        
        # Debug
        assert isinstance(random_seed, (int, type(None))), "Argument 'random_seed' must be an integer or None (if so, default value 'Game.DEFAULT_RANDOM_SEED' is used)"
        assert isinstance(random_seed_maze, (int, type(None))), "Argument 'random_seed_maze' must be an integer or None (if so, default value 'Game.DEFAULT_RANDOM_SEED_MAZE' is used)"
        assert isinstance(random_seed_cheese, (int, type(None))), "Argument 'random_seed_cheese' must be an integer or None (if so, default value 'Game.DEFAULT_RANDOM_SEED_CHEESE' is used)"
        assert isinstance(random_seed_players, (int, type(None))), "Argument 'random_seed_players' must be an integer or None (if so, default value 'Game.DEFAULT_RANDOM_SEED_PLAYERS' is used)"
        assert random_seed is None or (random_seed is not None and 0 <= random_seed < sys.maxsize), "Argument 'random_seed' should be non-negative"
        assert random_seed_maze is None or (random_seed_maze is not None and 0 <= random_seed_maze < sys.maxsize), "Argument 'random_seed_maze' should be a positive integer"
        assert random_seed_cheese is None or (random_seed_cheese is not None and 0 <= random_seed_cheese < sys.maxsize), "Argument 'random_seed_cheese' should be a positive integer"
        assert random_seed_players is None or (random_seed_players is not None and 0 <= random_seed_players < sys.maxsize), "Argument 'random_seed_players' should be a positive integer"
        assert random_seed is None or (random_seed is not None and all([param is None for param in [random_seed_maze, random_seed_cheese, random_seed_players]])), "Argument 'random_seed' should be given if and only if no other random seed is given"
        assert isinstance(render_mode, (RenderMode, type(None))), "Argument 'render_mode' must be of type 'pyrat.RenderMode' or None (if so, default value 'Game.DEFAULT_RENDER_MODE' is used)"
        assert isinstance(turn_time, (float, type(None))), "Argument 'turn_time' must be a real number or None (if so, default value 'Game.DEFAULT_TURN_TIME' is used)"
        assert turn_time is None or turn_time >= 0, "Argument 'turn_time' should be non-negative"
        assert isinstance(preprocessing_time, (float, type(None))), "Argument 'preprocessing_time' must be a real number or None (if so, default value 'Game.DEFAULT_PREPROCESSING_TIME' is used)"
        assert preprocessing_time is None or preprocessing_time >= 0, "Argument 'preprocessing_time' should be non-negative"
        assert isinstance(game_mode, (GameMode, type(None))), "Argument 'game_mode' must be of type 'pyrat.GameMode' or None (if so, default value 'Game.DEFAULT_GAME_MODE_SINGLE' or 'Game.DEFAULT_GAME_MODE_MULTI' is used)"
        assert isinstance(continue_on_error, (bool, type(None))), "Argument 'continue_on_error' must be a boolean or None (if so, default value 'Game.DEFAULT_CONTINUE_ON_ERROR' is used)"
        assert not(game_mode == GameMode.SIMULATION and render_mode == RenderMode.GUI), "Cannot render GUI in simulation mode"
        assert fixed_maze is None or (fixed_maze is not None and all(param is None for param in [random_seed_maze, random_maze_algorithm, maze_width, maze_height, cell_percentage, wall_percentage, mud_percentage, mud_range])), "Argument 'fixed_maze' should be given if and only if no other maze description is given"
        assert fixed_cheese is None or (fixed_cheese is not None and all(param is None for param in [random_seed_cheese, nb_cheese])), "Argument 'fixed_cheese' should be given if and only if no other cheese description is given"
        assert game_mode is None or game_mode != GameMode.SIMULATION or (game_mode == GameMode.SIMULATION and all([param is None for param in [render_mode, preprocessing_time, turn_time]])), "Some parameters should be set when running in simulation mode"
        assert not(render_mode not in [None, RenderMode.GUI] and any([param is not None for param in [trace_length, fullscreen]])), "Some parameters should be set only when rendering in GUI mode"
        assert not(render_mode not in [RenderMode.ASCII, RenderMode.ANSI] and clear_shell_each_turn is not None), "Parameter 'clear_shell_each_turn' should be set only when rendering in shell mode"
        assert not(render_mode == RenderMode.NO_RENDERING and rendering_speed is not None), "Parameter 'rendering_speed' should be set only when rendering in GUI or shell mode"
        assert isinstance(random_maze_algorithm, (RandomMazeAlgorithm, type(None))), "Argument 'random_maze_algorithm' must be of type 'pyrat.RandomMazeAlgorithm' or None (if so, default value 'Game.DEFAULT_RANDOM_MAZE_ALGORITHM' is used)"
        assert isinstance(save_game, (bool, type(None))), "Argument 'save_game' must be a boolean or None (if so, default value 'Game.DEFAULT_SAVE_GAME' is used)"
        assert isinstance(save_path, (str, type(None))), "Argument 'save_path' must be a string or None (if so, default value 'Game.DEFAULT_SAVE_PATH' is used)"
        assert save_path is None or is_valid_directory(save_path), "Argument 'save_path' must be a valid directory"

        # Store given parameters or default values
        self.__random_seed = random_seed if random_seed is not None else Game.DEFAULT_RANDOM_SEED
        self.__random_seed_maze = random_seed_maze if random_seed_maze is not None else Game.DEFAULT_RANDOM_SEED_MAZE
        self.__random_seed_cheese = random_seed_cheese if random_seed_cheese is not None else Game.DEFAULT_RANDOM_SEED_CHEESE
        self.__random_seed_players = random_seed_players if random_seed_players is not None else Game.DEFAULT_RANDOM_SEED_PLAYERS
        self.__maze_width = maze_width if maze_width is not None else Game.DEFAULT_MAZE_WIDTH
        self.__maze_height = maze_height if maze_height is not None else Game.DEFAULT_MAZE_HEIGHT
        self.__cell_percentage = cell_percentage if cell_percentage is not None else Game.DEFAULT_CELL_PERCENTAGE
        self.__wall_percentage = wall_percentage if wall_percentage is not None else Game.DEFAULT_WALL_PERCENTAGE
        self.__mud_percentage = mud_percentage if mud_percentage is not None else Game.DEFAULT_MUD_PERCENTAGE
        self.__mud_range = mud_range if mud_range is not None else Game.DEFAULT_MUD_RANGE
        self.__fixed_maze = fixed_maze if fixed_maze is not None else Game.DEFAULT_FIXED_MAZE
        self.__random_maze_algorithm = random_maze_algorithm if random_maze_algorithm is not None else Game.DEFAULT_RANDOM_MAZE_ALGORITHM
        self.__nb_cheese = nb_cheese if nb_cheese is not None else Game.DEFAULT_NB_CHEESE
        self.__fixed_cheese = fixed_cheese if fixed_cheese is not None else Game.DEFAULT_FIXED_CHEESE
        self.__render_mode = render_mode if render_mode is not None else Game.DEFAULT_RENDER_MODE
        self.__render_simplified = render_simplified if render_simplified is not None else Game.DEFAULT_RENDER_SIMPLIFIED
        self.__rendering_speed = rendering_speed if rendering_speed is not None else Game.DEFAULT_RENDERING_SPEED
        self.__trace_length = trace_length if trace_length is not None else Game.DEFAULT_TRACE_LENGTH
        self.__fullscreen = fullscreen if fullscreen is not None else Game.DEFAULT_FULLSCREEN
        self.__clear_shell_each_turn = clear_shell_each_turn if clear_shell_each_turn is not None else Game.DEFAULT_CLEAR_SHELL_EACH_TURN
        self.__save_path = save_path if save_path is not None else Game.DEFAULT_SAVE_PATH
        self.__save_game = save_game if save_game is not None else Game.DEFAULT_SAVE_GAME
        self.__preprocessing_time = preprocessing_time if preprocessing_time is not None else Game.DEFAULT_PREPROCESSING_TIME
        self.__turn_time = turn_time if turn_time is not None else Game.DEFAULT_TURN_TIME
        self.__continue_on_error = continue_on_error if continue_on_error is not None else Game.DEFAULT_CONTINUE_ON_ERROR
        
        # We will set the game mode later, as it depends on the number of players
        self.__asked_game_mode = game_mode
        self.__game_mode = game_mode

        # If the game is in simulation mode, we enforce some parameters
        if self.__asked_game_mode == GameMode.SIMULATION:
            self.__preprocessing_time = 0.0
            self.__turn_time = 0.0
            self.__render_mode = RenderMode.NO_RENDERING
            self.__game_mode = GameMode.SEQUENTIAL

        # Private attributes
        self.__game_random_seed_maze = None
        self.__game_random_seed_cheese = None
        self.__game_random_seed_players = None
        self.__players_rng = None
        self.__players_asked_location = []
        self.__players = []
        self.__initial_game_state = None
        self.__player_traces = None
        self.__actions_history = None
        self.__rendering_engine = None
        self.__maze = None
        self.__reset_called = False

        # Initialize the game
        self.reset()

    #############################################################################################################################################

    def __str__ (self) -> str:

        """
        Returns a string representation of the object.

        Returns:
            String representation of the object.
        """
        
        # Create the string
        string = "Game object:\n"
        string += "|  Random seed: {}\n".format(self.__random_seed)
        string += "|  Random seed for maze: {}\n".format(self.__random_seed_maze)
        string += "|  Random seed for cheese: {}\n".format(self.__random_seed_cheese)
        string += "|  Random seed for players: {}\n".format(self.__random_seed_players)
        string += "|  Maze width: {}\n".format(self.__maze_width)
        string += "|  Maze height: {}\n".format(self.__maze_height)
        string += "|  Cell percentage: {}\n".format(self.__cell_percentage)
        string += "|  Wall percentage: {}\n".format(self.__wall_percentage)
        string += "|  Mud percentage: {}\n".format(self.__mud_percentage)
        string += "|  Mud range: {}\n".format(self.__mud_range)
        string += "|  Fixed maze: {}\n".format(self.__fixed_maze)
        string += "|  Random maze algorithm: {}\n".format(self.__random_maze_algorithm)
        string += "|  Number of cheese: {}\n".format(self.__nb_cheese)
        string += "|  Fixed cheese: {}\n".format(self.__fixed_cheese)
        string += "|  Render mode: {}\n".format(self.__render_mode)
        string += "|  Render simplified: {}\n".format(self.__render_simplified)
        string += "|  Rendering speed: {}\n".format(self.__rendering_speed)
        string += "|  Trace length: {}\n".format(self.__trace_length)
        string += "|  Fullscreen: {}\n".format(self.__fullscreen)
        string += "|  Clear shell each turn: {}\n".format(self.__clear_shell_each_turn)
        string += "|  Save path: {}\n".format(self.__save_path)
        string += "|  Save game: {}\n".format(self.__save_game)
        string += "|  Preprocessing time: {}\n".format(self.__preprocessing_time)
        string += "|  Turn time: {}\n".format(self.__turn_time)
        string += "|  Game mode: {}\n".format(self.__game_mode)
        string += "|  Continue on error: {}\n".format(self.__continue_on_error)
        return string

    #############################################################################################################################################
    #                                                              PUBLIC METHODS                                                              #
    #############################################################################################################################################

    def add_player ( self,
                     player:   Player,
                     team:     str = "",
                     location: StartingLocation | int = StartingLocation.CENTER
                   ) ->        None:
        
        """
        Adds a player to the game.
        In a PyRat game, players are identified by their name, which should be unique.
        If a player with the same name is added, an error will be raised.

        If the target location is not reachable (if there is a hole), the player will be placed at the closest reachable location.

        Args:
            player:   Player to add.
            team:     Team of the player.
            location: Initial location of the player (fixed index or value of the ``StartingLocation`` enumeration).
        """

        # Debug
        assert isinstance(player, Player), "Argument 'player' must be of type 'pyrat.Player'"
        assert isinstance(team, str), "Argument 'team' must be a string"
        assert isinstance(location, (StartingLocation, int)), "Argument 'location' must be of type 'pyrat.StartingLocation' or an integer, corresponding to the index of the cell where the player should start"
        assert location in list(StartingLocation) or (isinstance(location, int) and self.__maze.i_exists(location)), "Argument 'location' must be a valid index of the maze or a value of the 'pyrat.StartingLocation' enumeration"
        assert player.get_name() not in self.__player_traces, "Player '%s' was already added to the game" % player.get_name()
        assert not (location == StartingLocation.SAME and len(self.__players) == 0), "Cannot start player '%s' at the same location as the previous player if no player was added before" % player.get_name()

        # Set initial location
        self.__players_asked_location.append(location)
        corrected_location = location
        if location == StartingLocation.RANDOM:
            corrected_location = self.__players_rng.choice(self.__maze.get_vertices())
        elif location == StartingLocation.SAME:
            corrected_location = list(self.__initial_game_state.player_locations.values())[-1]
        elif location == StartingLocation.CENTER:
            corrected_location = self.__maze.rc_to_i(self.__maze.get_height() // 2, self.__maze.get_width() // 2)
        elif location == StartingLocation.TOP_LEFT:
            corrected_location = self.__maze.rc_to_i(0, 0)
        elif location == StartingLocation.TOP_RIGHT:
            corrected_location = self.__maze.rc_to_i(0, self.__maze.get_width() - 1)
        elif location == StartingLocation.BOTTOM_LEFT:
            corrected_location = self.__maze.rc_to_i(self.__maze.get_height() - 1, 0)
        elif location == StartingLocation.BOTTOM_RIGHT:
            corrected_location = self.__maze.rc_to_i(self.__maze.get_height() - 1, self.__maze.get_width() - 1)
        
        # If the location is not reachable, we choose the closest reachable location
        if self.__maze.i_exists(corrected_location):
            self.__initial_game_state.player_locations[player.get_name()] = corrected_location
        else:
            valid_cells = self.__maze.get_vertices()
            distances = [math.dist(self.__maze.i_to_rc(corrected_location), self.__maze.i_to_rc(cell)) for cell in valid_cells]
            _, argmin_distance = min((val, idx) for (idx, val) in enumerate(distances))
            self.__initial_game_state.player_locations[player.get_name()] = valid_cells[argmin_distance]

        # Append to team
        if team not in self.__initial_game_state.teams:
            self.__initial_game_state.teams[team] = []
        self.__initial_game_state.teams[team].append(player.get_name())

        # Initialize other elements of game state
        self.__initial_game_state.score_per_player[player.get_name()] = 0
        self.__initial_game_state.muds[player.get_name()] = {"target": None, "count": 0}

        # Other attributes
        self.__players.append(player)
        self.__player_traces[player.get_name()] = []
        self.__actions_history[player.get_name()] = []
        
    #############################################################################################################################################

    def reset ( self,
                keep_players: bool = True,
                same:         bool = True
              ) ->            None:
        
        """
        Resets the game to its initial state.
        The initial state is defined by the parameters given in the constructor.

        If the game was generated with random elements, we will generate new random elements or keep the same ones, depending on the ``same`` parameter.
        If ``same`` is ``True``, we will keep the same random seeds that were used to generate the previous game.
        If ``same`` is ``False``, we will generate new random seeds for the game, based on what was provided in the constructor.

        Note that even if you set  ``same`` to ``False`` but you provided random seeds in the constructor, the game will use these random seeds.
        Thus, if you declare ``same=False`` but created a game with ``random_seed=42``, this will be equivalent ``same=True``.
        
        Another example: if you declare ``same=False`` but created a game with ``random_seed_maze=42``, the game will happen on the same maze as before, but with a different cheese distribution and random initial player locations.

        Args:
            keep_players: If ``True``, keeps the players in the game, otherwise removes them.
            same:         If ``True``, keeps the same random seeds as before, otherwise generates new random seeds.
        """
        
        # Debug
        assert isinstance(keep_players, bool), "Argument 'keep_players' must be a boolean"
        assert isinstance(same, bool), "Argument 'same' must be a boolean"

        # Set random seeds for the game
        if not same or self.__game_random_seed_maze is None:
            self.__game_random_seed_maze = self.__random_seed if self.__random_seed is not None else self.__random_seed_maze if self.__random_seed_maze is not None else random.randint(0, sys.maxsize - 1)
            self.__game_random_seed_cheese = self.__random_seed if self.__random_seed is not None else self.__random_seed_cheese if self.__random_seed_cheese is not None else random.randint(0, sys.maxsize - 1)
            self.__game_random_seed_players = self.__random_seed if self.__random_seed is not None else self.__random_seed_players if self.__random_seed_players is not None else random.randint(0, sys.maxsize - 1)
        self.__players_rng = random.Random(self.__game_random_seed_players)
        
        # Reset game elements
        self.__player_traces = {}
        self.__actions_history = {}
        if not self.__asked_game_mode:
            self.__game_mode = None
        
        # Initialize the maze
        if isinstance(self.__fixed_maze, Maze):
            self.__maze = copy.deepcopy(self.__fixed_maze)
        elif isinstance(self.__fixed_maze, dict):
            self.__maze = MazeFromDict(self.__fixed_maze)
        elif self.__fixed_maze is not None:
            self.__maze = MazeFromMatrix(self.__fixed_maze)
        elif self.__random_maze_algorithm == RandomMazeAlgorithm.UNIFORM_HOLES:
            self.__maze = UniformHolesRandomMaze(self.__cell_percentage, self.__wall_percentage, self.__mud_percentage, self.__mud_range, self.__game_random_seed_maze, self.__maze_width, self.__maze_height)
        elif self.__random_maze_algorithm == RandomMazeAlgorithm.HOLES_ON_SIDE:
            self.__maze = HolesOnSideRandomMaze(self.__cell_percentage, self.__wall_percentage, self.__mud_percentage, self.__mud_range, self.__game_random_seed_maze, self.__maze_width, self.__maze_height)
        elif self.__random_maze_algorithm == RandomMazeAlgorithm.BIG_HOLES:
            self.__maze = BigHolesRandomMaze(self.__cell_percentage, self.__wall_percentage, self.__mud_percentage, self.__mud_range, self.__game_random_seed_maze, self.__maze_width, self.__maze_height)

        # Initialize the rendering engine
        if self.__render_mode in [RenderMode.ASCII, RenderMode.ANSI]:
            use_colors = self.__render_mode == RenderMode.ANSI
            self.__rendering_engine = ShellRenderingEngine(use_colors, self.__clear_shell_each_turn, self.__rendering_speed, self.__render_simplified)
        elif self.__render_mode == RenderMode.GUI:
            self.__rendering_engine = PygameRenderingEngine(self.__fullscreen, self.__trace_length, self.__rendering_speed, self.__render_simplified)
        elif self.__render_mode == RenderMode.NO_RENDERING:
            self.__rendering_engine = RenderingEngine(self.__rendering_speed, self.__render_simplified)
        
        # Initialize the game state
        previous_initial_state = copy.deepcopy(self.__initial_game_state)
        self.__initial_game_state = GameState()

        # Add players as they were added
        for i in range(len(self.__players)):
            player = self.__players.pop(0)
            player_asked_location = self.__players_asked_location.pop(0)
            if keep_players:
                player_team = [team for team in previous_initial_state.teams if player.get_name() in previous_initial_state.teams[team]][0]
                self.add_player(player, player_team, player_asked_location)

        # Indicate that the game was reset
        self.__reset_called = True

    #############################################################################################################################################

    def start (self) -> dict[str, object]:

        """
        Starts a game, asking players for decisions until the game is over.

        Returns:
            Game statistics computed during the game.
        """
        
        # Debug
        assert len(self.__players) > 0, "No player was added to the game"
        assert self.__reset_called, "The game was not reset before starting"

        # We catch exceptions that may happen during the game
        try:
        
            # Set the game mode if needed
            if self.__game_mode is None:
                self.__game_mode = Game.DEFAULT_GAME_MODE_SINGLE_TEAM if len(self.__initial_game_state.teams) == 1 else Game.DEFAULT_GAME_MODE_MULTI_TEAM

            # Mark the game as not reset
            self.__reset_called = False

            # Initialize stats
            stats = {"players": {}, "turns": -1}
            for player in self.__players:
                stats["players"][player.get_name()] = {"score": 0,
                                                       "preprocessing_duration": None,
                                                       "turn_durations": [],
                                                       "team": [team for team in self.__initial_game_state.teams if player.get_name() in self.__initial_game_state.teams[team]][0],
                                                       "actions": {Action.NOTHING.value: 0,
                                                                   Action.NORTH.value: 0,
                                                                   Action.EAST.value: 0,
                                                                   Action.SOUTH.value: 0,
                                                                   Action.WEST.value: 0,
                                                                   "mud": 0,
                                                                   "error": 0,
                                                                   "miss": 0,
                                                                   "wall" : 0}}
            
            # In multiprocessing mode, prepare processes
            maze_per_player = {player.get_name(): copy.deepcopy(self.__maze) for player in self.__players}
            if self.__game_mode in [GameMode.MATCH, GameMode.SYNCHRONOUS]:

                # Create a process per player
                turn_start_synchronizer = multiprocessing.Manager().Barrier(len(self.__players) + 1)
                turn_timeout_lock = multiprocessing.Manager().Lock()
                player_processes = {}
                for player in self.__players:
                    player_processes[player.get_name()] = {"process": None, "input_queue": multiprocessing.Manager().Queue(), "output_queue": multiprocessing.Manager().Queue(), "turn_end_synchronizer": multiprocessing.Manager().Barrier(2)}
                    player_processes[player.get_name()]["process"] = multiprocessing.Process(target=_player_process_function, args=(player, maze_per_player[player.get_name()], player_processes[player.get_name()]["input_queue"], player_processes[player.get_name()]["output_queue"], turn_start_synchronizer, turn_timeout_lock, player_processes[player.get_name()]["turn_end_synchronizer"], None, None,))
                    player_processes[player.get_name()]["process"].start()

                # If playing in match mode, we create processs to wait instead of missing players
                if self.__game_mode == GameMode.MATCH:
                    waiter_processes = {}
                    for player in self.__players:
                        waiter_processes[player.get_name()] = {"process": None, "input_queue": multiprocessing.Manager().Queue()}
                        waiter_processes[player.get_name()]["process"] = multiprocessing.Process(target=_waiter_process_function, args=(waiter_processes[player.get_name()]["input_queue"], turn_start_synchronizer,))
                        waiter_processes[player.get_name()]["process"].start()

            # Add cheese
            available_cells = [i for i in self.__maze.get_vertices() if i not in self.__initial_game_state.player_locations.values()]
            self.__initial_game_state.cheese.extend(self.__distribute_cheese(available_cells))
            game_state = copy.deepcopy(self.__initial_game_state)
            
            # Initial rendering of the maze
            self.__rendering_engine.render(self.__players, self.__maze, game_state)
            
            # We play until the game is over
            players_ready = [player for player in self.__players]
            players_running = {player.get_name(): True for player in self.__players}
            all_action_names = [action.value for action in Action]
            while any(players_running.values()):

                # We communicate the state of the game to the players not in mud
                game_phases = {player.get_name(): "none" for player in self.__players}
                turn_actions = {player.get_name(): "miss" for player in self.__players}
                durations = {player.get_name(): None for player in self.__players}
                for ready_player in players_ready:
                    final_stats = copy.deepcopy(stats) if game_state.game_over() else {}
                    player_game_state = copy.deepcopy(game_state)
                    if self.__game_mode in [GameMode.MATCH, GameMode.SYNCHRONOUS]:
                        player_processes[ready_player.get_name()]["input_queue"].put((player_game_state, final_stats))
                    else:
                        turn_actions[ready_player.get_name()], game_phases[ready_player.get_name()], durations[ready_player.get_name()] = _player_process_function(ready_player, maze_per_player[ready_player.get_name()], None, None, None, None, None, player_game_state, final_stats)
                
                # In multiprocessing mode, we for everybody to receive data to start
                # In sequential mode, decisions are already received at this point
                if self.__game_mode in [GameMode.MATCH, GameMode.SYNCHRONOUS]:
                    turn_start_synchronizer.wait()

                # Wait a bit
                sleep_time = self.__preprocessing_time if game_state.turn == 0 else self.__turn_time
                time.sleep(sleep_time)

                # In synchronous mode, we wait for everyone
                if self.__game_mode == GameMode.SYNCHRONOUS:
                    for player in self.__players:
                        player_processes[player.get_name()]["turn_end_synchronizer"].wait()
                        turn_actions[player.get_name()], game_phases[player.get_name()], durations[player.get_name()] = player_processes[player.get_name()]["output_queue"].get()

                # In match mode, we block the possibility to return an action and check who answered in time
                elif self.__game_mode == GameMode.MATCH:

                    # Wait at least for those in mud
                    for player in self.__players:
                        if game_state.is_in_mud(player.get_name()) and players_running[player.get_name()]:
                            player_processes[player.get_name()]["turn_end_synchronizer"].wait()
                            turn_actions[player.get_name()], game_phases[player.get_name()], durations[player.get_name()] = player_processes[player.get_name()]["output_queue"].get()

                    # For others, set timeout and wait for output info of those who passed just before timeout
                    with turn_timeout_lock:
                        for player in self.__players:
                            if not game_state.is_in_mud(player.get_name()) and players_running[player.get_name()]:
                                if not player_processes[player.get_name()]["output_queue"].empty():
                                    player_processes[player.get_name()]["turn_end_synchronizer"].wait()
                                    turn_actions[player.get_name()], game_phases[player.get_name()], durations[player.get_name()] = player_processes[player.get_name()]["output_queue"].get()

                # Check which players are ready to continue
                players_ready = []
                for player in self.__players:
                    if game_phases[player.get_name()] == "postprocessing":
                        players_running[player.get_name()] = False
                    if self.__game_mode == GameMode.MATCH and (game_phases[player.get_name()] == "postprocessing" or turn_actions[player.get_name()] == "miss"):
                        waiter_processes[player.get_name()]["input_queue"].put(True)
                    else:
                        players_ready.append(player)

                # Check for errors
                if any([turn_actions[player.get_name()] == "error" for player in self.__players]) and not self.__continue_on_error:
                    raise Exception("A player has crashed, exiting")

                # We save the turn info if we are not postprocessing
                if not game_state.game_over():
                
                    # Apply the actions
                    corrected_actions = {player.get_name(): Action(turn_actions[player.get_name()]) if turn_actions[player.get_name()] in all_action_names else Action.NOTHING for player in self.__players}
                    new_game_state = self.__determine_new_game_state(game_state, corrected_actions)

                    # Save stats
                    for player in self.__players:
                        if game_phases[player.get_name()] == "none":
                            stats["players"][player.get_name()]["actions"]["miss"] += 1
                        elif game_phases[player.get_name()] != "preprocessing":
                            if turn_actions[player.get_name()] in all_action_names and turn_actions[player.get_name()] != Action.NOTHING.value and game_state.player_locations[player.get_name()] == new_game_state.player_locations[player.get_name()] and not new_game_state.is_in_mud(player.get_name()):
                                stats["players"][player.get_name()]["actions"]["wall"] += 1
                            else:
                                stats["players"][player.get_name()]["actions"][turn_actions[player.get_name()]] += 1
                            if turn_actions[player.get_name()] != "mud":
                                self.__actions_history[player.get_name()].append(corrected_actions[player.get_name()])
                        if durations[player.get_name()] is not None:
                            if game_phases[player.get_name()] == "preprocessing":
                                stats["players"][player.get_name()]["preprocessing_duration"] = durations[player.get_name()]
                            else:
                                stats["players"][player.get_name()]["turn_durations"].append(durations[player.get_name()])
                        stats["players"][player.get_name()]["score"] = new_game_state.score_per_player[player.get_name()]
                    stats["turns"] = game_state.turn
                    
                    # Go to next turn
                    self.__rendering_engine.render(self.__players, self.__maze, new_game_state)
                    game_state = new_game_state

        # In case of an error, we ignore stats
        except:
            print(traceback.format_exc(), file=sys.stderr)
            stats = {}
        
        # Apply end actions before returning
        self.__end(stats == {})
        return stats

    #############################################################################################################################################
    #                                                              PRIVATE METHODS                                                              #
    #############################################################################################################################################

    def __end ( self,
                game_crashed: bool,
              ) ->            None:
        
        """
        Actions to perform at the end of the game if needed.

        Args:
            game_crashed: Indicates if the game crashed.
        """

        # Debug
        assert isinstance(game_crashed, bool), "Argument 'game_crashed' must be a boolean"

        # We save the game if asked
        if self.__save_game and not game_crashed:
            
            # Create the saves directory if needed
            if not os.path.exists(self.__save_path):
                os.makedirs(self.__save_path)

            # Prepare the config dictionary
            config = {"game_mode": "{GAME_MODE}",
                      "fixed_maze": self.__maze.as_dict(),
                      "fixed_cheese": self.__initial_game_state.cheese}
            
            # Create a description of the players
            player_descriptions = []
            for player in self.__players:
                player_descriptions.append({"name": player.get_name(),
                                            "skin": "{SKIN_" + player.get_skin().name + "}",
                                            "team": [team for team in self.__initial_game_state.teams if player.get_name() in self.__initial_game_state.teams[team]][0],
                                            "location": self.__initial_game_state.player_locations[player.get_name()],
                                            "actions": "{ACTIONS_" + player.get_name() + "}"})

            # Create the players' file, forcing players to their initial locations
            output_file_name = os.path.join(self.__save_path, datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f.py"))
            with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "save_template.py"), "r") as save_template_file:
                save_template = save_template_file.read()
                save_template = save_template.replace("{PLAYERS}", str(player_descriptions).replace("}, ", "},\\n                       "))
                save_template = save_template.replace("{CONFIG}", str(config).replace(", '", ",\\n          '"))
                save_template = save_template.replace("'{GAME_MODE}'", "GameMode.SEQUENTIAL")
                for skin in PlayerSkin:
                    save_template = save_template.replace("'{SKIN_" + skin.get_name() + "}'", "PlayerSkin." + skin.get_name())
                for player in self.__players:
                    save_template = save_template.replace("'{ACTIONS_" + player.get_name() + "}'", "[" + ", ".join("Action." + action.get_name() for action in self.__actions_history[player.get_name()]) + "]")
                with open(output_file_name, "w") as output_file:
                    print(save_template, file=output_file)

        # Apply ending actions of the rendering engine
        self.__rendering_engine.end()
        
    #############################################################################################################################################

    def __determine_new_game_state ( self,
                                     game_state: GameState,
                                     actions:    dict[str, Action]
                                   ) ->          GameState:
        
        """
        Updates the game state after a turn, given decisions of players.

        Args:
            game_state: Current game state.
            actions:    Action performed per player.

        Returns:
            New game state after the turn.
        """

        # Debug
        assert isinstance(game_state, GameState), "Argument 'game_state' must be of type 'pyrat.GameState'"
        assert isinstance(actions, dict), "Argument 'actions' must be a dictionary"
        assert all(player_name in [player.get_name() for player in self.__players] for player_name in actions), "All players must be in the game"
        assert all(action in Action for action in actions.values()), "All actions must be of type 'pyrat.Action'"

        # Initialize new game state
        new_game_state = copy.deepcopy(game_state)
        new_game_state.turn += 1

        # Move all players accordingly
        for player in self.__players:
            row, col = self.__maze.i_to_rc(game_state.player_locations[player.get_name()])
            target = None
            if actions[player.get_name()] == Action.NORTH and row > 0:
                target = self.__maze.rc_to_i(row - 1, col)
            elif actions[player.get_name()] == Action.SOUTH and row < self.__maze.get_height() - 1:
                target = self.__maze.rc_to_i(row + 1, col)
            elif actions[player.get_name()] == Action.WEST and col > 0:
                target = self.__maze.rc_to_i(row, col - 1)
            elif actions[player.get_name()] == Action.EAST and col < self.__maze.get_width() - 1:
                target = self.__maze.rc_to_i(row, col + 1)
            if target is not None and self.__maze.i_exists(target) and self.__maze.has_edge(game_state.player_locations[player.get_name()], target):
                weight = self.__maze.get_weight(game_state.player_locations[player.get_name()], target)
                if weight == 1:
                    new_game_state.player_locations[player.get_name()] = target
                elif weight > 1:
                    new_game_state.muds[player.get_name()]["target"] = target
                    new_game_state.muds[player.get_name()]["count"] = weight

        # All players in mud advance a bit
        for player in self.__players:
            if new_game_state.is_in_mud(player.get_name()):
                new_game_state.muds[player.get_name()]["count"] -= 1
                if new_game_state.muds[player.get_name()]["count"] == 0:
                    new_game_state.player_locations[player.get_name()] = new_game_state.muds[player.get_name()]["target"]
                    new_game_state.muds[player.get_name()]["target"] = None

        # Update cheese and scores
        for c in game_state.cheese:
            players_on_cheese = [player for player in self.__players if c == new_game_state.player_locations[player.get_name()]]
            for player_on_cheese in players_on_cheese:
                new_game_state.score_per_player[player_on_cheese.get_name()] += 1.0 / len(players_on_cheese)
            if len(players_on_cheese) > 0:
                new_game_state.cheese.remove(c)
        
        # Store trace for GUI
        for player in self.__players:
            self.__player_traces[player.get_name()].append(new_game_state.player_locations[player.get_name()])
            self.__player_traces[player.get_name()] = self.__player_traces[player.get_name()][-self.__trace_length:]
        
        # Return new game state
        return new_game_state
        
    #############################################################################################################################################

    def __distribute_cheese ( self,
                              available_cells: list[int],
                            ) ->               list[int]:

        """
        Distributes pieces of cheese in the maze, according to the provided criteria.
        If a fixed list of cheese was provided, it is used.
        Otherwise, the cheese is distributed randomly.

        Args:
            available_cells: List of indices of cells that can be used to place cheese.

        Returns:
            List of indices of cells containing cheese.
        """
        
        # Debug
        assert isinstance(available_cells, list), "Argument 'available_cells' must be a list"
        assert all([isinstance(cell, int) for cell in available_cells]), "All elements of 'available_cells' must be integers"
        assert all([self.__maze.i_exists(cell) for cell in available_cells]), "All elements of 'available_cells' must be valid indices of the maze"

        # If we ask for a fixed list of cheese, we use it
        if self.__fixed_cheese is not None:
            
            # Debug
            assert isinstance(self.__fixed_cheese, list), "Attribute '__fixed_cheese' must be a list"
            assert all([isinstance(cell, int) for cell in self.__fixed_cheese]), "All elements of '__fixed_cheese' must be integers"
            assert len(set(self.__fixed_cheese)) == len(self.__fixed_cheese), "All elements of '__fixed_cheese' must be unique"
            assert len(available_cells) >= len(self.__fixed_cheese), "Not enough available cells to place the fixed cheese"
            assert all([self.__maze.i_exists(cell) for cell in self.__fixed_cheese]), "All elements of '__fixed_cheese' must be valid indices of the maze"
            assert all([cell in available_cells for cell in self.__fixed_cheese]), "All elements of '__fixed_cheese' must be in 'available_cells'"

            # Place the cheese
            cheese = copy.deepcopy(self.__fixed_cheese)

        # Otherwise, we place the cheese randomly
        else:
            
            # Debug
            assert isinstance(self.__nb_cheese, int), "Attribute '__nb_cheese' must be an integer"
            assert self.__nb_cheese > 0, "Attribute '__nb_cheese' must be positive"
            assert len(available_cells) >= self.__nb_cheese, "Not enough available cells to place the cheese"

            # Place the cheese randomly
            rng = random.Random(self.__game_random_seed_cheese)
            rng.shuffle(available_cells)
            cheese = available_cells[:self.__nb_cheese]

        # Return the cheese
        return cheese

#####################################################################################################################################################
##################################################################### FUNCTIONS #####################################################################
#####################################################################################################################################################

def _player_process_function ( player:                  Player,
                               maze:                    Maze,
                               input_queue:             mpmanagers.BaseProxy | None = None,
                               output_queue:            mpmanagers.BaseProxy | None = None,
                               turn_start_synchronizer: mpmanagers.BarrierProxy | None = None,
                               turn_timeout_lock:       mpmanagers.AcquirerProxy | None = None,
                               turn_end_synchronizer:   mpmanagers.BarrierProxy | None = None,
                               game_state:              GameState | None = None,
                               final_stats:             dict[str, object] | None = None,
                             ) ->                       tuple[str, str, float | None]:
    
    """
    This function is executed in a separate process per player.
    It handles the communication with the player and calls the functions given as arguments.
    It is defined outside of the class due to multiprocessing limitations.
    If not using multiprocessing, the function returns the action and the duration of the turn.

    Args:
        player:                  Player controlled by the process.
        maze:                    Maze in which the player plays.
        input_queue:             Queue to receive the game state (set if multiprocessing).
        output_queue:            Queue to send the action (set if multiprocessing).
        turn_start_synchronizer: Barrier to synchronize the start of the turn (set if multiprocessing).
        turn_timeout_lock:       Lock to synchronize the timeout of the turn (set if multiprocessing).
        turn_end_synchronizer:   Barrier to synchronize the end of the turn (set if multiprocessing).
        game_state:              Initial game state (set if sequential).
        final_stats:             Final stats (set if sequential).

    Returns:
        A tuple containing the action performed by the player, the phase of the game in which the player is, and the duration of the turn.
    """

    # Debug
    assert isinstance(player, Player), "Argument 'player' must be of type 'pyrat.Player'"
    assert isinstance(maze, Maze), "Argument 'maze' must be of type 'pyrat.Maze'"
    assert isinstance(input_queue, (mpmanagers.BaseProxy, type(None))), "Argument 'input_queue' must be of type 'multiprocessing.Queue' or None"
    assert isinstance(output_queue, (mpmanagers.BaseProxy, type(None))), "Argument 'output_queue' must be of type 'multiprocessing.Queue' or None"
    assert isinstance(turn_start_synchronizer, (mpmanagers.BarrierProxy, type(None))), "Argument 'turn_start_synchronizer' must be of type 'multiprocessing.Barrier' or None"
    assert isinstance(turn_timeout_lock, (mpmanagers.AcquirerProxy, type(None))), "Argument 'turn_timeout_lock' must be of type 'multiprocessing.Lock' or None"
    assert isinstance(turn_end_synchronizer, (mpmanagers.BarrierProxy, type(None))), "Argument 'turn_end_synchronizer' must be of type 'multiprocessing.Barrier' or None"
    assert isinstance(game_state, (GameState, type(None))), "Argument 'game_state' must be of type 'pyrat.GameState' or None"
    assert isinstance(final_stats, (dict, type(None))), "Argument 'final_stats' must be of type 'dict' or None"
    assert final_stats is None or all(isinstance(key, str) for key in final_stats), "Keys of 'final_stats' must be strings"
    assert (input_queue is None and output_queue is None and turn_start_synchronizer is None and turn_timeout_lock is None and turn_end_synchronizer is None) ^ (game_state is None and final_stats is None), "Some arguments are for multiprocessing mode, and others for sequential mode"
    
    # We catch exceptions that may happen during the game
    use_multiprocessing = input_queue is not None
    try:

        # Main loop
        while True:
            
            # In multiprocessing, wait for all players ready
            if use_multiprocessing:
                turn_start_synchronizer.wait()
                game_state, final_stats = input_queue.get()
            
            # Call the correct function
            game_phase = "turn"
            duration = None
            try:
                
                # Call postprocessing once the game is over
                if final_stats:
                    game_phase = "postprocessing"
                    action = "error"
                    player.postprocessing(maze, game_state, final_stats)
                    action = "ignore"
                    
                # If in mud, we return immediately (main process will wait for us in all cases)
                elif game_state.is_in_mud(player.get_name()):
                    action = "mud"
                
                # Otherwise, we ask for an action
                else:
                
                    # Measure start time
                    start = time.process_time()
                    
                    # Go
                    action = "error"
                    if game_state.turn == 0:
                        game_phase = "preprocessing"
                        player.preprocessing(maze, game_state)
                        action = "ignore"
                    else:
                        a = player.turn(maze, game_state)
                        if a not in list(Action):
                            raise Exception("Invalid action %s by player %s" % (str(a), player.get_name()))
                        action = a.value
                    
                    # Set end time
                    end_time = time.process_time()
                    duration = end_time - start
                        
            # Print error message in case of a crash
            except:
                print("Player %s has crashed with the following error:" % player.get_name(), file=sys.stderr)
                print(traceback.format_exc(), file=sys.stderr)
                    
            # Turn is over
            if use_multiprocessing:
                with turn_timeout_lock:
                    output_queue.put((action, game_phase, duration))
                turn_end_synchronizer.wait()
                if game_phase == "postprocessing":
                    break
            else:
                return action, game_phase, duration

    # Ignore
    except:
        pass

    # Default return when the process is killed
    # This is useless and there just to match the return type
    return "abort", "any", None

#####################################################################################################################################################

def _waiter_process_function ( input_queue:             mpmanagers.BaseProxy,
                               turn_start_synchronizer: mpmanagers.BarrierProxy,
                             ) ->                       None:
    
    """
    This function is executed in a separate process per player.
    It handles the timeouts of the player.
    It is defined outside of the class due to multiprocessing limitations.

    Args:
        input_queue:             Queue to receive the game state.
        turn_start_synchronizer: Barrier to synchronize the start of the turn.
    """

    # Debug
    assert isinstance(input_queue, mpmanagers.BaseProxy), "Argument 'input_queue' must be of type 'multiprocessing.Queue'"
    assert isinstance(turn_start_synchronizer, mpmanagers.BarrierProxy), "Argument 'turn_start_synchronizer' must be of type 'multiprocessing.Barrier'"

    # We catch exceptions that may happen during the game
    try:

        # We just mark as ready
        while True:
            _ = input_queue.get()
            turn_start_synchronizer.wait()

    # Ignore
    except:
        pass

#####################################################################################################################################################
#####################################################################################################################################################
