#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# Please import necessary elements using the following syntax:
#     from pyrat import <element_name>

"""
This module provides a rendering engine using the ``pygame`` library.
It will create a window and display the game in it.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
import copy
import multiprocessing
import os
import glob
import distinctipy
import math
import random
import time
import queue

# PyRat imports
from pyrat.src.RenderingEngine import RenderingEngine
from pyrat.src.Player import Player
from pyrat.src.Maze import Maze
from pyrat.src.GameState import GameState

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class PygameRenderingEngine (RenderingEngine):

    """
    *(This class inherits from* ``RenderingEngine`` *).*

    This rendering engine uses the ``pygame`` library to render the game.
    It will create a window and display the game in it.
    The window will run in a different process than the one running the game.
    """

    #############################################################################################################################################
    #                                                               MAGIC METHODS                                                               #
    #############################################################################################################################################

    def __init__ ( self,
                   fullscreen:   bool = False,
                   trace_length: int = 0,
                   *args:        object,
                   **kwargs:     object
                 ) ->            None:

        """
        Initializes a new instance of the class.

        Args:
            fullscreen:   Indicates if the GUI should be fullscreen.
            trace_length: Length of the trace to display.
            *args:        Arguments to pass to the parent constructor.
            **kwargs:     Keyword arguments to pass to the parent constructor.
        """

        # Inherit from parent class
        super().__init__(*args, **kwargs)

        # Debug
        assert isinstance(fullscreen, bool), "Argument 'fullscreen' must be a boolean"
        assert isinstance(trace_length, int), "Argument 'trace_length' must be an integer"
        assert trace_length >= 0, "Argument 'trace_length' must be positive"

        # Private attributes
        self.__fullscreen = fullscreen
        self.__trace_length = trace_length
        self.__gui_process = None
        self.__gui_queue = None

    #############################################################################################################################################
    #                                                               PUBLIC METHODS                                                              #
    #############################################################################################################################################

    def end (self) -> None:
        
        """
        *(This method redefines the method of the parent class with the same name).*
        
        It waits for the window to be closed before exiting.
        """

        # Wait for GUI to be exited to quit if there is one
        if self.__gui_process is not None:
            self.__gui_process.join()

    #############################################################################################################################################

    def render ( self,
                 players:    list[Player],
                 maze:       Maze,
                 game_state: GameState,
               ) ->          None:
        
        """
        *(This method redefines the method of the parent class with the same name).*

        This function renders the game to a ``pygame`` window.
        The window is created in a different process than the one running the game.
        
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

        # Initialize the GUI in a different process at turn 0
        if game_state.turn == 0:

            # Initialize the GUI process
            gui_initialized_synchronizer = multiprocessing.Manager().Barrier(2)
            self.__gui_queue = multiprocessing.Manager().Queue()
            self.__gui_process = multiprocessing.Process(target=_gui_process_function, args=(gui_initialized_synchronizer, self.__gui_queue, maze, game_state, players, self.__fullscreen, self._render_simplified, self.__trace_length, self._rendering_speed))
            self.__gui_process.start()
            gui_initialized_synchronizer.wait()
        
        # At each turn, send current info to the process
        else:
            self.__gui_queue.put(game_state)
        
#####################################################################################################################################################
##################################################################### FUNCTIONS #####################################################################
#####################################################################################################################################################

def _gui_process_function ( gui_initialized_synchronizer: multiprocessing.Barrier,
                            gui_queue:                    multiprocessing.Queue,
                            maze:                         Maze,
                            initial_game_state:           GameState,
                            players:                      list[Player],
                            fullscreen:                   bool,
                            render_simplified:            bool,
                            trace_length:                 int,
                            rendering_speed:              float
                          ) ->                            None:
    
    """
    This function is executed in a separate process for the GUI.
    It handles rendering in a ``pygame`` environment.
    It is defined outside of the class due to multiprocessing limitations.
    
    Args:
        gui_queue:          Queue to receive the game state.
        maze:               Maze of the game.
        initial_game_state: Initial game state.
        players:            Players of the game.
        fullscreen:         Indicates if the GUI should be fullscreen.
        render_simplified:  Indicates if the GUI should be simplified.
        trace_length:       Length of the trace to display.
        rendering_speed:    Speed at which the game should be rendered.
    """

    # Debug
    assert isinstance(gui_initialized_synchronizer, multiprocessing.managers.BarrierProxy), "Argument 'gui_initialized_synchronizer' must be a multiprocessing.Barrier"
    assert isinstance(gui_queue, multiprocessing.managers.BaseProxy), "Argument 'gui_queue' must be a multiprocessing.Queue"
    assert isinstance(maze, Maze), "Argument 'maze' must be of type 'pyrat.Maze'"
    assert isinstance(initial_game_state, GameState), "Argument 'initial_game_state' must be of type 'pyrat.GameState'"
    assert isinstance(players, list), "Argument 'players' must be a list"
    assert all(isinstance(player, Player) for player in players), "All elements of 'players' must be of type 'pyrat.Player'"
    assert isinstance(fullscreen, bool), "Argument 'fullscreen' must be a boolean"
    assert isinstance(render_simplified, bool), "Argument 'render_simplified' must be a boolean"
    assert isinstance(trace_length, int), "Argument 'trace_length' must be an integer"
    assert isinstance(rendering_speed, float), "Argument 'rendering_speed' must be a real number"
    assert trace_length >= 0, "Argument 'trace_length' must be positive"
    assert rendering_speed > 0.0, "Argument 'rendering_speed' must be positive"

    # We catch exceptions that may happen during the game
    try:

        # Initialize PyGame
        # Imports are done here to avoid multiple initializations in multiprocessing
        os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
        import pygame
        import pygame.locals as pglocals
        pygame.init()
        pygame.mixer.init()

        # Random number generator
        rng = random.Random()

        # Start screen
        if fullscreen:
            gui_screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
            pygame.display.toggle_fullscreen()
        else:
            gui_screen = pygame.display.set_mode((int(pygame.display.Info().current_w * 0.8), int(pygame.display.Info().current_h * 0.8)), pygame.SCALED)

        # We will store elements to display
        maze_elements = []
        avatar_elements = []
        player_elements = {}
        cheese_elements = {}
        
        # Parameters of the GUI
        window_width, window_height = pygame.display.get_surface().get_size()
        cell_size = int(min(window_width / maze.get_width(), window_height / maze.get_height()) * 0.9)
        background_color = (0, 0, 0)
        cell_text_color = (50, 50, 50)
        cell_text_offset = int(cell_size * 0.1)
        wall_size = cell_size // 7
        mud_text_color = (185, 155, 60)
        corner_wall_ratio = 1.2
        flag_size = int(cell_size * 0.4)
        flag_x_offset = int(cell_size * 0.2)
        flag_x_next_offset = int(cell_size * 0.07)
        flag_y_offset = int(cell_size * 0.3)
        game_area_width = cell_size * maze.get_width()
        game_area_height = cell_size * maze.get_height()
        maze_x_offset = int((window_width - game_area_width) * 0.9)
        maze_y_offset = (window_height - game_area_height) // 2
        avatars_x_offset = window_width - maze_x_offset - game_area_width
        avatars_area_width = maze_x_offset - 2 * avatars_x_offset
        avatars_area_height = min(game_area_height // 2, (game_area_height - (len(initial_game_state.teams) - 1) * maze_y_offset) // len(initial_game_state.teams))
        avatars_area_border = 2
        avatars_area_angle = 10
        avatars_area_color = (255, 255, 255)
        teams_enabled = len(initial_game_state.teams) > 1 or len(list(initial_game_state.teams.keys())[0]) > 0
        if teams_enabled:
            avatars_area_padding = avatars_area_height // 13
            team_text_size = avatars_area_padding * 3
            colors = distinctipy.distinctipy.get_colors(len(initial_game_state.teams))
            team_colors = {list(initial_game_state.teams.keys())[i]: tuple([int(c * 255) for c in colors[i]]) for i in range(len(initial_game_state.teams))}
        else:
            avatars_area_padding = avatars_area_height // 12
            team_text_size = 0
            avatars_area_height -= avatars_area_padding * 3
            team_colors = {list(initial_game_state.teams.keys())[i]: avatars_area_color for i in range(len(initial_game_state.teams))}
        player_avatar_size = avatars_area_padding * 3
        player_avatar_horizontal_padding = avatars_area_padding * 4
        player_name_text_size = avatars_area_padding
        cheese_score_size = avatars_area_padding
        text_size = int(cell_size * 0.17)
        cheese_size = int(cell_size * 0.4)
        player_size = int(cell_size * 0.5)
        flag_border_color = (255, 255, 255)
        flag_border_width = 1
        player_border_width = 2
        cheese_border_color = (255, 255, 0)
        cheese_border_width = 1
        cheese_score_border_color = (100, 100, 100)
        cheese_score_border_width = 1
        trace_size = wall_size // 2
        animation_steps = int(max(cell_size / rendering_speed, 1))
        animation_time = 0.01
        medal_size = min(avatars_x_offset, maze_y_offset) * 2
        icon_size = 50
        main_image_factor = 0.8
        main_image_border_color = (0, 0, 0)
        main_image_border_size = 1
        go_image_duration = 0.5
        
        # Function to load an image with some scaling
        # If only 2 arguments are provided, scales keeping ratio specifying the maximum size
        # If first argument is a directory, returns a random image from it
        already_loaded_images = {}
        def ___surface_from_image (file_or_dir_name, target_width_or_max_size, target_height=None):
            full_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), file_or_dir_name)
            if os.path.isdir(full_path):
                full_path = rng.choice(glob.glob(os.path.join(full_path, "*")))
            loaded_image_key = str(full_path) + "_" + str(target_width_or_max_size) + "_" + str(target_height)
            if loaded_image_key in already_loaded_images:
                return already_loaded_images[loaded_image_key]
            surface = pygame.image.load(full_path).convert_alpha()
            if target_height is None:
                max_surface_size = max(surface.get_width(), surface.get_height())
                surface = pygame.transform.scale(surface, (surface.get_width() * target_width_or_max_size // max_surface_size, surface.get_height() * target_width_or_max_size // max_surface_size))
            else:
                surface = pygame.transform.scale(surface, (target_width_or_max_size, target_height))
            already_loaded_images[loaded_image_key] = surface
            return surface
        
        # Same function for text
        def ___surface_from_text (text, target_height, text_color, original_font_size=50):
            surface = pygame.font.SysFont(None, original_font_size).render(text, True, text_color)
            surface = pygame.transform.scale(surface, (surface.get_width() * target_height // surface.get_height(), target_height))
            return surface

        # Function to colorize an object
        def ___colorize (surface, color):
            final_surface = surface.copy()
            color_surface = pygame.Surface(final_surface.get_size()).convert_alpha()
            color_surface.fill(color)
            final_surface.blit(color_surface, (0, 0), special_flags=pygame.BLEND_MULT)
            return final_surface
            
        # Function to add a colored border around an object
        def ___add_color_border (surface, border_color, border_size, final_rescale=True):
            final_surface = pygame.Surface((surface.get_width() + 2 * border_size, surface.get_height() + 2 * border_size)).convert_alpha()
            final_surface.fill((0, 0, 0, 0))
            mask_surface = surface.copy()
            color_surface = pygame.Surface(mask_surface.get_size())
            color_surface.fill((0, 0, 0, 0))
            mask_surface.blit(color_surface, (0, 0), special_flags=pygame.BLEND_MIN)
            color_surface.fill(border_color)
            mask_surface.blit(color_surface, (0, 0), special_flags=pygame.BLEND_MAX)
            for offset_x in range(-border_size, border_size + 1):
                for offset_y in range(-border_size, border_size + 1):
                    if math.dist([0, 0], [offset_x, offset_y]) <= border_size:
                        final_surface.blit(mask_surface, (border_size // 2 + offset_x, border_size // 2 + offset_y))
            final_surface.blit(surface, (border_size // 2, border_size // 2))
            if final_rescale:
                final_surface = pygame.transform.scale(final_surface, surface.get_size())
            return final_surface

        # Function to load the surfaces of a player
        def ___load_player_surfaces (player_skin, scale, border_color=None, border_width=None, add_border=teams_enabled):
            try:
                player_neutral = ___surface_from_image(os.path.join("..", "gui", "players", player_skin.value, "neutral.png"), scale)
                player_north = ___surface_from_image(os.path.join("..", "gui", "players", player_skin.value, "north.png"), scale)
                player_south = ___surface_from_image(os.path.join("..", "gui", "players", player_skin.value, "south.png"), scale)
                player_west = ___surface_from_image(os.path.join("..", "gui", "players", player_skin.value, "west.png"), scale)
                player_east = ___surface_from_image(os.path.join("..", "gui", "players", player_skin.value, "east.png"), scale)
                if add_border:
                    player_neutral = ___add_color_border(player_neutral, border_color, border_width)
                    player_north = ___add_color_border(player_north, border_color, border_width)
                    player_south = ___add_color_border(player_south, border_color, border_width)
                    player_west = ___add_color_border(player_west, border_color, border_width)
                    player_east = ___add_color_border(player_east, border_color, border_width)
                return player_neutral, player_north, player_south, player_west, player_east
            except:
                return ___load_player_surfaces("default", scale, border_color, border_width, add_border)
        
        # Function to play a sound
        def ___play_sound (file_name, alternate_file_name=None):
            sound_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), file_name)
            if not os.path.exists(sound_file):
                sound_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), alternate_file_name)
            sound = pygame.mixer.Sound(sound_file)
            channel = pygame.mixer.find_channel()
            channel.play(sound)
        
        # Function to load the avatar of a player
        def ___load_player_avatar (player_skin, scale):
            try:
                return ___surface_from_image(os.path.join("..", "gui", "players", player_skin.value, "avatar.png"), scale)
            except:
                return ___load_player_avatar("default", scale)
        
        # Function to get the main color of a surface
        def ___get_main_color (surface):
            colors = pygame.surfarray.array2d(surface)
            counts = {color: 0 for color in set(colors.flatten())}
            for color in colors.flatten():
                counts[color] += 1
            max_occurrences = sorted(counts, key=lambda x: counts[x], reverse=True)[:2]
            main_color = surface.unmap_rgb(max_occurrences[0])
            if main_color == (0, 0, 0, 0):
                main_color = surface.unmap_rgb(max_occurrences[1])
            return main_color

        # Set window icon and title
        icon = ___surface_from_image(os.path.join("..", "gui", "icon", "pyrat.png"), icon_size)
        pygame.display.set_icon(icon)
        pygame.display.set_caption("PyRat")
        
        # Set background color
        pygame.draw.rect(gui_screen, background_color, pygame.Rect(0, 0, window_width, window_height))
        
        # Add cells
        for row in range(maze.get_height()):
            for col in range(maze.get_width()):
                if maze.rc_exists(row, col):
                    cell = ___surface_from_image(os.path.join("..", "gui", "ground"), cell_size, cell_size)
                    cell = pygame.transform.rotate(cell, rng.randint(0, 3) * 90)
                    cell = pygame.transform.flip(cell, bool(rng.randint(0, 1)), bool(rng.randint(0, 1)))
                    cell_x = maze_x_offset + col * cell_size
                    cell_y = maze_y_offset + row * cell_size
                    maze_elements.append((cell_x, cell_y, cell))
                    
        # Add mud
        mud = ___surface_from_image(os.path.join("..", "gui", "mud", "mud.png"), cell_size)
        for row in range(maze.get_height()):
            for col in range(maze.get_width()):
                if maze.rc_exists(row, col):
                    if maze.rc_exists(row, col - 1):
                        if maze.has_edge(maze.rc_to_i(row, col), maze.rc_to_i(row, col - 1)):
                            if maze.get_weight(maze.rc_to_i(row, col), maze.rc_to_i(row, col - 1)) > 1:
                                mud_x = maze_x_offset + col * cell_size - mud.get_width() // 2
                                mud_y = maze_y_offset + row * cell_size
                                maze_elements.append((mud_x, mud_y, mud))
                                if not render_simplified:
                                    weight_text = ___surface_from_text(str(maze.get_weight(maze.rc_to_i(row, col), maze.rc_to_i(row, col - 1))), text_size, mud_text_color)
                                    weight_text_x = maze_x_offset + col * cell_size - weight_text.get_width() // 2
                                    weight_text_y = maze_y_offset + row * cell_size + (cell_size - weight_text.get_height()) // 2
                                    maze_elements.append((weight_text_x, weight_text_y, weight_text))
                    if maze.rc_exists(row - 1, col):
                        if maze.has_edge(maze.rc_to_i(row, col), maze.rc_to_i(row - 1, col)):
                            if maze.get_weight(maze.rc_to_i(row, col), maze.rc_to_i(row - 1, col)) > 1:
                                mud_horizontal = pygame.transform.rotate(mud, 90)
                                mud_x = maze_x_offset + col * cell_size
                                mud_y = maze_y_offset + row * cell_size - mud.get_width() // 2
                                maze_elements.append((mud_x, mud_y, mud_horizontal))
                                if not render_simplified:
                                    weight_text = ___surface_from_text(str(maze.get_weight(maze.rc_to_i(row, col), maze.rc_to_i(row - 1, col))), text_size, mud_text_color)
                                    weight_text_x = maze_x_offset + col * cell_size + (cell_size - weight_text.get_width()) // 2
                                    weight_text_y = maze_y_offset + row * cell_size - weight_text.get_height() // 2
                                    maze_elements.append((weight_text_x, weight_text_y, weight_text))

        # Add cell numbers
        if not render_simplified:
            for row in range(maze.get_height()):
                for col in range(maze.get_width()):
                    if maze.rc_exists(row, col):
                        cell_text = ___surface_from_text(str(maze.rc_to_i(row, col)), text_size, cell_text_color)
                        cell_text_x = maze_x_offset + col * cell_size + cell_text_offset
                        cell_text_y = maze_y_offset + row * cell_size + cell_text_offset
                        maze_elements.append((cell_text_x, cell_text_y, cell_text))
        
        # Add walls
        walls = []
        wall = ___surface_from_image(os.path.join("..", "gui", "wall", "wall.png"), cell_size)
        for row in range(maze.get_height() + 1):
            for col in range(maze.get_width() + 1):
                case_outside_to_inside = not maze.rc_exists(row, col) and maze.rc_exists(row, col - 1)
                case_inside_to_outside = maze.rc_exists(row, col) and not maze.rc_exists(row, col - 1)
                case_inside_to_inside = maze.rc_exists(row, col) and maze.rc_exists(row, col - 1) and not maze.has_edge(maze.rc_to_i(row, col), maze.rc_to_i(row, col - 1))
                if case_outside_to_inside or case_inside_to_outside or case_inside_to_inside:
                    wall_x = maze_x_offset + col * cell_size - wall.get_width() // 2
                    wall_y = maze_y_offset + row * cell_size
                    maze_elements.append((wall_x, wall_y, wall))
                    walls.append((row, col, row, col - 1))
                case_outside_to_inside = not maze.rc_exists(row, col) and maze.rc_exists(row - 1, col)
                case_inside_to_outside = maze.rc_exists(row, col) and not maze.rc_exists(row - 1, col)
                case_inside_to_inside = maze.rc_exists(row, col) and maze.rc_exists(row - 1, col) and not maze.has_edge(maze.rc_to_i(row, col), maze.rc_to_i(row - 1, col))
                if case_outside_to_inside or case_inside_to_outside or case_inside_to_inside:
                    wall_horizontal = pygame.transform.rotate(wall, 90)
                    wall_x = maze_x_offset + col * cell_size
                    wall_y = maze_y_offset + row * cell_size - wall.get_width() // 2
                    maze_elements.append((wall_x, wall_y, wall_horizontal))
                    walls.append((row, col, row - 1, col))
            
        # Add corners
        corner = ___surface_from_image(os.path.join("..", "gui", "wall", "corner.png"), int(wall.get_width() * corner_wall_ratio), int(wall.get_width() * corner_wall_ratio))
        for row, col, neighbor_row, neighbor_col in walls:
            if col != neighbor_col:
                corner_x = maze_x_offset + col * cell_size - corner.get_width() // 2
                if (row - 1, col, neighbor_row - 1, neighbor_col) not in walls or ((neighbor_row, neighbor_col, neighbor_row - 1, neighbor_col) in walls and (row, col, row - 1, col) in walls and (row - 1, col, neighbor_row - 1, neighbor_col) in walls):
                    corner_y = maze_y_offset + row * cell_size - corner.get_width() // 2
                    maze_elements.append((corner_x, corner_y, corner))
                if (row + 1, col, neighbor_row + 1, neighbor_col) not in walls:
                    corner_y = maze_y_offset + (row + 1) * cell_size - corner.get_width() // 2
                    maze_elements.append((corner_x, corner_y, corner))
            if row != neighbor_row:
                corner_y = maze_y_offset + row * cell_size - corner.get_width() // 2
                if (row, col - 1, neighbor_row, neighbor_col - 1) not in walls:
                    corner_x = maze_x_offset + col * cell_size - corner.get_width() // 2
                    maze_elements.append((corner_x, corner_y, corner))
                if (row, col + 1, neighbor_row, neighbor_col + 1) not in walls:
                    corner_x = maze_x_offset + (col + 1) * cell_size - corner.get_width() // 2
                    maze_elements.append((corner_x, corner_y, corner))
        
        # Add flags
        if not render_simplified:
            cells_with_flags = {cell: {} for cell in initial_game_state.player_locations.values()}
            for player in players:
                team = [team for team in initial_game_state.teams if player.get_name() in initial_game_state.teams[team]][0]
                if team not in cells_with_flags[initial_game_state.player_locations[player.get_name()]]:
                    cells_with_flags[initial_game_state.player_locations[player.get_name()]][team] = 0
                cells_with_flags[initial_game_state.player_locations[player.get_name()]][team] += 1
            flag = ___surface_from_image(os.path.join("..", "gui", "flag", "flag.png"), flag_size)
            max_teams_in_cells = max([len(team) for team in cells_with_flags.values()])
            max_players_in_cells = max([cells_with_flags[cell][team] for cell in cells_with_flags for team in cells_with_flags[cell]])
            for cell in cells_with_flags:
                row, col = maze.i_to_rc(cell)
                for i_team in range(len(cells_with_flags[cell])):
                    team = list(cells_with_flags[cell].keys())[i_team]
                    flag_colored = ___colorize(flag, team_colors[team])
                    flag_colored = ___add_color_border(flag_colored, flag_border_color, flag_border_width)
                    for i_player in range(cells_with_flags[cell][team]):
                        flag_x = maze_x_offset + (col + 1) * cell_size - flag_x_offset - i_player * min(flag_x_next_offset, (cell_size - flag_x_offset) / (max_players_in_cells + 1))
                        flag_y = maze_y_offset + row * cell_size - flag.get_height() + flag_y_offset + i_team * min(flag_y_offset, (cell_size - flag_y_offset) / (max_teams_in_cells + 1))
                        maze_elements.append((flag_x, flag_y, flag_colored))

        # Add cheese
        cheese = ___surface_from_image(os.path.join("..", "gui", "cheese", "cheese.png"), cheese_size)
        cheese = ___add_color_border(cheese, cheese_border_color, cheese_border_width)
        for c in initial_game_state.cheese:
            row, col = maze.i_to_rc(c)
            cheese_x = maze_x_offset + col * cell_size + (cell_size - cheese.get_width()) // 2
            cheese_y = maze_y_offset + row * cell_size + (cell_size - cheese.get_height()) // 2
            cheese_elements[c] = (cheese_x, cheese_y, cheese)
        
        # Add players
        for player in players:
            team = [team for team in initial_game_state.teams if player.get_name() in initial_game_state.teams[team]][0]
            player_neutral, player_north, player_south, player_west, player_east = ___load_player_surfaces(player.get_skin(), player_size, team_colors[team], player_border_width)
            row, col = maze.i_to_rc(initial_game_state.player_locations[player.get_name()])
            player_x = maze_x_offset + col * cell_size + (cell_size - player_neutral.get_width()) // 2
            player_y = maze_y_offset + row * cell_size + (cell_size - player_neutral.get_height()) // 2
            player_elements[player.get_name()] = (player_x, player_y, player_neutral, player_north, player_south, player_west, player_east)
        
        # Add avatars area
        score_locations = {}
        medal_locations = {}
        for i in range(len(initial_game_state.teams)):
        
            # Box
            team = list(initial_game_state.teams.keys())[i]
            team_background = pygame.Surface((avatars_area_width, avatars_area_height))
            pygame.draw.rect(team_background, background_color, pygame.Rect(0, 0, avatars_area_width, avatars_area_height))
            pygame.draw.rect(team_background, team_colors[team], pygame.Rect(0, 0, avatars_area_width, avatars_area_height), avatars_area_border, avatars_area_angle)
            team_background_x = avatars_x_offset
            team_background_y = (1 + i) * maze_y_offset + i * avatars_area_height if len(initial_game_state.teams) > 1 else (window_height - avatars_area_height) // 2
            avatar_elements.append((team_background_x, team_background_y, team_background))
            medal_locations[team] = (team_background_x + avatars_area_width, team_background_y)
            
            # Team name
            team_text = ___surface_from_text(team, team_text_size, team_colors[team])
            if team_text.get_width() > avatars_area_width - 2 * avatars_area_padding:
                ratio = (avatars_area_width - 2 * avatars_area_padding) / team_text.get_width()
                team_text = pygame.transform.scale(team_text, (int(team_text.get_width() * ratio), int(team_text.get_height() * ratio)))
            team_text_x = avatars_x_offset + (avatars_area_width - team_text.get_width()) // 2
            team_text_y = team_background_y + avatars_area_padding + (team_text_size - team_text.get_height()) // 2
            if not teams_enabled:
                team_text_size = -avatars_area_padding
            avatar_elements.append((team_text_x, team_text_y, team_text))
            
            # Players avatars
            player_images = []
            for j in range(len(initial_game_state.teams[team])):
                player = [player for player in players if player.get_name() == initial_game_state.teams[team][j]][0]
                player_avatar = ___load_player_avatar(player.get_skin(), player_avatar_size)
                player_images.append(player_avatar)
            avatar_area = pygame.Surface((2 * avatars_area_padding + sum([player_image.get_width() for player_image in player_images]) + player_avatar_horizontal_padding * (len(initial_game_state.teams[team]) - 1), player_avatar_size))
            pygame.draw.rect(avatar_area, background_color, pygame.Rect(0, 0, avatar_area.get_width(), avatar_area.get_height()))
            player_x = avatars_area_padding
            centers = []
            for player_avatar in player_images:
                avatar_area.blit(player_avatar, (player_x, 0))
                centers.append(player_x + player_avatar.get_width() // 2)
                player_x += player_avatar.get_width() + player_avatar_horizontal_padding
            if avatar_area.get_width() > avatars_area_width - 2 * avatars_area_padding:
                ratio = (avatars_area_width - 2 * avatars_area_padding) / avatar_area.get_width()
                centers = [center * ratio for center in centers]
                avatar_area = pygame.transform.scale(avatar_area, (int(avatar_area.get_width() * ratio), int(avatar_area.get_height() * ratio)))
            avatar_area_x = avatars_x_offset + (avatars_area_width - avatar_area.get_width()) // 2
            avatar_area_y = team_background_y + 2 * avatars_area_padding + team_text_size + (player_avatar_size - avatar_area.get_height()) // 2
            avatar_elements.append((avatar_area_x, avatar_area_y, avatar_area))

            # Players names
            for j in range(len(initial_game_state.teams[team])):
                player_name = initial_game_state.teams[team][j]
                while True:
                    player_name_text = ___surface_from_text(player_name, player_name_text_size, avatars_area_color)
                    if player_name_text.get_width() > (avatars_area_width - 2 * avatars_area_padding) / len(initial_game_state.teams[team]):
                        player_name = player_name[:-2] + "."
                    else:
                        break
                player_name_text_x = avatar_area_x + centers[j] - player_name_text.get_width() // 2
                player_name_text_y = team_background_y + 3 * avatars_area_padding + team_text_size + player_avatar_size + (player_name_text_size - player_name_text.get_height()) // 2
                avatar_elements.append((player_name_text_x, player_name_text_y, player_name_text))
        
            # Score locations
            cheese_missing = ___surface_from_image(os.path.join("..", "gui", "cheese", "cheese_missing.png"), cheese_score_size)
            score_x_offset = avatars_x_offset + avatars_area_padding
            score_margin = avatars_area_width - 2 * avatars_area_padding - cheese_missing.get_width()
            if len(initial_game_state.cheese) > 1:
                score_margin /= (len(initial_game_state.cheese) - 1)
            score_margin = min(score_margin, cheese_missing.get_width() * 2)
            estimated_width = cheese_missing.get_width() + (len(initial_game_state.cheese) - 1) * score_margin
            if estimated_width < avatars_area_width - 2 * avatars_area_padding:
                score_x_offset += (avatars_area_width - 2 * avatars_area_padding - estimated_width) / 2
            score_y_offset = team_background_y + 4 * avatars_area_padding + team_text_size + player_avatar_size + player_name_text_size
            score_locations[team] = (score_x_offset, score_margin, score_y_offset)

        # Show maze
        def ___show_maze ():
            pygame.draw.rect(gui_screen, background_color, pygame.Rect(maze_x_offset, maze_y_offset, game_area_width, game_area_height))
            for surface_x, surface_y, surface in maze_elements:
                gui_screen.blit(surface, (surface_x, surface_y))
        ___show_maze()
        
        # Show cheese
        def ___show_cheese (cheese):
            for c in cheese:
                cheese_x, cheese_y, surface = cheese_elements[c]
                gui_screen.blit(surface, (cheese_x, cheese_y))
        ___show_cheese(initial_game_state.cheese)
        
        # Show_players at initial locations
        def ___show_initial_players ():
            for p in player_elements:
                player_x, player_y, player_neutral, _, _ , _, _ = player_elements[p]
                gui_screen.blit(player_neutral, (player_x, player_y))
        ___show_initial_players()
        
        # Show avatars
        def ___show_avatars ():
            for surface_x, surface_y, surface in avatar_elements:
                gui_screen.blit(surface, (surface_x, surface_y))
        ___show_avatars()
        
        # Show scores
        def ___show_scores (team_scores):
            cheese_missing = ___surface_from_image(os.path.join("..", "gui", "cheese", "cheese_missing.png"), cheese_score_size)
            cheese_missing = ___add_color_border(cheese_missing, cheese_score_border_color, cheese_score_border_width)
            cheese_eaten = ___surface_from_image(os.path.join("..", "gui", "cheese", "cheese_eaten.png"), cheese_score_size)
            cheese_eaten = ___add_color_border(cheese_eaten, cheese_score_border_color, cheese_score_border_width)
            for team in score_locations:
                score_x_offset, score_margin, score_y_offset = score_locations[team]
                for i in range(int(team_scores[team])):
                    gui_screen.blit(cheese_eaten, (score_x_offset + i * score_margin, score_y_offset))
                if int(team_scores[team]) != team_scores[team]:
                    cheese_partial = ___surface_from_image(os.path.join("..", "gui", "cheese", "cheese_eaten.png"), cheese_score_size)
                    cheese_partial = ___colorize(cheese_partial, [(team_scores[team] - int(team_scores[team])) * 255] * 3)
                    cheese_partial = ___add_color_border(cheese_partial, cheese_score_border_color, cheese_score_border_width)
                    gui_screen.blit(cheese_partial, (score_x_offset + int(team_scores[team]) * score_margin, score_y_offset))
                for j in range(math.ceil(team_scores[team]), len(initial_game_state.cheese)):
                    gui_screen.blit(cheese_missing, (score_x_offset + j * score_margin, score_y_offset))
        initial_scores = {team: 0 for team in initial_game_state.teams}
        ___show_scores(initial_scores)
        
        # Show preprocessing message
        preprocessing_image = ___surface_from_image(os.path.join("..", "gui", "drawings", "pyrat_preprocessing.png"), int(min(game_area_width, game_area_height) * main_image_factor))
        preprocessing_image = ___add_color_border(preprocessing_image, main_image_border_color, main_image_border_size)
        go_image = ___surface_from_image(os.path.join("..", "gui", "drawings", "pyrat_go.png"), int(min(game_area_width, game_area_height) * main_image_factor))
        go_image = ___add_color_border(go_image, main_image_border_color, main_image_border_size)
        main_image_x = maze_x_offset + (game_area_width - preprocessing_image.get_width()) / 2
        main_image_y = maze_y_offset + (game_area_height - preprocessing_image.get_height()) / 2
        gui_screen.blit(preprocessing_image, (main_image_x, main_image_y))
        
        # Prepare useful variables
        current_state = copy.deepcopy(initial_game_state)
        mud_being_crossed = {player.get_name(): 0 for player in players}
        traces = {player.get_name(): [(player_elements[player.get_name()][0] + player_elements[player.get_name()][2].get_width() / 2, player_elements[player.get_name()][1] + player_elements[player.get_name()][2].get_height() / 2)] for player in players}
        trace_colors = {player.get_name(): ___get_main_color(player_elements[player.get_name()][2]) for player in players}
        player_surfaces = {player.get_name(): player_elements[player.get_name()][2] for player in players}

        # Show and indicate when ready
        gui_running = True
        pygame.display.flip()
        time.sleep(0.1)
        pygame.display.update()
        gui_initialized_synchronizer.wait()
        
        # Run until the user asks to quit
        while gui_running:
            try:

                # We check for termination
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pglocals.KEYDOWN and event.key == pglocals.K_ESCAPE):
                        gui_running = False
                if not gui_running:
                    break
                
                # Get turn info
                new_state = gui_queue.get(False)
                
                # Indicate when preprocessing is over for a little time
                if new_state.turn == 1:
                    ___show_maze()
                    ___show_cheese(current_state.cheese if i != animation_steps - 1 else new_state.cheese)
                    ___show_initial_players()
                    gui_screen.blit(go_image, (main_image_x, main_image_y))
                    pygame.display.update((maze_x_offset, maze_y_offset, maze.get_width() * cell_size, maze.get_height() * cell_size))
                    time.sleep(go_image_duration)

                # Enter mud?
                for player in players:
                    if new_state.muds[player.get_name()]["count"] > 0 and mud_being_crossed[player.get_name()] == 0:
                        mud_being_crossed[player.get_name()] = new_state.muds[player.get_name()]["count"] + 1

                # Choose the correct player surface
                for player in players:
                    player_x, player_y, player_neutral, player_north, player_south, player_west, player_east = player_elements[player.get_name()]
                    row, col = maze.i_to_rc(current_state.player_locations[player.get_name()])
                    adjusted_new_location = new_state.player_locations[player.get_name()] if not new_state.is_in_mud(player.get_name()) else new_state.muds[player.get_name()]["target"]
                    new_row, new_col = maze.i_to_rc(adjusted_new_location)
                    player_x += player_surfaces[player.get_name()].get_width() / 2
                    player_y += player_surfaces[player.get_name()].get_height() / 2
                    if new_col > col:
                        player_surfaces[player.get_name()] = player_east
                    elif new_col < col:
                        player_surfaces[player.get_name()] = player_west
                    elif new_row > row:
                        player_surfaces[player.get_name()] = player_south
                    elif new_row < row:
                        player_surfaces[player.get_name()] = player_north
                    else:
                        player_surfaces[player.get_name()] = player_neutral
                    player_x -= player_surfaces[player.get_name()].get_width() / 2
                    player_y -= player_surfaces[player.get_name()].get_height() / 2
                    player_elements[player.get_name()] = (player_x, player_y, player_neutral, player_north, player_south, player_west, player_east)

                # Move players
                for i in range(animation_steps):
                
                    # Reset background & cheese
                    ___show_maze()
                    ___show_cheese(current_state.cheese if i != animation_steps - 1 else new_state.cheese)
                    
                    # Move player with trace
                    for player in players:
                        player_x, player_y, player_neutral, player_north, player_south, player_west, player_east = player_elements[player.get_name()]
                        row, col = maze.i_to_rc(current_state.player_locations[player.get_name()])
                        adjusted_new_location = new_state.player_locations[player.get_name()] if not new_state.is_in_mud(player.get_name()) else new_state.muds[player.get_name()]["target"]
                        new_row, new_col = maze.i_to_rc(adjusted_new_location)
                        shift = (i + 1) * cell_size / animation_steps
                        if mud_being_crossed[player.get_name()] > 0:
                            shift /= mud_being_crossed[player.get_name()]
                            shift += (mud_being_crossed[player.get_name()] - new_state.muds[player.get_name()]["count"] - 1) * cell_size / mud_being_crossed[player.get_name()]
                        next_x = player_x if col == new_col else player_x + shift if new_col > col else player_x - shift
                        next_y = player_y if row == new_row else player_y + shift if new_row > row else player_y - shift
                        if i == animation_steps - 1 and new_state.muds[player.get_name()]["count"] == 0:
                            player_elements[player.get_name()] = (next_x, next_y, player_neutral, player_north, player_south, player_west, player_east)
                        if trace_length > 0:
                            pygame.draw.line(gui_screen, trace_colors[player.get_name()], (next_x + player_surfaces[player.get_name()].get_width() / 2, next_y + player_surfaces[player.get_name()].get_height() / 2), traces[player.get_name()][-1], width=trace_size)
                            for j in range(1, trace_length):
                                if len(traces[player.get_name()]) > j:
                                    pygame.draw.line(gui_screen, trace_colors[player.get_name()], traces[player.get_name()][-j-1], traces[player.get_name()][-j], width=trace_size)
                            if len(traces[player.get_name()]) == trace_length + 1:
                                final_segment_length = math.sqrt((traces[player.get_name()][-1][0] - (next_x + player_surfaces[player.get_name()].get_width() / 2))**2 + (traces[player.get_name()][-1][1] - (next_y + player_surfaces[player.get_name()].get_height() / 2))**2)
                                ratio = 1 - final_segment_length / cell_size
                                pygame.draw.line(gui_screen, trace_colors[player.get_name()], traces[player.get_name()][1], (traces[player.get_name()][1][0] + ratio * (traces[player.get_name()][0][0] - traces[player.get_name()][1][0]), traces[player.get_name()][1][1] + ratio * (traces[player.get_name()][0][1] - traces[player.get_name()][1][1])), width=trace_size)
                        gui_screen.blit(player_surfaces[player.get_name()], (next_x, next_y))
                    
                    # Update maze & wait for animation
                    pygame.display.update((maze_x_offset, maze_y_offset, maze.get_width() * cell_size, maze.get_height() * cell_size))
                    time.sleep(animation_time / animation_steps)

                # Exit mud?
                for player in players:
                    if new_state.muds[player.get_name()]["count"] == 0:
                        mud_being_crossed[player.get_name()] = 0
                    if mud_being_crossed[player.get_name()] == 0:
                        player_x, player_y, _, _, _, _, _ = player_elements[player.get_name()]
                        if traces[player.get_name()][-1] != (player_x + player_surfaces[player.get_name()].get_width() / 2, player_y + player_surfaces[player.get_name()].get_height() / 2):
                            traces[player.get_name()].append((player_x + player_surfaces[player.get_name()].get_width() / 2, player_y + player_surfaces[player.get_name()].get_height() / 2))
                        traces[player.get_name()] = traces[player.get_name()][-trace_length-1:]
                
                # Play a sound is a cheese is eaten
                for player in players:
                    if new_state.player_locations[player.get_name()] in current_state.cheese and mud_being_crossed[player.get_name()] == 0:
                        ___play_sound(os.path.join("..", "gui", "players", player.get_skin().value, "cheese_eaten.wav"), os.path.join("..", "gui", "players", "default", "cheese_eaten.wav"))
                
                # Update score
                ___show_avatars()
                new_scores = new_state.get_score_per_team()
                ___show_scores(new_scores)
                current_state = new_state
                
                # Indicate if the game is over
                if new_state.game_over():
                    sorted_results = sorted([(new_scores[team], team) for team in new_scores], reverse=True)
                    medals = [___surface_from_image(os.path.join("..", "gui", "endgame", medal_name), medal_size) for medal_name in ["first.png", "second.png", "third.png", "others.png"]]
                    for i in range(len(sorted_results)):
                        if i > 0 and sorted_results[i][0] != sorted_results[i-1][0] and len(medals) > 1:
                            del medals[0]
                        team = sorted_results[i][1]
                        gui_screen.blit(medals[0], (medal_locations[team][0] - medals[0].get_width() / 2, medal_locations[team][1] - medals[0].get_height() / 3))
                    ___play_sound(os.path.join("..", "gui", "endgame", "game_over.wav"))
                pygame.display.update((0, 0, maze_x_offset, window_height))
                
            # Ignore exceptions raised due to emtpy queue
            except queue.Empty:
                pass
            
        # Quit PyGame
        pygame.display.quit()
        pygame.quit()
        
    # Ignore
    except:
        pass

#####################################################################################################################################################
#####################################################################################################################################################
