##########################################################################################
########################################## INFO ##########################################
##########################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# Please import necessary elements using the following syntax:
#     from pyrat import <element_name>

"""
This module defines the exception raised by PyRat when something goes wrong during a game.
Catching it allows a program to react to a failing game, for instance to skip it when running many games in a row.
"""

##########################################################################################
######################################### CLASSES ########################################
##########################################################################################

class PyRatException (Exception):

    """
    *(This class inherits from* ``Exception`` *).*

    The exception raised by PyRat when a game cannot proceed.
    Typical causes are a player that crashes or returns something that is not an action, or a workspace that cannot be created.

    Note that invalid arguments given to the classes and functions of the library are reported with assertions, as they indicate a programming error rather than something that happened during the game.

    Here is an example of how to catch it:

    .. code-block:: python

        from pyrat import Game, PyRatException

        game = Game()
        game.add_player(MyPlayer())
        try:
            stats = game.start()
        except PyRatException as error:
            print("The game could not be played:", error)
    """

    # Nothing to add to the base class, the type itself carries the information
    pass

##########################################################################################
##########################################################################################
