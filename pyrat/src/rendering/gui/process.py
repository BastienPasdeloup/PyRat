##########################################################################################
########################################## INFO ##########################################
##########################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# It is internal to the library, and nothing in it is meant to be imported by PyRat programs.

"""
This module is the entry point of the process running the window of the graphical interface.

It is the only module of the ``gui`` package imported by the process running the game.
It therefore imports neither ``pygame`` nor the other modules of the package at the top level, so that only the process of the window loads them.
"""

##########################################################################################
######################################### IMPORTS ########################################
##########################################################################################

# External imports
import multiprocessing.managers as mpmanagers
import os
import sys
import traceback

# PyRat imports
from pyrat.src.mazes.maze import Maze
from pyrat.src.game.game_state import GameState
from pyrat.src.players.player import Player

##########################################################################################
######################################## FUNCTIONS #######################################
##########################################################################################

def run_gui_process ( gui_initialized_synchronizer: mpmanagers.BarrierProxy,
                      gui_queue:                    mpmanagers.BaseProxy,
                      maze:                         Maze,
                      initial_game_state:           GameState,
                      players:                      list[Player],
                      fullscreen:                   bool,
                      render_simplified:            bool,
                      trace_length:                 int,
                      rendering_speed:              float
                    ) ->                            None:

    """
    Opens the window of the game, tells the game that it is ready, and runs it until the user closes it.
    If the window cannot be opened, the game is told so, rather than waiting forever for a window that will never come.
    Errors are reported in the terminal, as the window has no other way to report them.

    Args:
        gui_initialized_synchronizer: Barrier used to tell the game that the window is ready.
        gui_queue:                    Queue through which the states of the game are received.
        maze:                         Maze of the game.
        initial_game_state:           State of the game before it starts.
        players:                      Players of the game.
        fullscreen:                   Indicates if the window should be fullscreen.
        render_simplified:            If ``True``, the details of the maze are not drawn.
        trace_length:                 Number of cells of trace to show behind a player.
        rendering_speed:              Speed at which the moves are shown, relative to the default one.
    """

    # Pygame prints a message when imported, which has nothing to do in the terminal of the game
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

    # Open the window, then run it
    # The game waits for the window to be open before starting, so that the first turns are not missed
    window_is_open = False
    try:
        from pyrat.src.rendering.gui.window import GameWindow
        window = GameWindow(maze, initial_game_state, players, fullscreen, render_simplified, trace_length, rendering_speed)
        window_is_open = True
        gui_initialized_synchronizer.wait()
        window.run(gui_queue)

    # The user interrupted the game from the terminal, the window just closes
    except KeyboardInterrupt:
        pass

    # Report errors, and release the game if it is still waiting for the window
    except Exception:
        print("The PyRat window has stopped with the following error:", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        if not window_is_open:
            gui_initialized_synchronizer.abort()

##########################################################################################
##########################################################################################
