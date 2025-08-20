#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# Please import necessary elements using the following syntax:
#     from pyrat import <element_name>

"""
This module provides a game state that is a snapshot of the game at a given time.
At each turn, the game creates a new instance of this class.
It gives an overview of scores, locations, available cheese, who is currently crossing mud, etc.
It also provides a few useful functions to determine who is currently leading, etc.
This game state is then provided to players so that they can make decisions based on the current state of the game.
"""

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class GameState ():

    """
    A game state is a snapshot of the game at a given time.
    It gives an overview of scores, locations, available cheese, who is currently crossing mud, etc.
    It also provides a few useful functions to determine who is currently leading, etc.
    Objects of this class are created each turn, so manually changing the attributes will not allow you to cheat :)
    """

    #############################################################################################################################################
    #                                                               MAGIC METHODS                                                               #
    #############################################################################################################################################

    def __init__ (self) -> None:

        """
        Initializes a new instance of the class.
        
        This constructor defines some public attributes that are used to store the state of the game.
        You can access these attributes to get information about the game state.

        Accessible attributes are:
            * ``player_locations``: Dictionary of player names and their current locations.
            * ``score_per_player``: Dictionary of player names and their current scores.
            * ``muds``: Dictionary of players currently crossing mud, with their target cell and the number of turns left to reach it.
            * ``teams``: Dictionary of team names and their members.
            * ``cheese``: List of cheese locations.
            * ``turn``: Current turn number (starting from 0).
        """

        # Public attributes
        self.player_locations = {}
        self.score_per_player = {}
        self.muds = {}
        self.teams = {}
        self.cheese = []
        self.turn = 0

    #############################################################################################################################################

    def __str__ (self) -> str:

        """
        Returns a string representation of the object.
        
        Returns:
            String representation of the object.
        """

        # Create the string
        string = "GameState object:\n"
        string += "|  Locations: {}\n".format(self.player_locations)
        string += "|  Scores: {}\n".format(self.score_per_player)
        string += "|  Muds: {}\n".format(self.muds)
        string += "|  Teams: {}\n".format(self.teams)
        string += "|  Cheese: {}\n".format(self.cheese)
        string += "|  Turn: {}".format(self.turn)
        return string

    #############################################################################################################################################
    #                                                               PUBLIC METHODS                                                              #
    #############################################################################################################################################
    
    def is_in_mud ( self,
                    name: str
                  ) ->    bool:

        """
        Returns whether a player is currently crossing mud.

        Args:
            name: Name of the player.

        Returns:
            ``True`` if the player is currently crossing mud, ``False`` otherwise.
        """

        # Debug
        assert isinstance(name, str), "Argument 'name' must be a string"
        assert name in self.get_players(), "Player '%s' is not in the game" % name

        # Get whether the player is currently crossing mud
        in_mud = self.muds[name]["target"] is not None
        return in_mud
    
    #############################################################################################################################################

    def game_over (self) -> bool:
        
        """
        Checks if the game is over.
        The game is over when there is no more cheese or when no team can catch up anymore.

        Returns:
            ``True`` if the game is over, ``False`` otherwise.
        """

        # The game is over when there is no more cheese
        if len(self.cheese) == 0:
            is_over = True
            return is_over

        # In a multi-team game, the game is over when no team can change their ranking anymore
        score_per_team = self.get_score_per_team()
        if len(score_per_team) > 1:
            is_over = True
            for team_1 in score_per_team:
                for team_2 in score_per_team:
                    if team_1 != team_2:
                        if score_per_team[team_1] == score_per_team[team_2] or (score_per_team[team_1] < score_per_team[team_2] and score_per_team[team_1] + len(self.cheese) >= score_per_team[team_2]):
                            is_over = False
            return is_over

        # The game is not over
        is_over = False
        return is_over

    #############################################################################################################################################

    def get_players (self) -> list[str]:
        
        """
        Returns the names of the players in the game.

        Returns:
            List of player names.
        """

        # Return the list of player names
        players = list(self.player_locations.keys())
        return players

    #############################################################################################################################################

    def get_score_per_team (self) -> dict[str, float]:
        
        """
        Returns the score per team.

        Returns:
            Dictionary of scores per team.
        """
        
        # Aggregate players of the team
        score_per_team = {team: round(sum([self.score_per_player[player] for player in self.teams[team]]), 5) for team in self.teams}
        return score_per_team

#####################################################################################################################################################
#####################################################################################################################################################
