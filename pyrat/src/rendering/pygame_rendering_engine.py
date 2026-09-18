##########################################################################################
########################################## INFO ##########################################
##########################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# Please import necessary elements using the following syntax:
#     from pyrat import <element_name>

"""
This module provides a rendering engine using the ``pygame`` library.
It creates a window and displays the game in it.
The window itself is built and run by the ``gui`` package, in a separate process, so that drawing never slows the game down.
"""

##########################################################################################
######################################### IMPORTS ########################################
##########################################################################################

# External imports
import multiprocessing
import threading

# PyRat imports
from pyrat.src.rendering.rendering_engine import RenderingEngine
from pyrat.src.rendering.gui.process import run_gui_process
from pyrat.src.players.player import Player
from pyrat.src.mazes.maze import Maze
from pyrat.src.game.game_state import GameState
from pyrat.src.game.exceptions import PyRatException

##########################################################################################
######################################### CLASSES ########################################
##########################################################################################

class PygameRenderingEngine (RenderingEngine):

    """
    *(This class inherits from* ``RenderingEngine`` *).*

    This rendering engine uses the ``pygame`` library to render the game.
    It creates a window and displays the game in it.

    The window runs in a different process than the one running the game, and receives the successive states of the game through a queue.
    It shows the moves at its own pace, set by the ``rendering_speed`` argument, and not at the pace of the game.
    The window may therefore lag behind the game, and catches up once the game is over.
    """

    ##################################################################################
    #                                   CONSTRUCTOR                                  #
    ##################################################################################

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
        self.__manager = None

    ##################################################################################
    #                                 PUBLIC METHODS                                 #
    ##################################################################################

    def end (self) -> None:

        """
        *(This method redefines the method of the parent class with the same name).*

        It waits for the window to be closed before exiting.
        """

        # Wait for GUI to be exited to quit if there is one
        if self.__gui_process is not None:
            self.__gui_process.join()

    ##################################################################################

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

        Raises:
            PyRatException: If the window could not be opened.
        """

        # Debug
        assert isinstance(players, list), "Argument 'players' must be a list"
        assert all(isinstance(player, Player) for player in players), "All elements of 'players' must be of type 'pyrat.Player'"
        assert isinstance(maze, Maze), "Argument 'maze' must be of type 'pyrat.Maze'"
        assert isinstance(game_state, GameState), "Argument 'game_state' must be of type 'pyrat.GameState'"

        # Initialize the GUI in a different process at turn 0, and wait for the window to be ready
        # If the window cannot be opened, the process breaks the barrier instead of letting us wait forever
        if game_state.turn == 0:
            self.__manager = multiprocessing.Manager()
            gui_initialized_synchronizer = self.__manager.Barrier(2)
            self.__gui_queue = self.__manager.Queue()
            self.__gui_process = multiprocessing.Process(target=run_gui_process, args=(gui_initialized_synchronizer, self.__gui_queue, maze, game_state, players, self.__fullscreen, self._render_simplified, self.__trace_length, self._rendering_speed))
            self.__gui_process.start()
            try:
                gui_initialized_synchronizer.wait()
            except threading.BrokenBarrierError:
                raise PyRatException("The graphical interface could not be started, see the error above")

        # At each turn, send current info to the process
        else:
            self.__gui_queue.put(game_state)

##########################################################################################
##########################################################################################
