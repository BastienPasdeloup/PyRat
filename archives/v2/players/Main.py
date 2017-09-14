#!/usr/bin/env python3
# -*- coding: utf-8 -*-
####################################################################################################################################################################################################################################
############################################################################################################## LICENSE #############################################################################################################
####################################################################################################################################################################################################################################
#
#    Copyright © 2016 Bastien Pasdeloup (name.surname@gmail.com) and Télécom Bretagne
#
#    This file is part of PyRat.
#
#    PyRat is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    PyRat is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with PyRat.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################################################################################################################################################
############################################################################################################## IMPORTS #############################################################################################################
####################################################################################################################################################################################################################################

### EXTERNAL ###
import importlib.util
import inspect
import traceback

### INTERNAL ###
import ArgumentsParser
import PyRatProgram
import Shell
import TypeConverter

####################################################################################################################################################################################################################################
############################################################################################################ ENTRY POINT ###########################################################################################################
####################################################################################################################################################################################################################################

### DOCUMENTATION ###
# Entry point of the program
# Imports what is written by the player to hide all the PyRat machinery
# The shell is started as soon as possible to display all errors
# If an error occurs before the player number is received, the shell will be non-personalized when displaying it

### CODE ###
if __name__ == "__main__" :
    
    # We start the shell (will reroute the prints) as soon as possible
    shell = Shell.Shell()
    shell.start()
    
    # We execute the program in a try/except to capture the exceptions and print them to the shell
    program = None
    try :
        
        # We customize the shell using the command line arguments
        parser = ArgumentsParser.ArgumentsParser()
        arguments = parser.argumentsToMap(["-number", "-fileName", "-closeAtEnd"], [])
        converter = TypeConverter.TypeConverter()
        closeAtEnd = converter.toBoolean(arguments["-closeAtEnd"])
        if closeAtEnd :
            shell.forceCloseAtEnd()
        playerNumber = converter.toPlayerNumber(arguments["-number"])
        fileName = converter.toPath(arguments["-fileName"])
        shell.customize(fileName, playerNumber)
        
        # We import the file given as an argument and check if it is a valid PyRat file
        spec = importlib.util.spec_from_file_location("module.name", fileName)
        PlayerFile = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(PlayerFile)
        for pyRatElement in ["TEAM_NAME", "MOVE_DOWN", "MOVE_LEFT", "MOVE_RIGHT", "MOVE_UP", "preprocessing", "turn"] :
            if pyRatElement not in dir(PlayerFile) :
                raise Exception("Invalid PyRat file given: \"" + pyRatElement + "\" is missing")
        for pyRatFunction, expectedNbArguments in [(PlayerFile.preprocessing, 7), (PlayerFile.turn, 9)] :
            if len(inspect.getfullargspec(pyRatFunction).args) != expectedNbArguments :
                raise Exception("Invalid number of arguments for \"" + pyRatFunction.__name__ + "\" method")
        
        # We start the program if the given file didn't cause errors
        program = PyRatProgram.PyRatProgram()
        program.start(PlayerFile.TEAM_NAME, PlayerFile.preprocessing, PlayerFile.turn)
        
        # Once everything is finished, we stop
        shell.stop(False)
        
    # We close the GUI at the end
    except Exception as e :
        shell.write("<b><font color=\"red\">[ERROR]</font></b> " + str(e))
        traceback.print_exc()
        if program :
            program.disconnect()
        shell.stop(True)

####################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################