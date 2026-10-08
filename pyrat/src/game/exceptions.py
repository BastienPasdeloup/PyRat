##########################################################################################
########################################## INFO ##########################################
##########################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# Please import necessary elements using the following syntax:
#     from pyrat import <element_name>

"""
This module defines the exceptions raised by PyRat when something goes wrong.
There are two of them, depending on where the error comes from:
    * ``PyRatException`` is raised when the library is used incorrectly, for instance with an invalid argument.
    * ``PyRatPlayerException`` is raised when a player causes an error during a game, for instance by crashing or by returning something that is not an action.
Since ``PyRatPlayerException`` inherits from ``PyRatException``, catching the latter catches both.
"""

##########################################################################################
######################################### CLASSES ########################################
##########################################################################################

class PyRatException (Exception):

    """
    *(This class inherits from* ``Exception`` *).*

    The exception raised by PyRat when the library is used incorrectly, or cannot do what it is asked.
    Typical causes are an invalid argument given to a class or a function of the library (e.g., a vertex that is not in a graph, or a percentage greater than 100), a workspace that cannot be created, or a game interrupted by the user (Ctrl+C in the terminal).

    Errors caused by players during a game are reported with ``PyRatPlayerException``, which inherits from this class.

    Here is an example of how to catch it:

    .. code-block:: python

        from pyrat import Graph, PyRatException

        graph = Graph()
        graph.add_vertex(0)
        try:
            graph.get_neighbors(1)
        except PyRatException as error:
            print("Invalid use of the library:", error)
    """

    # Nothing to add to the base class, the type itself carries the information
    pass

##########################################################################################

class PyRatPlayerException (PyRatException):

    """
    *(This class inherits from* ``PyRatException`` *).*

    The exception raised by PyRat when a player causes an error during a game.
    Typical causes are a player that crashes during ``preprocessing(...)``, ``turn(...)`` or ``postprocessing(...)`` (including when it uses the library incorrectly), or a player whose ``turn(...)`` method returns something that is not an action.
    The error of the player itself is printed when it happens, and the game stops with this exception, unless the game was created with ``continue_on_error=True``.

    Here is an example of how to catch it:

    .. code-block:: python

        from pyrat import Game, PyRatPlayerException

        game = Game()
        game.add_player(MyPlayer())
        try:
            stats = game.start()
        except PyRatPlayerException as error:
            print("A player caused an error:", error)
    """

    # Nothing to add to the base class, the type itself carries the information
    pass

##########################################################################################
##########################################################################################
