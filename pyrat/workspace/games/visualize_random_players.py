#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

# This file is part of the PyRat library.
# It describes a script that creates a PyRat game.
# Please import necessary elements using the following syntax:
#     from pyrat import <element_name>
#     from players.<player_name> import <player_name>

"""
In this script, we visualize four players in the same maze, one after the other.
Each player is a random player that performs random actions.
This is useful to see how the players behave in the same environment.
The maze is the same for all players, thanks to a fixed random seed.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
import pprint

# PyRat imports
from pyrat import Game, StartingLocation
from players.Random1 import Random1
from players.Random2 import Random2
from players.Random3 import Random3
from players.Random4 import Random4

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
                   "nb_cheese": 1,
                   "trace_length": 1000}

    # Instantiate a game with specified arguments
    game = Game(**game_config)
    
    # Let's visualize the three players in the same maze, one after the other
    # To make sure that the maze is the same for all players, we will add a fixed seed to the game configuration
    # This is done by the `random_seed` argument of the Game class, defined in the dictionary above
    for player in [Random1(), Random2(), Random3(), Random4()]:

        # Add player to the game, starting at the bottom left corner
        game.add_player(player, location=StartingLocation.BOTTOM_LEFT)

        # Start the game
        stats = game.start()
        print(f"Statistics for {player.get_name()}:")
        pprint.pprint(stats)

        # Reset the game for the next player
        # Argument same=True means that the game will keep the same maze and cheese distribution
        game.reset(keep_players=False, same=True)

#####################################################################################################################################################
#####################################################################################################################################################