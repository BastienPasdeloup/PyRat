#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# Please import necessary elements using the following syntax:
#     from pyrat import <element_name>

"""
This module provides a rendering engine using the shell.
It will print the game state to the console using ASCII characters and ANSI escape codes for colors.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
import colored
import re
import math
import sys
import platform
import os
import time

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
    *(This class inherits from* ``RenderingEngine`` *).*
    
    An ASCII rendering engine is a rendering engine that can render a PyRat game in ASCII.
    It also supports ANSI escape codes to colorize the rendering.
    """

    #############################################################################################################################################
    #                                                               MAGIC METHODS                                                               #
    #############################################################################################################################################

    def __init__ ( self,
                   use_colors:      bool = True,
                   clear_each_turn: bool = True,
                   *args:           object,
                   **kwargs:        object
                 ) ->               None:

        """
        Initializes a new instance of the class.
        
        Args:
            use_colors:      Boolean indicating whether the rendering engine should use colors or not.
            clear_each_turn: Boolean indicating whether the rendering engine should clear the screen each turn.
            args:            Arguments to pass to the parent constructor.
            kwargs:          Keyword arguments to pass to the parent constructor.
        """

        # Inherit from parent class
        super().__init__(*args, **kwargs)

        # Debug
        assert isinstance(use_colors, bool), "Argument 'use_colors' must be a boolean"
        assert isinstance(clear_each_turn, bool), "Argument 'clear_each_turn' must be a boolean"

        # Private attributes
        self.__use_colors = use_colors
        self.__clear_each_turn = clear_each_turn

    #############################################################################################################################################
    #                                                               PUBLIC METHODS                                                              #
    #############################################################################################################################################

    def render ( self,
                 players:    list[Player],
                 maze:       Maze,
                 game_state: GameState,
               ) ->          None:
        
        """
        *(This method redefines the method of the parent class with the same name).*
        
        This function renders the game to show its current state.
        It does so by creating a string representing the game state and printing it.
        
        Args:
            players:    Players of the game.
            maze:       Maze of the game.
            game_state: State of the game.
        """

        # Debug
        assert isinstance(players, list), "Argument 'players' must be a list"
        assert all(isinstance(player, Player) for player in players), "All elements of 'players' must be of type 'pyrat.Player'"
        assert isinstance(maze, Maze), "Argument 'maze' must be of type 'pyrat.Maze'"
        assert isinstance(game_state, GameState), "Argument 'game_state' must be of type 'pyrat.GameState'"

        # Dimensions
        max_weight = max([maze.get_weight(*edge) for edge in maze.get_edges()])
        max_weight_len = len(str(max_weight))
        max_player_name_len = max([len(player.get_name()) for player in players]) + (max_weight_len + 5 if max_weight > 1 else 0)
        max_cell_number_len = len(str(maze.get_width() * maze.get_height() - 1))
        cell_width = max(max_player_name_len, max_weight_len, max_cell_number_len + 1) + 2
        
        # Colors
        wall_color = "white"
        ground_color = "grey_23"
        cheese_color = "yellow_1"
        mud_color = "orange_1"
        path_color = "white"
        number_color = "magenta"

        # Game elements
        ground = self.__colorize(" ", colored.bg(ground_color))
        wall = self.__colorize(" ", colored.bg(wall_color) + colored.fg(wall_color), "▉")
        cheese = self.__colorize("▲", colored.bg(ground_color) + colored.fg(cheese_color))
        mud_horizontal = self.__colorize("━", colored.bg(ground_color) + colored.fg(mud_color))
        mud_vertical = self.__colorize("┃", colored.bg(ground_color) + colored.fg(mud_color))
        mud_value = lambda number: self.__colorize(str(number), colored.bg(ground_color) + colored.fg(mud_color))
        path_horizontal = self.__colorize("╌", colored.bg(ground_color) + colored.fg(path_color))
        path_vertical = self.__colorize("┆", colored.bg(ground_color) + colored.fg(path_color))
        cell_number = lambda number: self.__colorize(str(number), colored.bg(ground_color) + colored.fg(number_color))
        score_cheese = self.__colorize("▲ ", colored.fg(cheese_color))
        score_half_cheese = self.__colorize("△ ", colored.fg(cheese_color))
        
        # Player/team elements
        teams = {team: self.__colorize(team, colored.fg(9 + list(game_state.teams.keys()).index(team))) for team in game_state.teams}
        mud_indicator = lambda player_name: " (" + ("⬇" if maze.coords_difference(game_state.muds[player_name]["target"], game_state.player_locations[player_name]) == (-1, 0) else "⬆" if maze.coords_difference(game_state.muds[player_name]["target"], game_state.player_locations[player_name]) == (1, 0) else "➡" if maze.coords_difference(game_state.muds[player_name]["target"], game_state.player_locations[player_name]) == (0, 1) else "⬅") + " " + str(game_state.muds[player_name]["count"]) + ")" if game_state.muds[player_name]["count"] > 0 else ""
        player_names = {player.get_name(): self.__colorize(player.get_name() + mud_indicator(player.get_name()), colored.bg(ground_color) + ("" if len(teams) == 1 else colored.fg(9 + ["team" if player.get_name() in team else 0 for team in game_state.teams.values()].index("team")))) for player in players}
        
        # Game info
        environment_str = "Game over" if game_state.game_over() else "Starting turn %d" % game_state.turn if game_state.turn > 0 else "Initial configuration"
        team_scores = game_state.get_score_per_team()
        for team in game_state.teams:
            environment_str += "\n" + score_cheese * int(team_scores[team]) + score_half_cheese * math.ceil(team_scores[team] - int(team_scores[team]))
            environment_str += "[" + teams[team] + "] " if len(teams) > 1 or len(team) > 0 else ""
            environment_str += " + ".join(["%s (%s)" % (player_in_team, str(round(game_state.score_per_player[player_in_team], 3)).rstrip('0').rstrip('.') if game_state.score_per_player[player_in_team] > 0 else "0") for player_in_team in game_state.teams[team]])

        # Consider cells in lexicographic order
        environment_str += "\n" + wall * (maze.get_width() * (cell_width + 1) + 1)
        for row in range(maze.get_height()):
            players_in_row = [game_state.player_locations[player.get_name()] for player in players if maze.i_to_rc(game_state.player_locations[player.get_name()])[0] == row]
            cell_height = max([players_in_row.count(cell) for cell in players_in_row] + [max_weight_len]) + 2
            environment_str += "\n"
            for subrow in range(cell_height):
                environment_str += wall
                for col in range(maze.get_width()):
                    
                    # Check cell contents
                    players_in_cell = [player.get_name() for player in players if game_state.player_locations[player.get_name()] == maze.rc_to_i(row, col)]
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
                    if col == maze.get_width() - 1 or right_weight == "0":
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
            for col in range(maze.get_width()):
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
        if self.__clear_each_turn:
            self.__clear_output()
        print(environment_str, file=sys.stderr, flush=True)

        # Wait a bit
        sleep_time = 1.0 / self._rendering_speed
        time.sleep(sleep_time)
        
    #############################################################################################################################################
    #                                                              PRIVATE METHODS                                                              #
    #############################################################################################################################################

    def __clear_output (self) -> None:

        """
        This method clears the output of the console.
        It works in both Jupyter and standard environments.
        """

        # If in a Jupyter environment
        if "ipykernel" in sys.modules:
            from IPython.display import clear_output
            clear_output(wait=True)

        # If in a standard environment
        else:
            os.system("cls" if platform.system() == "Windows" else "clear")

    #############################################################################################################################################

    def __colored_len ( self,
                        text: str
                      ) ->    int:
        
        """
        This method returns the true ``len`` of a color-formated string.

        Args:
            text: Text to measure.
        
        Returns:
            The length of the text.
        """

        # Debug
        assert isinstance(text, str), "Argument 'text' must be a string"

        # Return the length of the text without the colorization
        text_length = len(re.sub(r"[\u001B\u009B][\[\]()#;?]*((([a-zA-Z\d]*(;[-a-zA-Z\d\/#&.:=?%@~_]*)*)?\u0007)|((\d{1,4}(?:;\d{0,4})*)?[\dA-PR-TZcf-ntqry=><~]))", "", text))
        return text_length
    
    #############################################################################################################################################

    def __colorize ( self,
                     text:           str,
                     colorization:   str,
                     alternate_text: str | None = None
                   ) ->              str:
        
        """
        This method colorizes a text.
        It does so by adding the colorization to the text and resetting the colorization at the end of the text.
        
        Args:
            text:           Text to colorize.
            colorization:   Colorization to use.
            alternate_text: Alternate text to use if we don't use colors and the provided text does not fit.
        
        Returns:
            The colorized text.
        """

        # Debug
        assert isinstance(text, str), "Argument 'text' must be a string"
        assert isinstance(colorization, str), "Argument 'colorization' must be a string"
        assert isinstance(alternate_text, (str, type(None))), "Argument 'alternate_text' must be a string or None"

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
    
#####################################################################################################################################################
#####################################################################################################################################################
