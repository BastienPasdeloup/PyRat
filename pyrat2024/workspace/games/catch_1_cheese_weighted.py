#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This file defines a game where there is only one cheese to catch in a maze with mud.
    Objective of the game is to catch the cheese as fast as possible.
    
    When running this file, it will create a PyRat game, add a player to it, and start the game.
    Here, the player used is Random4 for illustration purposes.
    Change the player to your own to test it in the game scenario.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
import sys
import os

# Add needed directories to the path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "players"))

# Internal imports
from pyrat2024 import Game
from Random4 import Random4

#####################################################################################################################################################
######################################################################## GO! ########################################################################
#####################################################################################################################################################

if __name__ == "__main__":

    # Customize the game elements
    config = {"maze_width": 19,
              "maze_height": 15,
              "nb_cheese": 1,
              "trace_length": 1000}
    
    # Instanciate the game with the chosen configuration
    game = Game(**config)

    # Instanciate and register player
    player = Random4()
    game.add_player(player)
    
    # Start the game and show statistics when over
    stats = game.start()
    print(stats)

#####################################################################################################################################################
#####################################################################################################################################################