#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

# This file is provided as an example by the PyRat library.
# It describes a script that creates a PyRat game.
# Please import necessary elements using the following syntax:
#     from pyrat import <element_name>
#     from players.<player_name> import <player_name>

"""
This file is a script that creates a PyRat game.
In this script, we create a match between two players.
We also configure the game with specific parameters such as the maze size, cheese count, and wall percentage.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
import pprint

# PyRat imports
from pyrat import Game, PlayerSkin
from players.Random2 import Random2
from players.Random3 import Random3

#####################################################################################################################################################
####################################################################### SCRIPT ######################################################################
#####################################################################################################################################################

if __name__ == "__main__":

    # First, let's customize the game elements
    # This is done by setting the arguments of the Game class when instantiating it
    # In Python, we can also create a dictionary `d` with these arguments and pass it to the Game class using `game = Game(**d)`
    # This can be convenient for code organization and readability
    game_config = {"mud_percentage": 20.0,
                   "cell_percentage": 80.0,
                   "wall_percentage": 60.0,
                   "maze_width": 13,
                   "maze_height": 10,
                   "nb_cheese": 5}

    # Instantiate a game with specified arguments
    game = Game(**game_config)

    # Instantiate players with different skins, and add them to the game in distinct teams
    player_1 = Random2(skin=PlayerSkin.RAT)
    player_2 = Random3(skin=PlayerSkin.PYTHON)
    game.add_player(player_1, team="Team Ratz")
    game.add_player(player_2, team="Team Pythonz")

    # Start the game
    stats = game.start()
    pprint.pprint(stats)

#####################################################################################################################################################
#####################################################################################################################################################