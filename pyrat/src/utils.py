##########################################################################################
########################################## INFO ##########################################
##########################################################################################

# This file is part of the PyRat library.
# It is meant to be used as a library, and not to be executed directly.
# It is internal to the library, and nothing in it is meant to be imported by PyRat programs.

"""
This module provides small helpers shared by the other modules of the library.
"""

##########################################################################################
######################################### IMPORTS ########################################
##########################################################################################

# External imports
import pathlib
import pyfakefs.fake_filesystem_unittest

##########################################################################################
######################################## FUNCTIONS #######################################
##########################################################################################

def is_valid_directory ( directory: str
                       ) ->         bool:

    """
    Checks if a directory exists or can be created, without actually creating it.
    The check is made in a fake filesystem, so that nothing is written on the disk.

    Args:
        directory: The directory to check.

    Returns:
        ``True`` if the directory can be created, ``False`` otherwise.
    """

    # Debug
    assert isinstance(directory, str), "Argument 'directory' must be a string"

    # Try to create the directory in a fake filesystem
    valid = False
    with pyfakefs.fake_filesystem_unittest.Patcher() as patcher:
        try:
            patcher.fs.makedirs(pathlib.Path(directory), exist_ok=True)
            valid = True
        except Exception:
            pass

    # Done
    return valid

##########################################################################################
##########################################################################################
