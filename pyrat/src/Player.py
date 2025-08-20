#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# Please import necessary elements using the following syntax:
#     from pyrat import <element_name>

"""
This module provides the base class for players in the PyRat game.
It defines the interface that all players must implement, including important methods ``preprocessing()``, ``turn()``, and ``postprocessing()``.
Players can be implemented as subclasses of this class, and they can use the provided methods to interact with the game state.
The ``turn()`` method is mandatory and must be implemented in the subclasses.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
import abc

# PyRat imports
from pyrat.src.Maze import Maze
from pyrat.src.GameState import GameState
from pyrat.src.enums import Action, PlayerSkin

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class Player (abc.ABC):

    """
        A player is an agent that can play a PyRat game.
        The ``preprocessing()`` method is called once at the beginning of the game.
        The ``turn()`` method is called at each turn of the game.
        The ``postprocessing()`` method is called once at the end of the game.
        Only the ``turn()`` method is mandatory.
        If you want to keep track of some information between turns, you can define a constructor and add attributes to the object.
        Check examples in the provided workspace to see how to do it properly.
    """

    #############################################################################################################################################
    #                                                               MAGIC METHODS                                                               #
    #############################################################################################################################################

    def __init__ ( self,
                   name: str | None = None,
                   skin: PlayerSkin = PlayerSkin.RAT
                 ) ->    None:

        """
        *(This class is abstract and meant to be subclassed, not instantiated directly).*
        
        Initializes a new instance of the class.
        
        Args:
            name: Name of the player (if ``None``, we take the name of the class).
            skin: Skin of the player.
        """

        # Debug
        assert isinstance(name, (str, type(None))), "Argument 'name' must be a string or None (if None, we take the name of the class)"
        assert isinstance(skin, PlayerSkin), "Argument 'skin' must be of type 'pyrat.PlayerSkin'"

        # Private attributes
        self.__name = name if name is not None else self.__class__.__name__
        self.__skin = skin

    #############################################################################################################################################
    #                                                               PUBLIC METHODS                                                              #
    #############################################################################################################################################

    def get_name (self) -> str:
        
        """
        Returns the name of the player.

        Returns:
            Name of the player.
        """

        # Get the attribute
        return self.__name

    #############################################################################################################################################

    def get_skin (self) -> PlayerSkin:
        
        """
        Returns the skin of the player.

        Returns:
            Skin of the player.
        """

        # Get the attribute
        return self.__skin

    #############################################################################################################################################

    def postprocessing ( self,
                         maze:       Maze,
                         game_state: GameState,
                         stats:      dict[str, object],
                       ) ->          None:

        """
        This method is called once at the end of the game.
        It can be used to perform any cleanup that is needed after the game ends.
        It is not timed, and can be used to analyze the completed game, train models, etc.

        Args:
            maze:       An object representing the maze in which the player plays.
            game_state: An object representing the state of the game.
            stats:      A dictionary containing statistics about the game.
        """

        # Debug
        assert isinstance(maze, Maze), "Argument 'maze' must be of type 'pyrat.Maze'"
        assert isinstance(game_state, GameState), "Argument 'game_state' must be of type 'pyrat.GameState'"
        assert isinstance(stats, dict), "Argument 'stats' must be a dictionary"
        assert all(isinstance(key, str) for key in stats.keys()), "All keys of 'stats' must be strings"

        # By default, this method does nothing unless implemented in the child classes
        pass

    #############################################################################################################################################
    
    def preprocessing ( self,
                        maze:       Maze,
                        game_state: GameState
                      ) ->          None:
        
        """
        This method is called once at the beginning of the game.
        It can be used to initialize attributes or to perform any other setup that is needed before the game starts.
        It typically is given more computational resources than the ``turn()`` method.
        Therefore, it is a good place to perform any heavy computations that are needed for the player to function correctly.

        Args:
            maze:       An object representing the maze in which the player plays.
            game_state: An object representing the state of the game.
        """

        # Debug
        assert isinstance(maze, Maze), "Argument 'maze' must be of type 'pyrat.Maze'"
        assert isinstance(game_state, GameState), "Argument 'game_state' must be of type 'pyrat.GameState'"

        # By default, this method does nothing unless implemented in the child classes
        pass

    #############################################################################################################################################

    @abc.abstractmethod
    def turn ( self,
               maze:       Maze,
               game_state: GameState
             ) ->          Action:

        """
        (This method is abstract and must be implemented in the subclasses.)

        This method is called at each turn of the game.
        It returns an action to perform among the possible actions, defined in the ``Action`` enumeration.
        It is generally given less computational resources than the ``preprocessing()`` method.
        Therefore, you should limit the amount of computations you perform in this method to those that require real-time information.

        Args:
            maze:       An object representing the maze in which the player plays.
            game_state: An object representing the state of the game.

        Returns:
            One of the possible action, defined in the ``Action`` enumeration.

        Raises:
            NotImplementedError: If the method is not implemented in the subclass.
        """

        # Debug
        assert isinstance(maze, Maze), "Argument 'maze' must be of type 'pyrat.Maze'"
        assert isinstance(game_state, GameState), "Argument 'game_state' must be of type 'pyrat.GameState'"

        # This method must be implemented in the child classes
        # By default we raise an error
        raise NotImplementedError("This method must be implemented in the child classes.")

#####################################################################################################################################################
#####################################################################################################################################################
