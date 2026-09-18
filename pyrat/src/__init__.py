##########################################################################################
########################################## INFO ##########################################
##########################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.

"""
This package contains the source code of the PyRat library.
Its modules are internal: programs should import what they need from the ``pyrat`` package directly, using ``from pyrat import <element_name>``.

The code is organized in the following packages:
    * ``game`` runs games, and defines the game state, the enumerations and the exceptions.
    * ``players`` defines the base class of the players, and a player replaying recorded actions.
    * ``mazes`` defines graphs, mazes, and the algorithms that generate random mazes.
    * ``rendering`` displays games, in a terminal or in a window.

Two modules complete these packages:
    * ``utils`` provides small helpers shared by the packages above.
    * ``workspace`` creates the workspace of the students, and implements the ``pyrat-init`` command.
"""

##########################################################################################
##########################################################################################
