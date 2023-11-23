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
#####################################################################################################################################################