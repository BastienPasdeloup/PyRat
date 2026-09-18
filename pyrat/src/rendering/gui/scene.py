##########################################################################################
########################################## INFO ##########################################
##########################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# It is internal to the library, and nothing in it is meant to be imported by PyRat programs.

"""
This module draws the graphical interface.

Everything that never changes during a game (the ground, the walls, the mud, the flags, the boxes of the scores area) is drawn once into a single background image.
Drawing an image of the game then consists in copying the relevant part of that background, and drawing over it the few elements that move.
This is much cheaper than drawing every wall of the maze again at each image, and it keeps the drawing code short.
"""

##########################################################################################
######################################### IMPORTS ########################################
##########################################################################################

# External imports
import math
import os
import random
import distinctipy
import pygame

# PyRat imports
from pyrat.src.rendering.gui import layout as layout_module
from pyrat.src.rendering.gui.assets import Assets
from pyrat.src.rendering.gui.layout import Layout
from pyrat.src.mazes.maze import Maze
from pyrat.src.game.game_state import GameState
from pyrat.src.game.enums import Action
from pyrat.src.players.player import Player

##########################################################################################
######################################## FUNCTIONS #######################################
##########################################################################################

def choose_team_colors ( initial_game_state: GameState
                       ) ->                  dict[str, tuple[int, int, int]]:

    """
    Chooses a color for each team, as different from each other as possible.
    When the game has no notion of team, the only team gets the neutral color of the scores area.

    Args:
        initial_game_state: State of the game before it starts.

    Returns:
        The color of each team.
    """

    # Debug
    assert isinstance(initial_game_state, GameState), "Argument 'initial_game_state' must be of type 'pyrat.GameState'"

    # Distinct colors only make sense when teams are shown
    teams = list(initial_game_state.teams.keys())
    if not layout_module.teams_are_named(initial_game_state):
        return {team: layout_module.AVATARS_AREA_COLOR for team in teams}
    colors = distinctipy.get_colors(len(teams))
    return {teams[i]: tuple(int(c * 255) for c in colors[i]) for i in range(len(teams))}

##########################################################################################
######################################### CLASSES ########################################
##########################################################################################

class MazeDecor ():

    """
    Describes how the ground of the maze is decorated.

    The ground tile of each cell is chosen at random, but only once per game.
    Keeping that choice allows rebuilding the interface at another size without the decor changing under the eyes of the players.
    """

    ##################################################################################
    #                                   CONSTRUCTOR                                  #
    ##################################################################################

    def __init__ ( self,
                   maze:   Maze,
                   assets: Assets,
                   rng:    random.Random
                 ) ->      None:

        """
        Initializes a new instance of the class.

        Args:
            maze:   Maze of the game.
            assets: Assets of the interface, used to list the available ground tiles.
            rng:    Random number generator.
        """

        # Debug
        assert isinstance(maze, Maze), "Argument 'maze' must be of type 'pyrat.Maze'"
        assert isinstance(assets, Assets), "Argument 'assets' must be of type 'Assets'"
        assert isinstance(rng, random.Random), "Argument 'rng' must be of type 'random.Random'"

        # One tile, one rotation and one flip per existing cell
        self.tiles = {}
        for row in range(maze.get_height()):
            for col in range(maze.get_width()):
                if maze.rc_exists(row, col):
                    self.tiles[(row, col)] = (assets.random_image_name("ground"), rng.randint(0, 3) * 90, bool(rng.randint(0, 1)), bool(rng.randint(0, 1)))

##########################################################################################

class Scene ():

    """
    Builds and draws the graphical interface at a given size.

    An instance is tied to one ``Layout``, thus to one window size.
    When the window is resized, a new instance is built, which rebuilds the images at the new scale.
    """

    ##################################################################################
    #                                   CONSTRUCTOR                                  #
    ##################################################################################

    def __init__ ( self,
                   assets:             Assets,
                   layout:             Layout,
                   maze:               Maze,
                   initial_game_state: GameState,
                   players:            list[Player],
                   team_colors:        dict[str, tuple[int, int, int]],
                   decor:              MazeDecor,
                   render_simplified:  bool,
                   trace_colors:       dict[str, tuple] | None = None
                 ) ->                  None:

        """
        Initializes a new instance of the class, and builds all the images of the interface.

        Args:
            assets:             Assets of the interface.
            layout:             Geometry of the interface.
            maze:               Maze of the game.
            initial_game_state: State of the game before it starts.
            players:            Players of the game.
            team_colors:        Color associated with each team.
            decor:              Decoration of the ground, shared by all sizes.
            render_simplified:  If ``True``, the details of the maze are not drawn.
            trace_colors:       Color of the trace of each player, to reuse the colors of a previous size, or ``None`` to compute them.
        """

        # Debug
        assert isinstance(assets, Assets), "Argument 'assets' must be of type 'Assets'"
        assert isinstance(layout, Layout), "Argument 'layout' must be of type 'Layout'"
        assert isinstance(maze, Maze), "Argument 'maze' must be of type 'pyrat.Maze'"
        assert isinstance(initial_game_state, GameState), "Argument 'initial_game_state' must be of type 'pyrat.GameState'"
        assert isinstance(players, list), "Argument 'players' must be a list"
        assert all(isinstance(player, Player) for player in players), "All elements of 'players' must be of type 'pyrat.Player'"
        assert isinstance(team_colors, dict), "Argument 'team_colors' must be a dictionary"
        assert isinstance(decor, MazeDecor), "Argument 'decor' must be of type 'MazeDecor'"
        assert isinstance(render_simplified, bool), "Argument 'render_simplified' must be a boolean"
        assert isinstance(trace_colors, (dict, type(None))), "Argument 'trace_colors' must be a dictionary or None"

        # Private attributes
        self.__assets = assets
        self.__layout = layout
        self.__maze = maze
        self.__initial_game_state = initial_game_state
        self.__players = players
        self.__team_colors = team_colors
        self.__decor = decor
        self.__render_simplified = render_simplified
        self.__cheese_image = None
        self.__cheese_eaten_image = None
        self.__cheese_missing_image = None
        self.__cheese_positions = {}
        self.__player_images = {}
        self.__score_locations = {}
        self.__medal_locations = {}

        # Public attributes
        # Giving the background the format of the window avoids a conversion at every image
        self.background = pygame.Surface((layout.window_width, layout.window_height)).convert()
        self.player_trace_colors = dict(trace_colors) if trace_colors is not None else {}

        # Build everything
        self.background.fill(layout_module.BACKGROUND_COLOR)
        self.__build_maze()
        self.__build_flags()
        self.__build_cheese()
        self.__build_players()
        self.__build_scores_area()

        # Drawing an image with transparency into the background also copies its transparency
        # The background is what the window shows below everything else, so it must be fully opaque
        # Without this, the parts of the window covered by an image would let the desktop show through on some systems
        self.background.fill((0, 0, 0, 255), special_flags=pygame.BLEND_RGBA_MAX)

    ##################################################################################
    #                                 PUBLIC METHODS                                 #
    ##################################################################################

    def draw_background ( self,
                          screen: pygame.Surface
                        ) ->      None:

        """
        Draws everything that never changes during the game.

        Args:
            screen: Surface to draw on.
        """

        # A single copy replaces drawing every element of the maze again
        screen.blit(self.background, (0, 0))

    ##################################################################################

    def draw_maze ( self,
                    screen:              pygame.Surface,
                    cheese:              list[int],
                    player_positions:    dict[str, tuple[float, float]],
                    player_orientations: dict[str, Action],
                    traces:              dict[str, list[int]],
                    trace_length:        int
                  ) ->                   None:

        """
        Draws one image of the maze, with the pieces of cheese, the traces and the players at the given positions.

        Args:
            screen:              Surface to draw on.
            cheese:              Cells that still contain a piece of cheese.
            player_positions:    Position of the image of each player, in pixels.
            player_orientations: Direction each player faces, as the action it performs.
            traces:              Cells recently visited by each player, the oldest first.
            trace_length:        Number of segments of trace to draw.
        """

        # Restore the part of the background hidden by the previous image
        maze_rect = pygame.Rect(self.__layout.maze_area())
        screen.blit(self.background, maze_rect, maze_rect)

        # Pieces of cheese that are still there
        for c in cheese:
            screen.blit(self.__cheese_image, self.__cheese_positions[c])

        # Traces of where the players come from, below all the players
        if trace_length > 0:
            for player_name, (player_x, player_y) in player_positions.items():
                image = self.__player_images[player_name][player_orientations[player_name]]
                center = (player_x + image.get_width() / 2, player_y + image.get_height() / 2)
                self.__draw_trace(screen, player_name, center, traces[player_name], trace_length)

        # Players
        for player_name, position in player_positions.items():
            screen.blit(self.__player_images[player_name][player_orientations[player_name]], position)

    ##################################################################################

    def draw_scores ( self,
                      screen:      pygame.Surface,
                      team_scores: dict[str, float]
                    ) ->           None:

        """
        Draws the scores area, with one piece of cheese per point a team can score.

        Args:
            screen:      Surface to draw on.
            team_scores: Score of each team.
        """

        # Restore the background of the area, as scores only grow
        scores_rect = pygame.Rect(self.__layout.scores_area())
        screen.blit(self.background, scores_rect, scores_rect)

        # Eaten, partially eaten and remaining pieces of cheese
        for team, (score_x_offset, score_margin, score_y_offset) in self.__score_locations.items():
            for i in range(int(team_scores[team])):
                screen.blit(self.__cheese_eaten_image, (score_x_offset + i * score_margin, score_y_offset))
            if int(team_scores[team]) != team_scores[team]:
                cheese_partial = self.__assets.image(os.path.join("cheese", "cheese_eaten.png"), self.__layout.cheese_score_size)
                cheese_partial = self.__assets.colorize(cheese_partial, [(team_scores[team] - int(team_scores[team])) * 255] * 3)
                cheese_partial = self.__assets.add_color_border(cheese_partial, layout_module.CHEESE_SCORE_BORDER_COLOR, layout_module.CHEESE_SCORE_BORDER_WIDTH)
                screen.blit(cheese_partial, (score_x_offset + int(team_scores[team]) * score_margin, score_y_offset))
            for j in range(math.ceil(team_scores[team]), len(self.__initial_game_state.cheese)):
                screen.blit(self.__cheese_missing_image, (score_x_offset + j * score_margin, score_y_offset))

    ##################################################################################

    def draw_medals ( self,
                      screen:      pygame.Surface,
                      team_scores: dict[str, float]
                    ) ->           None:

        """
        Draws a medal next to each team, according to its rank at the end of the game.

        Args:
            screen:      Surface to draw on.
            team_scores: Final score of each team.
        """

        # Teams with the same score get the same medal
        sorted_results = sorted([(team_scores[team], team) for team in team_scores], reverse=True)
        medals = [self.__assets.image(os.path.join("endgame", medal_name), self.__layout.medal_size) for medal_name in ["first.png", "second.png", "third.png", "others.png"]]
        for i in range(len(sorted_results)):
            if i > 0 and sorted_results[i][0] != sorted_results[i-1][0] and len(medals) > 1:
                del medals[0]
            team = sorted_results[i][1]
            screen.blit(medals[0], (self.__medal_locations[team][0] - medals[0].get_width() / 2, self.__medal_locations[team][1] - medals[0].get_height() / 3))

    ##################################################################################

    def draw_main_image ( self,
                          screen:     pygame.Surface,
                          image_name: str
                        ) ->          None:

        """
        Draws a large image in the middle of the maze, used to announce the beginning of the game.

        Args:
            screen:     Surface to draw on.
            image_name: Name of the image, in the drawings directory.
        """

        # Centered in the maze
        image = self.__assets.image(os.path.join("drawings", image_name), self.__layout.main_image_size)
        image = self.__assets.add_color_border(image, layout_module.MAIN_IMAGE_BORDER_COLOR, layout_module.MAIN_IMAGE_BORDER_SIZE)
        image_x = self.__layout.maze_x_offset + (self.__layout.game_area_width - image.get_width()) / 2
        image_y = self.__layout.maze_y_offset + (self.__layout.game_area_height - image.get_height()) / 2
        screen.blit(image, (image_x, image_y))

    ##################################################################################

    def player_position ( self,
                          player_name: str,
                          orientation: Action,
                          cell:        int,
                          shift:       tuple[float, float] = (0.0, 0.0)
                        ) ->           tuple[float, float]:

        """
        Returns where to draw a player standing in a cell, possibly shifted towards a neighboring cell.

        Args:
            player_name: Name of the player.
            orientation: Direction the player faces, as the action it performs.
            cell:        Cell in which the player stands.
            shift:       Fraction of a cell by which the player is shifted horizontally and vertically.

        Returns:
            The position of the top left corner of the image of the player, in pixels.
        """

        # Centered in the cell, then shifted
        image = self.__player_images[player_name][orientation]
        position_x, position_y = self.__layout.centered_in_cell(cell, image.get_size())
        return position_x + shift[0] * self.__layout.cell_size, position_y + shift[1] * self.__layout.cell_size

    ##################################################################################
    #                                 PRIVATE METHODS                                #
    ##################################################################################

    def __draw_trace ( self,
                       screen:       pygame.Surface,
                       player_name:  str,
                       center:       tuple[float, float],
                       trace_cells:  list[int],
                       trace_length: int
                     ) ->            None:

        """
        Draws the trace of a player, which fades away as the player moves on.

        Args:
            screen:       Surface to draw on.
            player_name:  Name of the player.
            center:       Current center of the player.
            trace_cells:  Cells recently visited by the player, the oldest first.
            trace_length: Number of segments to draw.
        """

        # Segment between the player and the last visited cell, then the older ones
        trace = [self.__layout.cell_center(cell) for cell in trace_cells]
        color = self.player_trace_colors[player_name]
        size = self.__layout.trace_size
        pygame.draw.line(screen, color, center, trace[-1], width=size)
        for j in range(1, trace_length):
            if len(trace) > j:
                pygame.draw.line(screen, color, trace[-j-1], trace[-j], width=size)

        # The oldest segment is shortened as the player moves away, so that the trace keeps a constant length
        if len(trace) == trace_length + 1:
            final_segment_length = math.dist(trace[-1], center)
            ratio = 1 - final_segment_length / self.__layout.cell_size
            pygame.draw.line(screen, color, trace[1], (trace[1][0] + ratio * (trace[0][0] - trace[1][0]), trace[1][1] + ratio * (trace[0][1] - trace[1][1])), width=size)

    ##################################################################################

    def __build_maze ( self ) -> None:

        """
        Draws the ground, the mud, the numbers of the cells, the walls and the corners into the background.
        """

        # Shortcuts
        maze = self.__maze
        layout = self.__layout
        assets = self.__assets
        cell_size = layout.cell_size

        # Ground
        for (row, col), (tile_name, rotation, flip_x, flip_y) in self.__decor.tiles.items():
            cell = assets.image(tile_name, cell_size, cell_size)
            cell = pygame.transform.rotate(cell, rotation)
            cell = pygame.transform.flip(cell, flip_x, flip_y)
            self.background.blit(cell, layout.cell_position(row, col))

        # Mud, and the number of turns needed to cross it
        mud = assets.image(os.path.join("mud", "mud.png"), cell_size)
        mud_horizontal = pygame.transform.rotate(mud, 90)
        for row in range(maze.get_height()):
            for col in range(maze.get_width()):
                if not maze.rc_exists(row, col):
                    continue
                cell_x, cell_y = layout.cell_position(row, col)
                for neighbor_row, neighbor_col, vertical in [(row, col - 1, True), (row - 1, col, False)]:
                    if not maze.rc_exists(neighbor_row, neighbor_col):
                        continue
                    if not maze.has_edge(maze.rc_to_i(row, col), maze.rc_to_i(neighbor_row, neighbor_col)):
                        continue
                    weight = maze.get_weight(maze.rc_to_i(row, col), maze.rc_to_i(neighbor_row, neighbor_col))
                    if weight <= 1:
                        continue
                    if vertical:
                        self.background.blit(mud, (cell_x - mud.get_width() // 2, cell_y))
                    else:
                        self.background.blit(mud_horizontal, (cell_x, cell_y - mud.get_width() // 2))
                    if not self.__render_simplified:
                        weight_text = assets.text(str(weight), layout.text_size, layout_module.MUD_TEXT_COLOR)
                        if vertical:
                            self.background.blit(weight_text, (cell_x - weight_text.get_width() // 2, cell_y + (cell_size - weight_text.get_height()) // 2))
                        else:
                            self.background.blit(weight_text, (cell_x + (cell_size - weight_text.get_width()) // 2, cell_y - weight_text.get_height() // 2))

        # Number of each cell
        if not self.__render_simplified:
            for row in range(maze.get_height()):
                for col in range(maze.get_width()):
                    if maze.rc_exists(row, col):
                        cell_text = assets.text(str(maze.rc_to_i(row, col)), layout.text_size, layout_module.CELL_TEXT_COLOR)
                        cell_x, cell_y = layout.cell_position(row, col)
                        self.background.blit(cell_text, (cell_x + layout.cell_text_offset, cell_y + layout.cell_text_offset))

        # Walls, between two cells or at the border of the maze
        walls = []
        wall = assets.image(os.path.join("wall", "wall.png"), cell_size)
        wall_horizontal = pygame.transform.rotate(wall, 90)
        for row in range(maze.get_height() + 1):
            for col in range(maze.get_width() + 1):
                cell_x, cell_y = layout.cell_position(row, col)
                if self.__is_wall(row, col, row, col - 1):
                    self.background.blit(wall, (cell_x - wall.get_width() // 2, cell_y))
                    walls.append((row, col, row, col - 1))
                if self.__is_wall(row, col, row - 1, col):
                    self.background.blit(wall_horizontal, (cell_x, cell_y - wall.get_width() // 2))
                    walls.append((row, col, row - 1, col))

        # Corners, where walls meet
        corner = assets.image(os.path.join("wall", "corner.png"), int(wall.get_width() * layout_module.CORNER_WALL_RATIO), int(wall.get_width() * layout_module.CORNER_WALL_RATIO))
        for row, col, neighbor_row, neighbor_col in walls:
            cell_x, cell_y = layout.cell_position(row, col)
            if col != neighbor_col:
                corner_x = cell_x - corner.get_width() // 2
                if (row - 1, col, neighbor_row - 1, neighbor_col) not in walls or ((neighbor_row, neighbor_col, neighbor_row - 1, neighbor_col) in walls and (row, col, row - 1, col) in walls and (row - 1, col, neighbor_row - 1, neighbor_col) in walls):
                    self.background.blit(corner, (corner_x, cell_y - corner.get_width() // 2))
                if (row + 1, col, neighbor_row + 1, neighbor_col) not in walls:
                    self.background.blit(corner, (corner_x, layout.cell_position(row + 1, col)[1] - corner.get_width() // 2))
            if row != neighbor_row:
                corner_y = cell_y - corner.get_width() // 2
                if (row, col - 1, neighbor_row, neighbor_col - 1) not in walls:
                    self.background.blit(corner, (cell_x - corner.get_width() // 2, corner_y))
                if (row, col + 1, neighbor_row, neighbor_col + 1) not in walls:
                    self.background.blit(corner, (layout.cell_position(row, col + 1)[0] - corner.get_width() // 2, corner_y))

    ##################################################################################

    def __is_wall ( self,
                    row:          int,
                    col:          int,
                    neighbor_row: int,
                    neighbor_col: int
                  ) ->            bool:

        """
        Indicates if a wall should be drawn between a cell and one of its neighbors.
        A wall is drawn between two cells that are not connected, and at the border between the maze and the outside.

        Args:
            row:          Row of the cell.
            col:          Column of the cell.
            neighbor_row: Row of the neighbor.
            neighbor_col: Column of the neighbor.

        Returns:
            ``True`` if a wall should be drawn, ``False`` otherwise.
        """

        # Border of the maze
        maze = self.__maze
        cell_exists = maze.rc_exists(row, col)
        neighbor_exists = maze.rc_exists(neighbor_row, neighbor_col)
        if cell_exists != neighbor_exists:
            return True

        # Wall between two existing cells
        return cell_exists and neighbor_exists and not maze.has_edge(maze.rc_to_i(row, col), maze.rc_to_i(neighbor_row, neighbor_col))

    ##################################################################################

    def __build_flags ( self ) -> None:

        """
        Draws into the background a flag per player, at the cell where that player starts.
        """

        # Flags are a detail of the maze
        if self.__render_simplified:
            return

        # Count how many players of each team start on each cell
        layout = self.__layout
        initial_game_state = self.__initial_game_state
        cells_with_flags = {cell: {} for cell in initial_game_state.player_locations.values()}
        for player in self.__players:
            team = [team for team in initial_game_state.teams if player.get_name() in initial_game_state.teams[team]][0]
            cell = initial_game_state.player_locations[player.get_name()]
            cells_with_flags[cell][team] = cells_with_flags[cell].get(team, 0) + 1

        # Flags are spread so that they remain visible when several players start on the same cell
        flag = self.__assets.image(os.path.join("flag", "flag.png"), layout.flag_size)
        max_teams_in_cells = max([len(team) for team in cells_with_flags.values()])
        max_players_in_cells = max([cells_with_flags[cell][team] for cell in cells_with_flags for team in cells_with_flags[cell]])
        for cell in cells_with_flags:
            cell_x, cell_y = layout.cell_position(*self.__maze.i_to_rc(cell))
            for i_team, team in enumerate(cells_with_flags[cell]):
                flag_colored = self.__assets.colorize(flag, self.__team_colors[team])
                flag_colored = self.__assets.add_color_border(flag_colored, layout_module.FLAG_BORDER_COLOR, layout_module.FLAG_BORDER_WIDTH)
                for i_player in range(cells_with_flags[cell][team]):
                    flag_x = cell_x + layout.cell_size - layout.flag_x_offset - i_player * min(layout.flag_x_next_offset, (layout.cell_size - layout.flag_x_offset) / (max_players_in_cells + 1))
                    flag_y = cell_y - flag.get_height() + layout.flag_y_offset + i_team * min(layout.flag_y_offset, (layout.cell_size - layout.flag_y_offset) / (max_teams_in_cells + 1))
                    self.background.blit(flag_colored, (flag_x, flag_y))

    ##################################################################################

    def __build_cheese ( self ) -> None:

        """
        Prepares the image of a piece of cheese, and the position it occupies in each cell.
        """

        # The same image is used for every piece of cheese
        self.__cheese_image = self.__assets.image(os.path.join("cheese", "cheese.png"), self.__layout.cheese_size)
        self.__cheese_image = self.__assets.add_color_border(self.__cheese_image, layout_module.CHEESE_BORDER_COLOR, layout_module.CHEESE_BORDER_WIDTH)
        for c in self.__initial_game_state.cheese:
            self.__cheese_positions[c] = self.__layout.centered_in_cell(c, self.__cheese_image.get_size())

    ##################################################################################

    def __build_players ( self ) -> None:

        """
        Prepares the images of the players, and the color of their traces.
        """

        # One set of images per player, bordered with the color of its team when teams are shown
        layout = self.__layout
        initial_game_state = self.__initial_game_state
        for player in self.__players:
            team = [team for team in initial_game_state.teams if player.get_name() in initial_game_state.teams[team]][0]
            border_color = self.__team_colors[team] if layout.teams_enabled else None
            images = self.__assets.player_images(player.get_skin(), layout.player_size, border_color, layout_module.PLAYER_BORDER_WIDTH)
            self.__player_images[player.get_name()] = images
            if player.get_name() not in self.player_trace_colors:
                self.player_trace_colors[player.get_name()] = self.__assets.main_color(images[Action.NOTHING])

    ##################################################################################

    def __build_scores_area ( self ) -> None:

        """
        Draws into the background the box of each team, with its name and the avatars of its players.
        Also prepares the images of the scores, and computes where the scores and the medals of each team are drawn.
        """

        # Shortcuts
        layout = self.__layout
        assets = self.__assets
        initial_game_state = self.__initial_game_state
        padding = layout.avatars_area_padding

        # Images used to show the scores
        self.__cheese_eaten_image = assets.add_color_border(assets.image(os.path.join("cheese", "cheese_eaten.png"), layout.cheese_score_size), layout_module.CHEESE_SCORE_BORDER_COLOR, layout_module.CHEESE_SCORE_BORDER_WIDTH)
        self.__cheese_missing_image = assets.add_color_border(assets.image(os.path.join("cheese", "cheese_missing.png"), layout.cheese_score_size), layout_module.CHEESE_SCORE_BORDER_COLOR, layout_module.CHEESE_SCORE_BORDER_WIDTH)

        # One box per team
        for i, team in enumerate(initial_game_state.teams):
            team_text_size = layout.team_text_size

            # Box of the team
            team_background = pygame.Surface((layout.avatars_area_width, layout.avatars_area_height))
            pygame.draw.rect(team_background, layout_module.BACKGROUND_COLOR, pygame.Rect(0, 0, layout.avatars_area_width, layout.avatars_area_height))
            pygame.draw.rect(team_background, self.__team_colors[team], pygame.Rect(0, 0, layout.avatars_area_width, layout.avatars_area_height), layout_module.AVATARS_AREA_BORDER, layout_module.AVATARS_AREA_ANGLE)
            team_background_x = layout.avatars_x_offset
            team_background_y = (1 + i) * layout.maze_y_offset + i * layout.avatars_area_height if len(initial_game_state.teams) > 1 else (layout.window_height - layout.avatars_area_height) // 2
            self.background.blit(team_background, (team_background_x, team_background_y))
            self.__medal_locations[team] = (team_background_x + layout.avatars_area_width, team_background_y)

            # Name of the team, shrunk if it does not fit in the box
            team_text = assets.text(team, max(team_text_size, 1), self.__team_colors[team])
            if team_text.get_width() > layout.avatars_area_width - 2 * padding:
                ratio = (layout.avatars_area_width - 2 * padding) / team_text.get_width()
                team_text = pygame.transform.scale(team_text, (int(team_text.get_width() * ratio), int(team_text.get_height() * ratio)))
            if layout.teams_enabled:
                team_text_x = layout.avatars_x_offset + (layout.avatars_area_width - team_text.get_width()) // 2
                team_text_y = team_background_y + padding + (team_text_size - team_text.get_height()) // 2
                self.background.blit(team_text, (team_text_x, team_text_y))
            else:
                team_text_size = -padding

            # Avatars of the players of the team, side by side
            player_avatars = []
            for player_name in initial_game_state.teams[team]:
                player = [player for player in self.__players if player.get_name() == player_name][0]
                player_avatars.append(assets.player_avatar(player.get_skin(), layout.player_avatar_size))
            avatar_area = pygame.Surface((2 * padding + sum([avatar.get_width() for avatar in player_avatars]) + layout.player_avatar_horizontal_padding * (len(player_avatars) - 1), layout.player_avatar_size))
            pygame.draw.rect(avatar_area, layout_module.BACKGROUND_COLOR, pygame.Rect(0, 0, avatar_area.get_width(), avatar_area.get_height()))
            player_x = padding
            centers = []
            for player_avatar in player_avatars:
                avatar_area.blit(player_avatar, (player_x, 0))
                centers.append(player_x + player_avatar.get_width() // 2)
                player_x += player_avatar.get_width() + layout.player_avatar_horizontal_padding
            if avatar_area.get_width() > layout.avatars_area_width - 2 * padding:
                ratio = (layout.avatars_area_width - 2 * padding) / avatar_area.get_width()
                centers = [center * ratio for center in centers]
                avatar_area = pygame.transform.scale(avatar_area, (int(avatar_area.get_width() * ratio), int(avatar_area.get_height() * ratio)))
            avatar_area_x = layout.avatars_x_offset + (layout.avatars_area_width - avatar_area.get_width()) // 2
            avatar_area_y = team_background_y + 2 * padding + team_text_size + (layout.player_avatar_size - avatar_area.get_height()) // 2
            self.background.blit(avatar_area, (avatar_area_x, avatar_area_y))

            # Name of each player, shortened until it fits under its avatar
            for j, player_name in enumerate(initial_game_state.teams[team]):
                while True:
                    player_name_text = assets.text(player_name, layout.player_name_text_size, layout_module.AVATARS_AREA_COLOR)
                    if player_name_text.get_width() > (layout.avatars_area_width - 2 * padding) / len(initial_game_state.teams[team]) and len(player_name) > 2:
                        player_name = player_name[:-2] + "."
                    else:
                        break
                player_name_text_x = avatar_area_x + centers[j] - player_name_text.get_width() // 2
                player_name_text_y = team_background_y + 3 * padding + team_text_size + layout.player_avatar_size + (layout.player_name_text_size - player_name_text.get_height()) // 2
                self.background.blit(player_name_text, (player_name_text_x, player_name_text_y))

            # Where the pieces of cheese of the score are drawn
            cheese_width = self.__cheese_missing_image.get_width()
            score_x_offset = layout.avatars_x_offset + padding
            score_margin = layout.avatars_area_width - 2 * padding - cheese_width
            if len(initial_game_state.cheese) > 1:
                score_margin /= (len(initial_game_state.cheese) - 1)
            score_margin = min(score_margin, cheese_width * 2)
            estimated_width = cheese_width + (len(initial_game_state.cheese) - 1) * score_margin
            if estimated_width < layout.avatars_area_width - 2 * padding:
                score_x_offset += (layout.avatars_area_width - 2 * padding - estimated_width) / 2
            score_y_offset = team_background_y + 4 * padding + team_text_size + layout.player_avatar_size + layout.player_name_text_size
            self.__score_locations[team] = (score_x_offset, score_margin, score_y_offset)

##########################################################################################
##########################################################################################
