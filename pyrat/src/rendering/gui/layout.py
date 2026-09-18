##########################################################################################
########################################## INFO ##########################################
##########################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# It is internal to the library, and nothing in it is meant to be imported by PyRat programs.

"""
This module computes the geometry of the graphical interface.
Every size and position used by the interface is derived here from the size of the window and from the dimensions of the maze.
Resizing the window therefore only consists in building a new layout, and rebuilding the images that depend on it.
"""

##########################################################################################
######################################### IMPORTS ########################################
##########################################################################################

# PyRat imports
from pyrat.src.mazes.maze import Maze
from pyrat.src.game.game_state import GameState

##########################################################################################
######################################## CONSTANTS #######################################
##########################################################################################

# Colors of the interface
BACKGROUND_COLOR = (0, 0, 0)
CELL_TEXT_COLOR = (50, 50, 50)
MUD_TEXT_COLOR = (185, 155, 60)
AVATARS_AREA_COLOR = (255, 255, 255)
FLAG_BORDER_COLOR = (255, 255, 255)
CHEESE_BORDER_COLOR = (255, 255, 0)
CHEESE_SCORE_BORDER_COLOR = (100, 100, 100)
MAIN_IMAGE_BORDER_COLOR = (0, 0, 0)

# Sizes that do not depend on the window
FLAG_BORDER_WIDTH = 1
PLAYER_BORDER_WIDTH = 2
CHEESE_BORDER_WIDTH = 1
CHEESE_SCORE_BORDER_WIDTH = 1
AVATARS_AREA_BORDER = 2
AVATARS_AREA_ANGLE = 10
CORNER_WALL_RATIO = 1.2
ICON_SIZE = 50
MAIN_IMAGE_FACTOR = 0.8
MAIN_IMAGE_BORDER_SIZE = 1

# Smallest window the interface accepts, to avoid degenerate layouts when the user shrinks the window
MIN_WINDOW_WIDTH = 480
MIN_WINDOW_HEIGHT = 360

##########################################################################################
######################################## FUNCTIONS #######################################
##########################################################################################

def teams_are_named ( initial_game_state: GameState
                    ) ->                  bool:

    """
    Indicates if the teams should be shown in the interface.
    This is the case when there are several teams, or when the only team has a name.

    Args:
        initial_game_state: State of the game before it starts.

    Returns:
        ``True`` if the teams should be shown, ``False`` otherwise.
    """

    # Debug
    assert isinstance(initial_game_state, GameState), "Argument 'initial_game_state' must be of type 'pyrat.GameState'"

    # A single unnamed team is the case of a game with no notion of team
    teams = list(initial_game_state.teams.keys())
    return len(teams) > 1 or len(teams[0]) > 0

##########################################################################################
######################################### CLASSES ########################################
##########################################################################################

class Layout ():

    """
    Computes all the sizes and positions of the interface for a given window size.
    An instance describes the interface at one size only, and a new one is built when the window is resized.
    """

    ##################################################################################
    #                                   CONSTRUCTOR                                  #
    ##################################################################################

    def __init__ ( self,
                   window_size:        tuple[int, int],
                   maze:               Maze,
                   initial_game_state: GameState
                 ) ->                  None:

        """
        Initializes a new instance of the class.

        Args:
            window_size:        Size of the window, as a width and a height in pixels.
            maze:               Maze of the game.
            initial_game_state: State of the game before it starts.
        """

        # Debug
        assert isinstance(window_size, tuple), "Argument 'window_size' must be a tuple"
        assert isinstance(maze, Maze), "Argument 'maze' must be of type 'pyrat.Maze'"
        assert isinstance(initial_game_state, GameState), "Argument 'initial_game_state' must be of type 'pyrat.GameState'"

        # Private attributes
        self.__maze = maze

        # Size of the window, never smaller than the accepted minimum
        self.window_width = max(int(window_size[0]), MIN_WINDOW_WIDTH)
        self.window_height = max(int(window_size[1]), MIN_WINDOW_HEIGHT)

        # The maze occupies most of the window, the scores area being on its left
        self.cell_size = max(int(min(self.window_width / maze.get_width(), self.window_height / maze.get_height()) * 0.9), 1)
        self.game_area_width = self.cell_size * maze.get_width()
        self.game_area_height = self.cell_size * maze.get_height()
        self.maze_x_offset = int((self.window_width - self.game_area_width) * 0.9)
        self.maze_y_offset = (self.window_height - self.game_area_height) // 2

        # Elements drawn inside a cell
        self.wall_size = max(self.cell_size // 7, 1)
        self.trace_size = max(self.wall_size // 2, 1)
        self.cell_text_offset = int(self.cell_size * 0.1)
        self.text_size = max(int(self.cell_size * 0.17), 1)
        self.cheese_size = max(int(self.cell_size * 0.4), 1)
        self.player_size = max(int(self.cell_size * 0.5), 1)
        self.flag_size = max(int(self.cell_size * 0.4), 1)
        self.flag_x_offset = int(self.cell_size * 0.2)
        self.flag_x_next_offset = int(self.cell_size * 0.07)
        self.flag_y_offset = int(self.cell_size * 0.3)

        # Scores area, on the left of the maze
        nb_teams = len(initial_game_state.teams)
        self.avatars_x_offset = self.window_width - self.maze_x_offset - self.game_area_width
        self.avatars_area_width = self.maze_x_offset - 2 * self.avatars_x_offset
        self.avatars_area_height = min(self.game_area_height // 2, (self.game_area_height - (nb_teams - 1) * self.maze_y_offset) // nb_teams)

        # Teams are named only when there are several of them, which changes how the scores area is filled
        self.teams_enabled = teams_are_named(initial_game_state)
        if self.teams_enabled:
            self.avatars_area_padding = max(self.avatars_area_height // 13, 1)
            self.team_text_size = self.avatars_area_padding * 3
        else:
            self.avatars_area_padding = max(self.avatars_area_height // 12, 1)
            self.team_text_size = 0
            self.avatars_area_height -= self.avatars_area_padding * 3
        self.player_avatar_size = self.avatars_area_padding * 3
        self.player_avatar_horizontal_padding = self.avatars_area_padding * 4
        self.player_name_text_size = self.avatars_area_padding
        self.cheese_score_size = self.avatars_area_padding

        # Images shown over the maze, when the game starts and when it ends
        self.medal_size = max(min(self.avatars_x_offset, self.maze_y_offset) * 2, 1)
        self.main_image_size = max(int(min(self.game_area_width, self.game_area_height) * MAIN_IMAGE_FACTOR), 1)

    ##################################################################################
    #                                 PUBLIC METHODS                                 #
    ##################################################################################

    def cell_position ( self,
                        row: int,
                        col: int
                      ) ->   tuple[int, int]:

        """
        Returns the position of the top left corner of a cell, in the window.
        The cell does not need to exist, which allows locating the borders of the maze.

        Args:
            row: Row of the cell.
            col: Column of the cell.

        Returns:
            The coordinates of the top left corner of the cell.
        """

        # Debug
        assert isinstance(row, int), "Argument 'row' must be an integer"
        assert isinstance(col, int), "Argument 'col' must be an integer"

        # Position in the window
        return self.maze_x_offset + col * self.cell_size, self.maze_y_offset + row * self.cell_size

    ##################################################################################

    def cell_center ( self,
                      cell: int
                    ) ->    tuple[float, float]:

        """
        Returns the position of the center of a cell, in the window.

        Args:
            cell: Index of the cell.

        Returns:
            The coordinates of the center of the cell.
        """

        # Debug
        assert isinstance(cell, int), "Argument 'cell' must be an integer"

        # Half a cell away from the top left corner
        cell_x, cell_y = self.cell_position(*self.__maze.i_to_rc(cell))
        return cell_x + self.cell_size / 2, cell_y + self.cell_size / 2

    ##################################################################################

    def centered_in_cell ( self,
                           cell:       int,
                           image_size: tuple[int, int]
                         ) ->          tuple[int, int]:

        """
        Returns the position at which to draw an image so that it is centered in a cell.

        Args:
            cell:       Index of the cell.
            image_size: Size of the image to draw, as a width and a height.

        Returns:
            The coordinates of the top left corner of the image.
        """

        # Debug
        assert isinstance(cell, int), "Argument 'cell' must be an integer"
        assert isinstance(image_size, tuple), "Argument 'image_size' must be a tuple"

        # Center the image in the cell
        cell_x, cell_y = self.cell_position(*self.__maze.i_to_rc(cell))
        return cell_x + (self.cell_size - image_size[0]) // 2, cell_y + (self.cell_size - image_size[1]) // 2

    ##################################################################################

    def maze_area ( self ) -> tuple[int, int, int, int]:

        """
        Returns the rectangle occupied by the maze in the window.

        Returns:
            The rectangle, as a position and a size.
        """

        # Rectangle of the maze
        return self.maze_x_offset, self.maze_y_offset, self.game_area_width, self.game_area_height

    ##################################################################################

    def scores_area ( self ) -> tuple[int, int, int, int]:

        """
        Returns the rectangle occupied by the scores in the window.

        Returns:
            The rectangle, as a position and a size.
        """

        # Everything on the left of the maze
        return 0, 0, self.maze_x_offset, self.window_height

##########################################################################################
##########################################################################################
