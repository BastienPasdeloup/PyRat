#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This file is part of the PyRat library.
    It is meant to be used as a library, and not to be executed directly.
    Please import necessary elements using the following syntax:
        from pyrat import <element_name>
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
from typing import *
from typing_extensions import *
from numbers import *
import colored
import re
import math
import sys

# PyRat imports
from pyrat.src.RenderingEngine import RenderingEngine
from pyrat.src.Player import Player
from pyrat.src.Maze import Maze
from pyrat.src.GameState import GameState

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class ShellRenderingEngine (RenderingEngine):

    """
        This class inherits from the RenderingEngine class.
        Therefore, it has the attributes and methods defined in the RenderingEngine class in addition to the ones defined below.

        An ASCII rendering engine is a rendering engine that can render a PyRat game in ASCII.
        It also supports ANSI escape codes to colorize the rendering.
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self:       Self,
                   use_colors: bool = True,
                   *args:      Any,
                   **kwargs:   Any
                 ) ->          Self:

        """
            This function is the constructor of the class.
            We do not duplicate asserts already made in the parent method.
            In:
                * self:       Reference to the current object.
                * use_colors: Boolean indicating whether the rendering engine should use colors or not.
                * args:       Arguments to pass to the parent constructor.
                * kwargs:     Keyword arguments to pass to the parent constructor.
            Out:
                * A new instance of the class.
        """

        # Inherit from parent class
        super().__init__(*args, **kwargs)

        # Debug
        assert isinstance(use_colors, bool) # Type check for the use of colors

        # Private attributes
        self.__use_colors = use_colors

    #############################################################################################################################################
    #                                                               PUBLIC METHODS                                                              #
    #############################################################################################################################################

    def render ( self:       Self,
                 players:    List[Player],
                 maze:       Maze,
                 game_state: GameState,
               ) ->          None:
        
        """
            This method redefines the method of the parent class.
            This function renders the game to show its current state.
            It does so by creating a string representing the game state and printing it.
            In:
                * self:       Reference to the current object.
                * players:    Players of the game.
                * maze:       Maze of the game.
                * game_state: State of the game.
            Out:
                * None.
        """

        # Debug
        assert isinstance(players, list) # Type check for the players
        assert all(isinstance(player, Player) for player in players) # Type check for the players
        assert isinstance(maze, Maze) # Type check for the maze
        assert isinstance(game_state, GameState) # Type check for the game state

        # Dimensions
        max_weight = max([maze.get_weight(vertex, neighbor) for vertex in maze.vertices for neighbor in maze.get_neighbors(vertex)])
        max_weight_len = len(str(max_weight))
        max_player_name_len = max([len(player.name) for player in players]) + (max_weight_len + 5 if max_weight > 1 else 0)
        max_cell_number_len = len(str(maze.width * maze.height - 1))
        cell_width = max(max_player_name_len, max_weight_len, max_cell_number_len + 1) + 2
        
        # Game elements
        wall = self.__colorize(" ", colored.bg("light_gray"), "#")
        ground = self.__colorize(" ", colored.bg("grey_23"))
        cheese = self.__colorize("▲", colored.bg("grey_23") + colored.fg("yellow_1"))
        mud_horizontal = self.__colorize("ⴾ", colored.bg("grey_23") + colored.fg("orange_4b"))
        mud_vertical = self.__colorize("ⵘ", colored.bg("grey_23") + colored.fg("orange_4b"))
        mud_value = lambda number: self.__colorize(str(number), colored.bg("grey_23") + colored.fg("orange_4b"))
        path_horizontal = self.__colorize("⋅", colored.bg("grey_23") + colored.fg("orange_4b"))
        path_vertical = self.__colorize("ⵗ", colored.bg("grey_23") + colored.fg("orange_4b"))
        cell_number = lambda number: self.__colorize(str(number), colored.bg("grey_23") + colored.fg("magenta"))
        score_cheese = self.__colorize("▲ ", colored.fg("yellow_1"))
        score_half_cheese = self.__colorize("△ ", colored.fg("yellow_1"))
        
        # Player/team elements
        teams = {team: self.__colorize(team, colored.fg(9 + list(game_state.teams.keys()).index(team))) for team in game_state.teams}
        mud_indicator = lambda player_name: " (" + ("⬇" if maze.coords_difference(game_state.muds[player_name]["target"], game_state.player_locations[player_name]) == (1, 0) else "⬆" if maze.coords_difference(game_state.muds[player_name]["target"], game_state.player_locations[player_name]) == (-1, 0) else "➡" if maze.coords_difference(game_state.muds[player_name]["target"], game_state.player_locations[player_name]) == (0, 1) else "⬅") + " " + str(game_state.muds[player_name]["count"]) + ")" if game_state.muds[player_name]["count"] > 0 else ""
        player_names = {player.name: self.__colorize(player.name + mud_indicator(player.name), colored.bg("grey_23") + colored.fg(9 + ["team" if player.name in team else 0 for team in game_state.teams.values()].index("team"))) for player in players}
        
        # Game info
        environment_str = "" if self.__use_colors else "\n"
        environment_str += "Game over" if game_state.game_over() else "Starting turn %d" % game_state.turn if game_state.turn > 0 else "Initial configuration"
        team_scores = game_state.get_score_per_team()
        scores_str = ""
        for team in game_state.teams:
            scores_str += "\n" + score_cheese * int(team_scores[team]) + score_half_cheese * math.ceil(team_scores[team] - int(team_scores[team]))
            scores_str += "[" + teams[team] + "] " if len(teams) > 1 or len(team) > 0 else ""
            scores_str += " + ".join(["%s (%s)" % (player_in_team, str(round(game_state.score_per_player[player_in_team], 3)).rstrip('0').rstrip('.') if game_state.score_per_player[player_in_team] > 0 else "0") for player_in_team in game_state.teams[team]])
        environment_str += scores_str

        # Consider cells in lexicographic order
        environment_str += "\n" + wall * (maze.width * (cell_width + 1) + 1)
        for row in range(maze.height):
            players_in_row = [game_state.player_locations[player.name] for player in players if maze.i_to_rc(game_state.player_locations[player.name])[0] == row]
            cell_height = max([players_in_row.count(cell) for cell in players_in_row] + [max_weight_len]) + 2
            environment_str += "\n"
            for subrow in range(cell_height):
                environment_str += wall
                for col in range(maze.width):
                    
                    # Check cell contents
                    players_in_cell = [player.name for player in players if game_state.player_locations[player.name] == maze.rc_to_i(row, col)]
                    cheese_in_cell = maze.rc_to_i(row, col) in game_state.cheese

                    # Find subrow contents (nothing, cell number, cheese, trace, player)
                    background = wall if not maze.rc_exists(row, col) else ground
                    cell_contents = ""
                    if subrow == 0:
                        if background != wall and not self._render_simplified:
                            cell_contents += background
                            cell_contents += cell_number(maze.rc_to_i(row, col))
                    elif cheese_in_cell:
                        if subrow == (cell_height - 1) // 2:
                            cell_contents = background * ((cell_width - self.__colored_len(cheese)) // 2)
                            cell_contents += cheese
                        else:
                            cell_contents = background * cell_width
                    else:
                        first_player_index = (cell_height - len(players_in_cell)) // 2
                        if first_player_index <= subrow < first_player_index + len(players_in_cell):
                            cell_contents = background * ((cell_width - self.__colored_len(player_names[players_in_cell[subrow - first_player_index]])) // 2)
                            cell_contents += player_names[players_in_cell[subrow - first_player_index]]
                        else:
                            cell_contents = background * cell_width
                    environment_str += cell_contents
                    environment_str += background * (cell_width - self.__colored_len(cell_contents))
                    
                    # Right separation
                    right_weight = "0" if not maze.rc_exists(row, col) or not maze.rc_exists(row, col + 1) or not maze.has_edge(maze.rc_to_i(row, col), maze.rc_to_i(row, col + 1)) else str(maze.get_weight(maze.rc_to_i(row, col), maze.rc_to_i(row, col + 1)))
                    if col == maze.width - 1 or right_weight == "0":
                        environment_str += wall
                    else:
                        if right_weight == "1":
                            environment_str += path_vertical
                        elif not self._render_simplified and math.ceil((cell_height - len(right_weight)) / 2) <= subrow < math.ceil((cell_height - len(right_weight)) / 2) + len(right_weight):
                            digit_number = subrow - math.ceil((cell_height - len(right_weight)) / 2)
                            environment_str += mud_value(right_weight[digit_number])
                        else:
                            environment_str += mud_vertical
                environment_str += "\n"
            environment_str += wall
            
            # Bottom separation
            for col in range(maze.width):
                bottom_weight = "0" if not maze.rc_exists(row, col) or not maze.rc_exists(row + 1, col) or not maze.has_edge(maze.rc_to_i(row, col), maze.rc_to_i(row + 1, col)) else str(maze.get_weight(maze.rc_to_i(row, col), maze.rc_to_i(row + 1, col)))
                if bottom_weight == "0":
                    environment_str += wall * (cell_width + 1)
                elif bottom_weight == "1":
                    environment_str += path_horizontal * cell_width + wall
                else:
                    cell_contents = mud_horizontal * ((cell_width - self.__colored_len(bottom_weight)) // 2) + mud_value(bottom_weight) if not self._render_simplified else ""
                    environment_str += cell_contents
                    environment_str += mud_horizontal * (cell_width - self.__colored_len(cell_contents)) + wall
        
        # Render
        if self.__use_colors:
            nb_rows = 1 + len(environment_str.splitlines())
            nb_cols = 1 + (cell_width + 1) * maze.width
            print("\x1b[8;%d;%dt" % (nb_rows, nb_cols), file=sys.stderr)
        print(environment_str, file=sys.stderr)
        
    #############################################################################################################################################
    #                                                              PRIVATE METHODS                                                              #
    #############################################################################################################################################

    def __colorize ( self:           Self,
                     text:           str,
                     colorization:   str,
                     alternate_text: Optional[str] = None
                   ) ->              str:
        
        """
            This method colorizes a text.
            It does so by adding the colorization to the text and resetting the colorization at the end of the text.
            In:
                * self:           Reference to the current object.
                * text:           Text to colorize.
                * colorization:   Colorization to use.
                * alternate_text: Alternate text to use if we don't use colors and the provided text does not fit.
            Out:
                * colorized_text: Colorized text.
        """

        # Debug
        assert isinstance(text, str) # Type check for the text
        assert isinstance(colorization, str) # Type check for the colorization
        assert isinstance(alternate_text, (str, type(None))) # Type check for the alternate text

        # If we don't use colors, we return the correct text
        if not self.__use_colors:
            if alternate_text is None:
                colorized_text = str(text)
            else:
                colorized_text = str(alternate_text)
        
        # If using colors, we return the colorized text
        else:
            colorized_text = colorization + str(text) + colored.attr(0)

        # Return the colorized (or not) text
        return colorized_text
    
    #############################################################################################################################################

    def __colored_len ( self: Self,
                        text: str
                      ) ->    Integral:
        
        """
            This method returns the true len of a color-formated string.
            In:
                * self: Reference to the current object.
                * text: Text to measure.
            Out:
                * text_length: Length of the text.
        """

        # Debug
        assert isinstance(text, str) # Type check for the text

        # Return the length of the text without the colorization
        text_length = len(re.sub(r"[\u001B\u009B][\[\]()#;?]*((([a-zA-Z\d]*(;[-a-zA-Z\d\/#&.:=?%@~_]*)*)?\u0007)|((\d{1,4}(?:;\d{0,4})*)?[\dA-PR-TZcf-ntqry=><~]))", "", text))
        return text_length
    
#####################################################################################################################################################
#####################################################################################################################################################
