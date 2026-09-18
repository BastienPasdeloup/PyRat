##########################################################################################
########################################## INFO ##########################################
##########################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# It is internal to the library, and nothing in it is meant to be imported by PyRat programs.

"""
This module paces the animations of the graphical interface.

A move is described by a duration rather than by a number of images.
The interface then draws as many images as the machine can afford during that duration, and no more than the screen can show.
This way, a move always lasts the same time, whatever the machine, the operating system, the maze and the size of the window.
On a machine that cannot keep up, images are skipped instead of the animation taking longer.
"""

##########################################################################################
######################################### IMPORTS ########################################
##########################################################################################

# External imports
import time
from collections.abc import Iterator

##########################################################################################
######################################## FUNCTIONS #######################################
##########################################################################################

def animation_frames ( duration: float,
                       fps:      int
                     ) ->        Iterator[tuple[float, bool]]:

    """
    Paces the images of an animation, and describes how far the animation has progressed.

    The images are due at fixed instants, computed once when the animation starts.
    An image that is already late is skipped, except the last one, which always happens, as it is the one that shows the final positions.

    Args:
        duration: Duration of the whole animation, in seconds.
        fps:      Maximum number of images to draw per second.

    Yields:
        The progress of the animation, between 0 (excluded) and 1 (included), and whether this is the last image.
    """

    # Debug
    assert isinstance(duration, float), "Argument 'duration' must be a real number"
    assert isinstance(fps, int), "Argument 'fps' must be an integer"
    assert duration >= 0.0, "Argument 'duration' must be non-negative"
    assert fps > 0, "Argument 'fps' must be positive"

    # Drawing more images than the screen shows would only waste computation
    nb_frames = max(round(duration * fps), 1)
    start_time = time.perf_counter()

    # Draw the images, waiting for the instant each of them is due
    for i in range(nb_frames):
        is_last_frame = i == nb_frames - 1
        frame_time = start_time + (i + 1) * duration / nb_frames
        if not is_last_frame and time.perf_counter() > frame_time:
            continue
        yield (i + 1) / nb_frames, is_last_frame
        remaining_time = frame_time - time.perf_counter()
        if remaining_time > 0.0:
            time.sleep(remaining_time)

##########################################################################################
##########################################################################################
