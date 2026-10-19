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
import ast
import inspect
import multiprocessing
import threading
import tokenize

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

        # Check validity
        if not isinstance(fullscreen, bool):
            raise PyRatException(f"Argument 'fullscreen' must be a boolean, got {fullscreen!r} of type {type(fullscreen).__name__}")
        if not isinstance(trace_length, int):
            raise PyRatException(f"Argument 'trace_length' must be an integer, got {trace_length!r} of type {type(trace_length).__name__}")
        if not (trace_length >= 0):
            raise PyRatException(f"Argument 'trace_length' must be non-negative, got {trace_length!r}")

        # The window is opened in another process, which needs the game to be created from a block 'if __name__ == "__main__":'
        _check_main_guard()

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
            PyRatException: If no player is given, if a player is not in the game state, or if the window could not be opened.
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
        if not (len(players) > 0):
            raise PyRatException("Argument 'players' must contain at least one player, got an empty list")
        if not all(player.get_name() in game_state.player_locations for player in players):
            raise PyRatException(f"All players must be in the game state, got player {next(player.get_name() for player in players if player.get_name() not in game_state.player_locations)!r}, which is not in 'game_state.player_locations' (players of the game state: {game_state.get_players()!r})")

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
                raise PyRatException("The graphical interface could not be started, see the error reported above by the PyRat window, or render the game in the terminal with render_mode=RenderMode.ANSI")

        # At each turn, send current info to the process
        else:
            self.__gui_queue.put(game_state)

##########################################################################################
######################################## FUNCTIONS #######################################
##########################################################################################

def _check_main_guard () -> None:

    """
    Checks that the script running the game creates it from a block ``if __name__ == "__main__":``.
    The window is opened in another process, and on some systems (Windows, macOS), this process starts by executing the main script again.
    Outside of such a block, the script would then create a new game in this process, which fails with an error that is hard to understand, and leaves the game waiting for a window that never opens.
    The block is required on all systems, so that a script working on one system also works on the others.
    Nothing is checked when there is no script to execute again (interactive session, ``python -c``), or when Python does not execute it again (module ``__main__`` of a package run with ``python -m``).
    It is defined outside of the class as it does not depend on it.

    Raises:
        PyRatException: If the game is created by the main script outside of a block ``if __name__ == "__main__":``.
    """

    # Find the code of the main script that is being executed, which is the outermost one executed at the level of a module and named as the main module
    # When the main script is executed again by another process, it is named "__mp_main__", and this means that it is not protected by the block
    main_frame = None
    frame = inspect.currentframe()
    while frame is not None:
        if frame.f_code.co_name == "<module>" and frame.f_globals.get("__name__") in ("__main__", "__mp_main__"):
            main_frame = frame
        frame = frame.f_back
    if main_frame is None or main_frame.f_lineno is None:
        return
    script_path = main_frame.f_code.co_filename
    line_number = main_frame.f_lineno
    error_message = f"The game must be created from a block 'if __name__ == \"__main__\":' of the script that runs it, which is not the case at line {line_number} of {script_path} -- The window of the game is opened in another process, which executes the script again on some systems (Windows, macOS), so please move the code that creates and starts the game into such a block, as in 'games/sample_game.py'"
    if main_frame.f_globals.get("__name__") == "__mp_main__":
        raise PyRatException(error_message)

    # Python does not execute again the module "__main__" of a package run with "python -m"
    main_spec = main_frame.f_globals.get("__spec__")
    if main_spec is not None and (main_spec.name == "__main__" or main_spec.name.endswith(".__main__")):
        return

    # Read the script, unless it has no file (interactive session, "python -c")
    try:
        with tokenize.open(script_path) as script_file:
            script_tree = ast.parse(script_file.read(), filename=script_path)
    except (OSError, SyntaxError, ValueError):
        return

    # Look for a block 'if __name__ == "__main__":' containing the line being executed
    for node in ast.walk(script_tree):
        if isinstance(node, ast.If) and isinstance(node.test, ast.Compare) and len(node.test.ops) == 1 and isinstance(node.test.ops[0], ast.Eq):
            compared = [node.test.left, node.test.comparators[0]]
            compares_name = any(isinstance(element, ast.Name) and element.id == "__name__" for element in compared)
            compares_main = any(isinstance(element, ast.Constant) and element.value == "__main__" for element in compared)
            if compares_name and compares_main and node.body[0].lineno <= line_number <= node.body[-1].end_lineno:
                return

    # The game is created outside of the block
    raise PyRatException(error_message)

##########################################################################################
##########################################################################################
