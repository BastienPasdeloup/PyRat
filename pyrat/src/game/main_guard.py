##########################################################################################
########################################## INFO ##########################################
##########################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# Please import necessary elements using the following syntax:
#     from pyrat import <element_name>

"""
This module checks that a game using other processes is run from a block ``if __name__ == "__main__":`` of the main script.
On some systems (Windows, macOS), a new process starts by executing the main script again, so the code that creates and starts the game must be protected by such a block.
"""

##########################################################################################
######################################### IMPORTS ########################################
##########################################################################################

# External imports
import ast
import inspect
import tokenize

# PyRat imports
from pyrat.src.game.exceptions import PyRatException

##########################################################################################
######################################## FUNCTIONS #######################################
##########################################################################################

def check_main_guard ( reason: str
                     ) ->     None:

    """
    Checks that the script running the game creates and starts it from a block ``if __name__ == "__main__":``.
    This is needed as soon as the game uses other processes (window of the game, players of the multiprocessing game modes), as on some systems (Windows, macOS), such a process starts by executing the main script again.
    Outside of such a block, the script would then create a new game in that process, which fails with an error that is hard to understand, and leaves the game waiting for a process that never starts.
    The block is required on all systems, so that a script working on one system also works on the others.
    Nothing is checked when there is no script to execute again (interactive session, ``python -c``), or when Python does not execute it again (module ``__main__`` of a package run with ``python -m``).

    Args:
        reason: Why the game uses another process, as the start of a sentence for the error message (for instance "The window of the game is opened in another process").

    Raises:
        PyRatException: If the game is created or started by the main script outside of a block ``if __name__ == "__main__":``.
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
    error_message = f"The game must be created and started from a block 'if __name__ == \"__main__\":' of the script that runs it, which is not the case at line {line_number} of {script_path} -- {reason}, which executes the script again on some systems (Windows, macOS), so please move the code that creates and starts the game into such a block, as in 'games/sample_game.py'"
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

    # The game is created or started outside of the block
    raise PyRatException(error_message)

##########################################################################################
##########################################################################################
