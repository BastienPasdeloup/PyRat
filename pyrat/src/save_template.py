#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

# This file is part of the PyRat library.
# It describes a script that creates a PyRat game.
# Please import necessary elements using the following syntax:
#     from pyrat import <element_name>
#     from players import <player_name>

"""
This script was generated from a template.
It is a replay of a previously recorded game.
Actions are stored in a list, and the game is played by executing these actions in order.
No complex logic is implemented, as the actions are predefined.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
import pprint

# PyRat imports
from pyrat import FixedPlayer, Game, Action, GameMode, PlayerSkin

#####################################################################################################################################################
####################################################################### SCRIPT ######################################################################
#####################################################################################################################################################

if __name__ == "__main__":

    # First, let's customize the game elements
    game_config = {CONFIG}

    # Instanciate the game with the chosen configuration
    game = Game(**game_config)

    # Description of the players
    player_descriptions = {PLAYERS}

    # Instanciate and register players
    for player_description in player_descriptions:
        player = FixedPlayer(player_description["actions"], player_description["name"], player_description["skin"])
        game.add_player(player, player_description["team"], player_description["location"])

    # Start the game
    stats = game.start()
    print(stats)

#####################################################################################################################################################
#####################################################################################################################################################