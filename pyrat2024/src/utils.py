#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This file contains a few functions that can be useful in general.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External typing imports
from typing import *
from typing_extensions import *
from numbers import *

# Other external imports
import os
import shutil
import inspect

#####################################################################################################################################################
##################################################################### FUNCTIONS #####################################################################
#####################################################################################################################################################

def create_workspace () -> None:

    """
        Creates all the directories for a clean student workspace.
        Also creates a few default programs to start with.
        In:
            * None.
        Out:
            * None.
    """

    # Copy the template workspace into the current directory if not already exixting
    source_workspace = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "workspace")
    shutil.copytree(source_workspace, "pyrat_workspace", ignore=shutil.ignore_patterns('__pycache__'))

#####################################################################################################################################################

def caller_file () -> str:

    """
        Returns the name of the file from which the caller of this function was called.
        In:
            * None.
        Out:
            * caller: The name of the file from which the caller of this function was called.
    """

    # Check stack to get the name
    caller = inspect.currentframe().f_back.f_back.f_code.co_filename
    return caller

#####################################################################################################################################################
#####################################################################################################################################################