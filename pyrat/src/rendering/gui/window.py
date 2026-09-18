##########################################################################################
########################################## INFO ##########################################
##########################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# It is internal to the library, and nothing in it is meant to be imported by PyRat programs.

"""
This module runs the window of the graphical interface.

The window lives in its own process, and receives the successive states of the game through a queue.
It shows the moves at its own pace: a move always takes the same time, whatever the pace of the game and the machine.
The game may therefore be ahead of what the window shows, in which case the window catches up once the game is over.
This is intentional: the game is never slowed down by the drawing, and the moves are always readable.

The window also reacts to what the user does with it: closing it or pressing escape ends it, and resizing it rebuilds the interface at the new size.
"""

##########################################################################################
######################################### IMPORTS ########################################
##########################################################################################

# External imports
import multiprocessing.managers as mpmanagers
import os
import queue
import random
import time
import pygame

# PyRat imports
from pyrat.src.rendering.gui import layout as layout_module
from pyrat.src.rendering.gui.animation import animation_frames
from pyrat.src.rendering.gui.assets import Assets
from pyrat.src.rendering.gui.layout import Layout
from pyrat.src.rendering.gui.scene import MazeDecor, Scene, choose_team_colors
from pyrat.src.mazes.maze import Maze
from pyrat.src.game.game_state import GameState
from pyrat.src.game.enums import Action
from pyrat.src.players.player import Player

##########################################################################################
######################################## CONSTANTS #######################################
##########################################################################################

# Duration of the animation of a move, in seconds, at the default rendering speed
MOVE_DURATION = 0.3

# Maximum number of images drawn per second
ANIMATION_FPS = 60

# Duration for which the image announcing the beginning of the game is shown, in seconds
GO_IMAGE_DURATION = 0.5

# Time the window waits for a new state of the game before checking the events again, in seconds
EVENT_POLL_INTERVAL = 0.02

# Time without a resize event after which the interface is rebuilt at the new size, in seconds
RESIZE_SETTLE_DELAY = 0.2

# Proportion of the screen occupied by the window when it is not fullscreen
WINDOW_SCREEN_RATIO = 0.8

# Displacement corresponding to each action, as a fraction of a cell
MOVE_VECTORS = {Action.NOTHING: (0.0, 0.0),
                Action.NORTH: (0.0, -1.0),
                Action.SOUTH: (0.0, 1.0),
                Action.WEST: (-1.0, 0.0),
                Action.EAST: (1.0, 0.0)}

##########################################################################################
######################################### CLASSES ########################################
##########################################################################################

class GameWindow ():

    """
    The window in which a game is shown.

    Creating an instance opens the window and shows the initial state of the game.
    The ``run()`` method then shows the states of the game as they arrive, until the user closes the window.
    """

    ##################################################################################
    #                                   CONSTRUCTOR                                  #
    ##################################################################################

    def __init__ ( self,
                   maze:               Maze,
                   initial_game_state: GameState,
                   players:            list[Player],
                   fullscreen:         bool,
                   render_simplified:  bool,
                   trace_length:       int,
                   rendering_speed:    float
                 ) ->                  None:

        """
        Initializes a new instance of the class, which opens the window and shows the initial state of the game.

        Args:
            maze:               Maze of the game.
            initial_game_state: State of the game before it starts.
            players:            Players of the game.
            fullscreen:         Indicates if the window should be fullscreen.
            render_simplified:  If ``True``, the details of the maze are not drawn.
            trace_length:       Number of cells of trace to show behind a player.
            rendering_speed:    Speed at which the moves are shown, relative to the default one.
        """

        # Debug
        assert isinstance(maze, Maze), "Argument 'maze' must be of type 'pyrat.Maze'"
        assert isinstance(initial_game_state, GameState), "Argument 'initial_game_state' must be of type 'pyrat.GameState'"
        assert isinstance(players, list), "Argument 'players' must be a list"
        assert all(isinstance(player, Player) for player in players), "All elements of 'players' must be of type 'pyrat.Player'"
        assert isinstance(fullscreen, bool), "Argument 'fullscreen' must be a boolean"
        assert isinstance(render_simplified, bool), "Argument 'render_simplified' must be a boolean"
        assert isinstance(trace_length, int), "Argument 'trace_length' must be an integer"
        assert trace_length >= 0, "Argument 'trace_length' must be non-negative"
        assert isinstance(rendering_speed, float), "Argument 'rendering_speed' must be a real number"
        assert rendering_speed > 0.0, "Argument 'rendering_speed' must be positive"

        # Private attributes, describing the game
        self.__maze = maze
        self.__initial_game_state = initial_game_state
        self.__players = players
        self.__skins = {player.get_name(): player.get_skin() for player in players}
        self.__fullscreen = fullscreen
        self.__render_simplified = render_simplified
        self.__trace_length = trace_length
        self.__move_duration = MOVE_DURATION / rendering_speed

        # Start pygame and open the window
        pygame.init()
        self.__screen = self.__open_window()

        # Elements that are decided once, and kept when the window is resized
        rng = random.Random()
        self.__assets = Assets(rng)
        self.__decor = MazeDecor(maze, self.__assets, rng)
        self.__team_colors = choose_team_colors(initial_game_state)
        pygame.display.set_icon(self.__assets.image(os.path.join("icon", "pyrat.png"), layout_module.ICON_SIZE))
        pygame.display.set_caption("PyRat")

        # Interface at the current size of the window
        self.__layout = None
        self.__scene = None
        self.__build_interface(self.__screen.get_size())

        # State of the game, as the window currently shows it
        # A player is drawn from an anchor cell, shifted by a fraction of the current move
        names = [player.get_name() for player in players]
        self.__current_state = initial_game_state
        self.__anchor_cells = dict(initial_game_state.player_locations)
        self.__orientations = {name: Action.NOTHING for name in names}
        self.__moves = {name: MOVE_VECTORS[Action.NOTHING] for name in names}
        self.__progress = {name: 0.0 for name in names}
        self.__mud_turns = {name: 0 for name in names}
        self.__traces = {name: [initial_game_state.player_locations[name]] for name in names}
        self.__game_is_over = False

        # Interaction with the user
        self.__running = True
        self.__pending_resize = None
        self.__last_resize_time = 0.0

        # Show the initial state, with the image announcing the preprocessing
        # Some systems only compose the window once its events have been handled a first time, so we show it twice
        self.__redraw_everything("pyrat_preprocessing.png")
        pygame.event.pump()
        time.sleep(0.1)
        pygame.display.flip()

    ##################################################################################
    #                                 PUBLIC METHODS                                 #
    ##################################################################################

    def run ( self,
              gui_queue: mpmanagers.BaseProxy
            ) ->         None:

        """
        Shows the states of the game as they arrive, until the user closes the window.
        The window is closed when this method returns.

        Args:
            gui_queue: Queue through which the states of the game are received.
        """

        # Alternate between reacting to the user and showing the turns of the game
        # If the process of the game disappears, the queue becomes unusable, and the window simply closes
        try:
            while self.__running:
                self.__handle_events()
                self.__finish_resize()
                try:
                    new_state = gui_queue.get(timeout=EVENT_POLL_INTERVAL)
                except queue.Empty:
                    continue
                except (EOFError, ConnectionError):
                    break
                self.__show_turn(new_state)

        # Quit pygame, even if something went wrong
        finally:
            pygame.quit()

    ##################################################################################
    #                                 PRIVATE METHODS                                #
    ##################################################################################

    def __open_window ( self ) -> pygame.Surface:

        """
        Opens the window, which the user can resize unless it is fullscreen.

        Returns:
            The surface of the window.
        """

        # Fullscreen, or a large part of the screen
        if self.__fullscreen:
            screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
            pygame.display.toggle_fullscreen()
        else:
            screen_info = pygame.display.Info()
            window_size = (int(screen_info.current_w * WINDOW_SCREEN_RATIO), int(screen_info.current_h * WINDOW_SCREEN_RATIO))
            screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
        return screen

    ##################################################################################

    def __build_interface ( self,
                            window_size: tuple[int, int]
                          ) ->           None:

        """
        Builds the interface for a window size.
        What was decided once for the game (decor, colors) is kept, only the sizes change.

        Args:
            window_size: Size of the window, as a width and a height in pixels.
        """

        # The colors of the traces are kept from one size to another, as they are computed from the images
        trace_colors = self.__scene.player_trace_colors if self.__scene is not None else None
        self.__layout = Layout(window_size, self.__maze, self.__initial_game_state)
        self.__scene = Scene(self.__assets, self.__layout, self.__maze, self.__initial_game_state, self.__players, self.__team_colors, self.__decor, self.__render_simplified, trace_colors)

    ##################################################################################

    def __handle_events ( self ) -> None:

        """
        Reacts to what the user did with the window since the last call.
        Closing the window or pressing escape ends the window, and resizing it stretches the current image until the interface is rebuilt.
        """

        # Process all pending events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.__running = False
            elif event.type == pygame.VIDEORESIZE and not self.__fullscreen:
                self.__stretch_to(event.w, event.h)

    ##################################################################################

    def __stretch_to ( self,
                       width:  int,
                       height: int
                     ) ->      None:

        """
        Stretches the current image to a new size of the window.
        Rebuilding the interface takes time, so while the user drags the border of the window we only stretch the image we already have.
        The interface is rebuilt once the dragging stops.

        Args:
            width:  New width of the window.
            height: New height of the window.
        """

        # Remember that the interface must be rebuilt, and show a stretched image in the meantime
        self.__pending_resize = (width, height)
        self.__last_resize_time = time.perf_counter()
        stretched = pygame.transform.smoothscale(self.__screen.copy(), (width, height))
        self.__screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.__screen.blit(stretched, (0, 0))
        pygame.display.flip()

    ##################################################################################

    def __finish_resize ( self ) -> None:

        """
        Rebuilds the interface at the new size of the window, once the user has stopped resizing it for a moment.
        """

        # Nothing to do if there is no resize, or if the user is still dragging
        if self.__pending_resize is None or time.perf_counter() - self.__last_resize_time <= RESIZE_SETTLE_DELAY:
            return

        # Rebuild everything at the new size, so that the image is sharp again
        self.__build_interface(self.__pending_resize)
        self.__pending_resize = None
        self.__redraw_everything()

    ##################################################################################

    def __show_turn ( self,
                      new_state: GameState
                    ) ->         None:

        """
        Shows a turn of the game, by animating the moves of the players from what the window currently shows to the new state.
        The user can still interact with the window during the animation.

        Args:
            new_state: State of the game at the end of the turn.
        """

        # Indicate for a little time that the preprocessing is over
        if new_state.turn == 1:
            self.__draw_frame(self.__current_state.cheese)
            self.__scene.draw_main_image(self.__screen, "pyrat_go.png")
            self.__present()
            time.sleep(GO_IMAGE_DURATION)

        # Decide where each player goes, then animate the move
        self.__start_move(new_state)
        for progress, is_last_frame in animation_frames(self.__move_duration, ANIMATION_FPS):
            self.__handle_events()
            if not self.__running:
                return
            self.__finish_resize()
            for name in self.__progress:
                self.__progress[name] = self.__move_progress(name, progress, new_state)
            self.__draw_frame(new_state.cheese if is_last_frame else self.__current_state.cheese)
            self.__present()

        # The players have arrived
        self.__end_move(new_state)

    ##################################################################################

    def __start_move ( self,
                       new_state: GameState
                     ) ->         None:

        """
        Decides in which direction each player moves during a turn, and which of its images to show.

        Args:
            new_state: State of the game at the end of the turn.
        """

        # A player in mud heads towards the cell it is crossing to, and stays in the same direction for several turns
        for name in self.__anchor_cells:
            target_cell = new_state.muds[name]["target"] if new_state.is_in_mud(name) else new_state.player_locations[name]
            action = self.__maze.locations_to_action(self.__anchor_cells[name], target_cell)
            if action is None:
                self.__anchor_cells[name] = target_cell
                action = Action.NOTHING
            self.__orientations[name] = action
            self.__moves[name] = MOVE_VECTORS[action]
            self.__progress[name] = 0.0
            if new_state.muds[name]["count"] > 0 and self.__mud_turns[name] == 0:
                self.__mud_turns[name] = new_state.muds[name]["count"] + 1

    ##################################################################################

    def __move_progress ( self,
                          name:      str,
                          progress:  float,
                          new_state: GameState
                        ) ->         float:

        """
        Returns how far a player is in its current move, for a given progress of the animation of the turn.
        A player crossing mud advances only by a fraction of a cell per turn, so that it takes the whole crossing to reach the next cell.

        Args:
            name:      Name of the player.
            progress:  Progress of the animation of the turn, between 0 and 1.
            new_state: State of the game at the end of the turn.

        Returns:
            The fraction of the move already done, between 0 and 1.
        """

        # Turns already spent in the mud count as progress
        if self.__mud_turns[name] == 0:
            return progress
        return (progress + self.__mud_turns[name] - new_state.muds[name]["count"] - 1) / self.__mud_turns[name]

    ##################################################################################

    def __end_move ( self,
                     new_state: GameState
                   ) ->         None:

        """
        Updates what the window shows once the moves of a turn are animated.
        The players that have arrived are anchored to their new cell, their traces grow, and the sounds and scores are updated.

        Args:
            new_state: State of the game at the end of the turn.
        """

        # Players that have arrived, unless they are still crossing mud
        for name in self.__anchor_cells:
            if new_state.muds[name]["count"] == 0:
                self.__mud_turns[name] = 0
                self.__anchor_cells[name] = new_state.player_locations[name]
                self.__moves[name] = MOVE_VECTORS[Action.NOTHING]
                self.__progress[name] = 0.0
                if self.__traces[name][-1] != self.__anchor_cells[name]:
                    self.__traces[name].append(self.__anchor_cells[name])
                self.__traces[name] = self.__traces[name][-self.__trace_length - 1:]

            # A sound is played when a player reaches a piece of cheese
            if new_state.player_locations[name] in self.__current_state.cheese and self.__mud_turns[name] == 0:
                self.__assets.play_sound(os.path.join("players", self.__skins[name].value, "cheese_eaten.wav"))

        # The new state is now what the window shows
        self.__current_state = new_state
        if new_state.game_over():
            self.__game_is_over = True
            self.__assets.play_sound(os.path.join("endgame", "game_over.wav"))
        self.__draw_scores()
        self.__present()

    ##################################################################################

    def __draw_frame ( self,
                       cheese: list[int]
                     ) ->      None:

        """
        Draws the maze, with the players where their current moves and progresses put them.
        Nothing is drawn while the user is resizing the window, as the stretched image is kept until the interface is rebuilt.

        Args:
            cheese: Cells that still contain a piece of cheese.
        """

        # Position of each player, shifted from its anchor cell by the progress of its move
        if self.__pending_resize is not None:
            return
        positions = {}
        for name, anchor_cell in self.__anchor_cells.items():
            shift = (self.__moves[name][0] * self.__progress[name], self.__moves[name][1] * self.__progress[name])
            positions[name] = self.__scene.player_position(name, self.__orientations[name], anchor_cell, shift)
        self.__scene.draw_maze(self.__screen, cheese, positions, self.__orientations, self.__traces, self.__trace_length)

    ##################################################################################

    def __draw_scores ( self ) -> None:

        """
        Draws the scores area, and the medals if the game is over.
        Nothing is drawn while the user is resizing the window.
        """

        # Scores of the state currently shown
        if self.__pending_resize is not None:
            return
        team_scores = self.__current_state.get_score_per_team()
        self.__scene.draw_scores(self.__screen, team_scores)
        if self.__game_is_over:
            self.__scene.draw_medals(self.__screen, team_scores)

    ##################################################################################

    def __redraw_everything ( self,
                              main_image_name: str | None = None
                            ) ->               None:

        """
        Draws the whole window from what it currently shows, and presents it.

        Args:
            main_image_name: Name of an image to draw over the maze, or ``None`` for no image.
        """

        # Background, maze, scores, and optionally the main image
        self.__scene.draw_background(self.__screen)
        self.__draw_frame(self.__current_state.cheese)
        self.__draw_scores()
        if main_image_name is not None:
            self.__scene.draw_main_image(self.__screen, main_image_name)
        self.__present()

    ##################################################################################

    def __present ( self ) -> None:

        """
        Shows what was drawn on the screen.
        Nothing is shown while the user is resizing the window, as the stretched image is kept until the interface is rebuilt.
        """

        # Present the screen
        if self.__pending_resize is None:
            pygame.display.flip()

##########################################################################################
##########################################################################################
