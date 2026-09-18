##########################################################################################
########################################## INFO ##########################################
##########################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# It is internal to the library, and nothing in it is meant to be imported by PyRat programs.

"""
This package contains the graphical interface of PyRat, used by the ``PygameRenderingEngine`` rendering engine.

It is organized as follows:
    * ``process`` is the entry point of the process running the window, and the only module of this package the game process imports.
    * ``window`` runs the window: it receives the states of the game, animates the moves, and reacts to what the user does.
    * ``scene`` draws the interface, using a single background image for everything that does not move.
    * ``layout`` computes every size and position from the size of the window.
    * ``assets`` loads and scales the images, texts and sounds.
    * ``animation`` paces the animations, so that a move lasts the same time on every machine.

The images and sounds themselves are stored in the ``pyrat/gui`` directory of the library, which is not a Python package.
"""

##########################################################################################
##########################################################################################
