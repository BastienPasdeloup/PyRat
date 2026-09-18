##########################################################################################
########################################## INFO ##########################################
##########################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# It is internal to the library, and nothing in it is meant to be imported by PyRat programs.

"""
This module loads and transforms the images, fonts and sounds used by the graphical interface.
Everything it produces depends on a target size, so it is reloaded when the window is resized.
Results are cached per size, which makes going back to a previous size instantaneous.

Note that the assets themselves (the image and sound files) are stored in the ``pyrat/gui`` directory of the library.
"""

##########################################################################################
######################################### IMPORTS ########################################
##########################################################################################

# External imports
import collections
import glob
import math
import os
import random
import pygame

# PyRat imports
from pyrat.src.game.enums import Action, PlayerSkin

##########################################################################################
######################################## CONSTANTS #######################################
##########################################################################################

# Directory in which the images and sounds of the interface are stored
ASSETS_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", "..", "gui")

# Image of a player shown for each action, in the directory of its skin
PLAYER_IMAGE_NAMES = {Action.NOTHING: "neutral.png",
                      Action.NORTH: "north.png",
                      Action.SOUTH: "south.png",
                      Action.WEST: "west.png",
                      Action.EAST: "east.png"}

##########################################################################################
######################################### CLASSES ########################################
##########################################################################################

class Assets ():

    """
    Loads the images, texts and sounds of the graphical interface, and keeps them in a cache.
    The cache is keyed by the requested size, so rebuilding the interface at a new size reuses what can be reused.
    """

    ##################################################################################
    #                                   CONSTRUCTOR                                  #
    ##################################################################################

    def __init__ ( self,
                   rng: random.Random
                 ) ->   None:

        """
        Initializes a new instance of the class.

        Args:
            rng: Random number generator, used to choose among the available ground tiles.
        """

        # Debug
        assert isinstance(rng, random.Random), "Argument 'rng' must be of type 'random.Random'"

        # Private attributes
        self.__rng = rng
        self.__images = {}
        self.__texts = {}
        self.__sounds = {}

    ##################################################################################
    #                                 PUBLIC METHODS                                 #
    ##################################################################################

    def image ( self,
                file_name:                str,
                target_width_or_max_size: int,
                target_height:            int | None = None
              ) ->                        pygame.Surface:

        """
        Loads an image and scales it.
        If only a size is given, the image is scaled keeping its ratio, the given size being the maximum one.
        Otherwise, the image is scaled to the given width and height.

        Args:
            file_name:                Path of the image, relative to the assets directory.
            target_width_or_max_size: Target width, or maximum size if no height is given.
            target_height:            Target height, or ``None`` to keep the ratio of the image.

        Returns:
            The scaled image.
        """

        # Debug
        assert isinstance(file_name, str), "Argument 'file_name' must be a string"
        assert isinstance(target_width_or_max_size, int), "Argument 'target_width_or_max_size' must be an integer"
        assert isinstance(target_height, (int, type(None))), "Argument 'target_height' must be an integer or None"

        # Reuse the image if it was already loaded at that size
        full_path = os.path.join(ASSETS_DIRECTORY, file_name)
        key = (full_path, target_width_or_max_size, target_height)
        if key not in self.__images:
            surface = pygame.image.load(full_path).convert_alpha()
            if target_height is None:
                max_surface_size = max(surface.get_width(), surface.get_height())
                surface = pygame.transform.scale(surface, (surface.get_width() * target_width_or_max_size // max_surface_size, surface.get_height() * target_width_or_max_size // max_surface_size))
            else:
                surface = pygame.transform.scale(surface, (target_width_or_max_size, target_height))
            self.__images[key] = surface

        # Done
        return self.__images[key]

    ##################################################################################

    def random_image_name ( self,
                            directory_name: str
                          ) ->              str:

        """
        Chooses at random the name of an image among those of a directory.

        Args:
            directory_name: Path of the directory, relative to the assets directory.

        Returns:
            The path of the chosen image, relative to the assets directory.
        """

        # Debug
        assert isinstance(directory_name, str), "Argument 'directory_name' must be a string"

        # Choose among the files of the directory
        full_path = os.path.join(ASSETS_DIRECTORY, directory_name)
        chosen = self.__rng.choice(sorted(glob.glob(os.path.join(full_path, "*"))))
        return os.path.relpath(chosen, ASSETS_DIRECTORY)

    ##################################################################################

    def text ( self,
               text:               str,
               target_height:      int,
               text_color:         tuple[int, int, int],
               original_font_size: int = 50
             ) ->                  pygame.Surface:

        """
        Renders a text, scaled to the given height.

        Args:
            text:               Text to render.
            target_height:      Height of the produced image.
            text_color:         Color of the text.
            original_font_size: Size at which the text is rendered before being scaled.

        Returns:
            The rendered text.
        """

        # Debug
        assert isinstance(text, str), "Argument 'text' must be a string"
        assert isinstance(target_height, int), "Argument 'target_height' must be an integer"
        assert isinstance(original_font_size, int), "Argument 'original_font_size' must be an integer"

        # Render then scale, so that the text always has the expected height
        key = (text, target_height, tuple(text_color), original_font_size)
        if key not in self.__texts:
            surface = pygame.font.SysFont(None, original_font_size).render(text, True, text_color)
            surface = pygame.transform.scale(surface, (max(surface.get_width() * target_height // max(surface.get_height(), 1), 1), max(target_height, 1)))
            self.__texts[key] = surface

        # Done
        return self.__texts[key]

    ##################################################################################

    def colorize ( self,
                   surface: pygame.Surface,
                   color:   tuple[int, int, int]
                 ) ->       pygame.Surface:

        """
        Returns a copy of an image, tinted with the given color.

        Args:
            surface: Image to tint.
            color:   Color to apply.

        Returns:
            The tinted image.
        """

        # Debug
        assert isinstance(surface, pygame.Surface), "Argument 'surface' must be of type 'pygame.Surface'"

        # Multiply the image by a uniform color
        final_surface = surface.copy()
        color_surface = pygame.Surface(final_surface.get_size()).convert_alpha()
        color_surface.fill(color)
        final_surface.blit(color_surface, (0, 0), special_flags=pygame.BLEND_MULT)
        return final_surface

    ##################################################################################

    def add_color_border ( self,
                           surface:       pygame.Surface,
                           border_color:  tuple[int, int, int],
                           border_size:   int,
                           final_rescale: bool = True
                         ) ->             pygame.Surface:

        """
        Returns a copy of an image, surrounded by a colored border that follows its shape.

        Args:
            surface:       Image to surround.
            border_color:  Color of the border.
            border_size:   Thickness of the border.
            final_rescale: If ``True``, the result is scaled back to the size of the original image.

        Returns:
            The image with its border.
        """

        # Debug
        assert isinstance(surface, pygame.Surface), "Argument 'surface' must be of type 'pygame.Surface'"
        assert isinstance(border_size, int), "Argument 'border_size' must be an integer"
        assert isinstance(final_rescale, bool), "Argument 'final_rescale' must be a boolean"

        # The border is the silhouette of the image, drawn in the border color, and repeated around the image
        final_surface = pygame.Surface((surface.get_width() + 2 * border_size, surface.get_height() + 2 * border_size)).convert_alpha()
        final_surface.fill((0, 0, 0, 0))
        mask_surface = surface.copy()
        color_surface = pygame.Surface(mask_surface.get_size())
        color_surface.fill((0, 0, 0, 0))
        mask_surface.blit(color_surface, (0, 0), special_flags=pygame.BLEND_MIN)
        color_surface.fill(border_color)
        mask_surface.blit(color_surface, (0, 0), special_flags=pygame.BLEND_MAX)
        for offset_x in range(-border_size, border_size + 1):
            for offset_y in range(-border_size, border_size + 1):
                if math.dist([0, 0], [offset_x, offset_y]) <= border_size:
                    final_surface.blit(mask_surface, (border_size // 2 + offset_x, border_size // 2 + offset_y))
        final_surface.blit(surface, (border_size // 2, border_size // 2))
        if final_rescale:
            final_surface = pygame.transform.scale(final_surface, surface.get_size())
        return final_surface

    ##################################################################################

    def main_color ( self,
                     surface: pygame.Surface
                   ) ->       tuple[int, int, int, int]:

        """
        Returns the color that appears most in an image, ignoring transparency.
        This is used to draw the trace of a player in the color of its skin.

        Args:
            surface: Image to analyze.

        Returns:
            The dominant color of the image.
        """

        # Debug
        assert isinstance(surface, pygame.Surface), "Argument 'surface' must be of type 'pygame.Surface'"

        # The most frequent color is usually the transparent background, in which case we take the next one
        counts = collections.Counter(pygame.surfarray.array2d(surface).flatten().tolist())
        for mapped_color, _ in counts.most_common(2):
            color = surface.unmap_rgb(mapped_color)
            if color != (0, 0, 0, 0):
                return color
        return color

    ##################################################################################

    def player_images ( self,
                        skin:         PlayerSkin,
                        size:         int,
                        border_color: tuple[int, int, int] | None = None,
                        border_width: int = 0
                      ) ->            dict[Action, pygame.Surface]:

        """
        Loads the images of a player, one per direction it can face.
        A border in the color of its team can be added around the player.

        Args:
            skin:         Skin of the player.
            size:         Size of the produced images.
            border_color: Color of the border to add around the player, or ``None`` for no border.
            border_width: Thickness of that border.

        Returns:
            The image of the player for each action, ``Action.NOTHING`` being the player facing nowhere.
        """

        # Debug
        assert isinstance(skin, PlayerSkin), "Argument 'skin' must be of type 'pyrat.PlayerSkin'"
        assert isinstance(size, int), "Argument 'size' must be an integer"
        assert isinstance(border_width, int), "Argument 'border_width' must be an integer"

        # One image per direction, bordered if asked
        images = {}
        for action, image_name in PLAYER_IMAGE_NAMES.items():
            image = self.image(os.path.join("players", skin.value, image_name), size)
            if border_color is not None:
                image = self.add_color_border(image, border_color, border_width)
            images[action] = image
        return images

    ##################################################################################

    def player_avatar ( self,
                        skin: PlayerSkin,
                        size: int
                      ) ->    pygame.Surface:

        """
        Loads the avatar of a player, shown in the scores area.

        Args:
            skin: Skin of the player.
            size: Size of the produced image.

        Returns:
            The avatar of the player.
        """

        # Debug
        assert isinstance(skin, PlayerSkin), "Argument 'skin' must be of type 'pyrat.PlayerSkin'"
        assert isinstance(size, int), "Argument 'size' must be an integer"

        # The avatar is in the directory of the skin
        return self.image(os.path.join("players", skin.value, "avatar.png"), size)

    ##################################################################################

    def play_sound ( self,
                     file_name: str
                   ) ->         None:

        """
        Plays a sound.
        Sounds are ignored if no audio device is available, so that a game can run on a machine without sound.

        Args:
            file_name: Path of the sound, relative to the assets directory.
        """

        # Debug
        assert isinstance(file_name, str), "Argument 'file_name' must be a string"

        # A missing audio device should not interrupt the game
        sound_file = os.path.join(ASSETS_DIRECTORY, file_name)
        try:
            if sound_file not in self.__sounds:
                self.__sounds[sound_file] = pygame.mixer.Sound(sound_file)
            channel = pygame.mixer.find_channel()
            if channel is not None:
                channel.play(self.__sounds[sound_file])
        except pygame.error:
            pass

##########################################################################################
##########################################################################################
