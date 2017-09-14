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
import ast
import os
import random
import selenium.webdriver
import signal
import subprocess
import sys
import threading
import time
import uuid

####################################################################################################################################################################################################################################
############################################################################################################# CONSTANTS ############################################################################################################
####################################################################################################################################################################################################################################

### DOCUMENTATION ###
# Connection information for the GUI to work properly
# The port must be a valid integer in [1024, 65535]
# The IP address must correspond to where the GUI program runs

### CODE ###
GUI_IP = "127.0.0.1"
GUI_PORT = 12345

####################################################################################################################################################################################################################################

### DOCUMENTATION ###
# Connection information for the first player's program to work properly
# The port must be a valid integer in [1024, 65535]
# The server IP address must correspond to where the PyRat core runs

### CODE ###
PLAYER_1_IP = "127.0.0.1"
PLAYER_1_PORT = 23456

####################################################################################################################################################################################################################################

### DOCUMENTATION ###
# Connection information for the second player's program to work properly
# The port must be a valid integer in [1024, 65535]
# The server IP address must correspond to where the PyRat core runs

### CODE ###
PLAYER_2_IP = "127.0.0.1"
PLAYER_2_PORT = 34567

####################################################################################################################################################################################################################################
############################################################################################################# FUNCTIONS ############################################################################################################
####################################################################################################################################################################################################################################

### DOCUMENTATION ###
# Starts the PyRat core program with a random maze
# Unless you know what you are doing, do not call this function

### CODE ###
def startRandomCore (mazeWidth, mazeHeight, mazeDensity, mudProbability, mazeSymmetric, nbPiecesOfCheese, timingInformation, showGuiAndShells, twoPlayers, outputDirectory, gameID) :
    
    # Core command line
    commandLine = ["pyrat_core",
                   "-ip1", str(PLAYER_1_IP),
                   "-port1", str(PLAYER_1_PORT),
                   "-mazeWidth", str(mazeWidth),
                   "-mazeHeight", str(mazeHeight),
                   "-mazeDensity", str(mazeDensity),
                   "-mudProbability", str(mudProbability),
                   "-mazeSymmetric", str(mazeSymmetric),
                   "-outputDirectory", str(outputDirectory),
                   "-gameID", str(gameID),
                   "-nbPiecesOfCheese", str(nbPiecesOfCheese),
                   "-closeAtEnd", str(not showGuiAndShells)]
    
    # Additional argument to determine synchronicity
    if not isinstance(timingInformation, str) :
        commandLine += ["-preprocessingTime", str(timingInformation[0]),
                        "-turnTime", str(timingInformation[1])]
    else :
        commandLine += ["-synchronicity", str(timingInformation)]
    
    # Additional arguments if the GUI is shown
    if showGuiAndShells :
        commandLine += ["-ipGUI", str(GUI_IP),
                        "-portGUI", str(GUI_PORT)]
    
    # Additional arguments if there are two players
    if twoPlayers :
        commandLine += ["-ip2", str(PLAYER_2_IP),
                        "-port2", str(PLAYER_2_PORT)]
    
    # We execute the command
    process = subprocess.Popen(commandLine, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # We return the stop and poll functions
    return (process.terminate, process.poll)

####################################################################################################################################################################################################################################

### DOCUMENTATION ###
# Starts the PyRat core program from a file
# Unless you know what you are doing, do not call this function

### CODE ###
def startCustomCore (mazeFileName, timingInformation, showGuiAndShells, twoPlayers, outputDirectory, gameID) :
    
    # Core command line
    commandLine = ["pyrat_core",
                   "-ip1", str(PLAYER_1_IP),
                   "-port1", str(PLAYER_1_PORT),
                   "-mazeFileName", str(mazeFileName),
                   "-outputDirectory", str(outputDirectory),
                   "-gameID", str(gameID),
                   "-closeAtEnd", str(not showGuiAndShells)]
    
    # Additional argument to determine synchronicity
    if not isinstance(timingInformation, str) :
        commandLine += ["-preprocessingTime", str(timingInformation[0]),
                        "-turnTime", str(timingInformation[1])]
    else :
        commandLine += ["-synchronicity", str(timingInformation)]
    
    # Additional arguments if the GUI is shown
    if showGuiAndShells :
        commandLine += ["-ipGUI", str(GUI_IP),
                        "-portGUI", str(GUI_PORT)]
    
    # Additional arguments if there are two players
    if twoPlayers :
        commandLine += ["-ip2", str(PLAYER_2_IP),
                        "-port2", str(PLAYER_2_PORT)]
    
    # We execute the command
    process = subprocess.Popen(commandLine, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # We return the stop and poll functions
    return (process.terminate, process.poll)

####################################################################################################################################################################################################################################

### DOCUMENTATION ###
# Starts the PyRat GUI program
# Unless you know what you are doing, do not call this function

### CODE ###
def startGUI () :
    
    # GUI web server address and arguments
    address = "http://" + str(GUI_IP) + "/pyrat/index.php" \
            + "?address=" + str(GUI_IP) \
            + "&port=" + str(GUI_PORT)
    
    # We start a browser at this address
    try :
        browser = selenium.webdriver.Chrome()
        browser.maximize_window()
        browser.get(address)
    except :
        pass
    
    # Function to stop the program
    def stop () :
        try :
            browser.close()
        except :
            pass
    
    # function to poll the program
    def poll () :
        try :
            browser.find_element_by_id("pyrat")
            return None
        except :
            return 0
            
    # We return the stop and poll functions
    return (stop, poll)

####################################################################################################################################################################################################################################

### DOCUMENTATION ###
# Starts the PyRat player manager
# Unless you know what you are doing, do not call this function

### CODE ###
def startPlayer (number, fileName, showGuiAndShells) :

    # Player manager command line
    commandLine = ["pyrat_player",
                   "-fileName", str(fileName),
                   "-ip", str(PLAYER_1_IP if number == 1 else PLAYER_2_IP),
                   "-port", str(PLAYER_1_PORT if number == 1 else PLAYER_2_PORT),
                   "-closeAtEnd", str(not showGuiAndShells),
                   "-number", str(number)]
    
    # We execute the command
    process = subprocess.Popen(commandLine, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # We return the stop and poll functions
    return (process.terminate, process.poll)

####################################################################################################################################################################################################################################

### DOCUMENTATION ###
# Starts a game with the given elements
# Unless you know what you are doing, do not call this function

### CODE ###
def startGame (coreFunctions, guiFunctions, player1Functions, player2Functions, outputDirectory, timeout, gameID) :
    
    # Corresponding lists of existing functions
    stopFunctions = [elementFunctions[0] for elementFunctions in [guiFunctions, coreFunctions, player1Functions, player2Functions] if elementFunctions[0]]
    pollFunctions = [elementFunctions[1] for elementFunctions in [guiFunctions, coreFunctions, player1Functions, player2Functions] if elementFunctions[1]]
    
    # We capture the CTRL+C command to stop everything on request
    def sigintCallback (signal=None, frame=None) :
        [stopFunction() for stopFunction in stopFunctions]
    signal.signal(signal.SIGINT, sigintCallback)
    print("Press CTRL+C to abort execution")
    
    # We stop everything if we reach a defined timeout
    def timeoutCallback (signal=None, frame=None) :
        print("Timeout reached")
        [stopFunction() for stopFunction in stopFunctions[1:]]
    timer = threading.Timer(timeout, timeoutCallback)
    if timeout :
        timer.start()
    
    # We wait until everything is closed
    while any([pollFunction() is None for pollFunction in pollFunctions]) :
        time.sleep(0.01)
    timer.cancel()
    
    # We return the contents of the output file if it was created
    resultsFileName = outputDirectory + "/results.txt"
    if os.path.isfile(resultsFileName) :
        with open(resultsFileName, "r") as results :
            fileContents = ast.literal_eval(results.read())
        if fileContents["gameID"] == gameID :
            return fileContents
    
    # If the game didn't end, we return an empty dictionary
    return {}
    
####################################################################################################################################################################################################################################

### DOCUMENTATION ###
# Starts the PyRat elements and performs a game with a random maze

### CODE ###
def startRandomGame (mazeWidth, mazeHeight, mazeDensity, mudProbability, mazeSymmetric, nbPiecesOfCheese, timingInformation, showGuiAndShells, outputDirectory, timeout, player1FileName, player2FileName=None) :
    
    # We create a game ID
    gameID = str(uuid.uuid4())
    
    # We start the various programs
    core = startRandomCore(mazeWidth, mazeHeight, mazeDensity, mudProbability, mazeSymmetric, nbPiecesOfCheese, timingInformation, showGuiAndShells, player2FileName != None, outputDirectory, gameID)
    player1 = startPlayer(1, player1FileName, showGuiAndShells)
    player2 = startPlayer(2, player2FileName, showGuiAndShells) if player2FileName else (None, None)
    gui = startGUI() if showGuiAndShells else (None, None)
    
    # We run the game with them
    return startGame(core, gui, player1, player2, outputDirectory, timeout, gameID)

####################################################################################################################################################################################################################################

### DOCUMENTATION ###
# Starts the PyRat elements and performs a game with a custom maze

### CODE ###
def startCustomGame (mazeFileName, timingInformation, showGuiAndShells, outputDirectory, timeout, player1FileName, player2FileName=None) :
    
    # We create a game ID
    gameID = str(uuid.uuid4())
    
    # We start the various programs
    core = startCustomCore(mazeFileName, timingInformation, showGuiAndShells, player2FileName != None, outputDirectory, gameID)
    player1 = startPlayer(1, player1FileName, showGuiAndShells)
    player2 = startPlayer(2, player2FileName, showGuiAndShells) if player2FileName else (None, None)
    gui = startGUI() if showGuiAndShells else (None, None)
    
    # We run the game with them
    return startGame(core, gui, player1, player2, outputDirectory, timeout, gameID)

####################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################