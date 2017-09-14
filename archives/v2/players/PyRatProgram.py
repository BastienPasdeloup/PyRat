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
import time

### INTERNAL ###
import NetworkClient
import TypeConverter

####################################################################################################################################################################################################################################
############################################################################################################### CLASS ##############################################################################################################
####################################################################################################################################################################################################################################

class PyRatProgram (NetworkClient.NetworkClient) :
    
    ############################################################################################################################################################################################################################
    ######################################################################################################### CONSTANTS ########################################################################################################
    ############################################################################################################################################################################################################################
        
        ### DOCUMENTATION ###
        # Set this to False to work with the normal PyRat representation
        # Set this to True to work with numpy representation

        ### CODE ###
        NUMPY_STRUCTURES = False
        
    ############################################################################################################################################################################################################################
    ####################################################################################################### CONSTRUCTORS #######################################################################################################
    ############################################################################################################################################################################################################################
        
        ### DOCUMENTATION ###
        # Default constructor
        
        ### CODE ###
        def __init__ (self) :
            
            # Parent constructor
            super().__init__()
        
    ############################################################################################################################################################################################################################
    ######################################################################################################## DESTRUCTOR ########################################################################################################
    ############################################################################################################################################################################################################################
        
        ### DOCUMENTATION ###
        # Default destructor
        
        ### CODE ###
        def __del__ (self) :
            
            pass
        
    ############################################################################################################################################################################################################################
    ########################################################################################################## METHODS #########################################################################################################
    ############################################################################################################################################################################################################################
        
        ### DOCUMENTATION ###
        # Establishes the connection and interacts with the server
        # The game is in two phases
        # The initialization step is longer and allows some preprocessing
        # The game itself is a sequence of interactions with the server
        
        ### CODE ###
        def start (self, playerName, preprocessingMethod, turnMethod) :
            
            # We connect to the server and send the name to it
            super().establishConnection()
            super().sendMessage(playerName)
            
            # We get the initial information
            configurationString = super().receiveMessage()
            converter = TypeConverter.TypeConverter()
            compulsoryKeys = ["mazeMap", "mazeWidth", "mazeHeight", "playerLocation", "piecesOfCheese", "timeAllowed"]
            optionalKeys = ["opponentLocation"]
            configuration = converter.toStructure(configurationString, compulsoryKeys, optionalKeys)
            mazeMap = configuration["mazeMap"];
            mazeWidth = configuration["mazeWidth"]
            mazeHeight = configuration["mazeHeight"]
            playerLocation = configuration["playerLocation"]
            opponentLocation = configuration["opponentLocation"]
            piecesOfCheese = configuration["piecesOfCheese"]
            timeAllowed = configuration["timeAllowed"]
            
            # Possible conversion to numpy structures
            if self.NUMPY_STRUCTURES :
                mazeMap = converter.toNumpyMatrix(configuration["mazeMap"], mazeWidth)
                playerLocation = converter.toIndex(configuration["playerLocation"], mazeWidth)
                if opponentLocation :
                    opponentLocation = converter.toIndex(configuration["opponentLocation"], mazeWidth)
                piecesOfCheese = converter.toNumpyArray(configuration["piecesOfCheese"], mazeWidth)
            
            # Preprocessing step
            start = time.time()
            preprocessingMethod(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed)
            elapsed = time.time() - start
            super().sendMessage(str(elapsed))
            
            # Main loop
            while True :
                
                # We get the turn information
                configurationString = super().receiveMessage()
                compulsoryKeys = ["playerLocation", "playerScore", "piecesOfCheese"]
                optionalKeys = ["opponentLocation", "opponentScore", "timeAllowed"]
                configuration = converter.toStructure(configurationString, compulsoryKeys, optionalKeys)
                piecesOfCheese = configuration["piecesOfCheese"]
                playerLocation = configuration["playerLocation"]
                playerScore = configuration["playerScore"]
                opponentLocation = configuration["opponentLocation"]
                opponentScore = configuration["opponentScore"]
                timeAllowed = configuration["timeAllowed"]
                
                # Possible conversion to numpy structures
                if self.NUMPY_STRUCTURES :
                    playerLocation = converter.toIndex(configuration["playerLocation"], mazeWidth)
                    if opponentLocation :
                        opponentLocation = converter.toIndex(configuration["opponentLocation"], mazeWidth)
                    piecesOfCheese = converter.toNumpyArray(configuration["piecesOfCheese"], mazeWidth)
                
                # We stop if no more cheese is available
                if len(piecesOfCheese) == 0 :
                    break
                
                # Turn step
                start = time.time()
                move = turnMethod(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed)
                if not move :
                    raise Exception("Turn method should return a move")
                elapsed = time.time() - start
                super().sendMessage(str(move) + str(elapsed))
            
            # Game is over
            if opponentLocation is None :
                print("<b><font color=\"green\">[INFO]</font></b> Congratulations! You got all the cheese!")
            else :
                if playerScore > opponentScore :
                    print("<b><font color=\"green\">[INFO]</font></b> You win the game!")
                elif playerScore < opponentScore :
                    print("<b><font color=\"green\">[INFO]</font></b> You lose the game!")
                else :
                    print("<b><font color=\"green\">[INFO]</font></b> The game is a tie!")
            
    ############################################################################################################################################################################################################################
    ############################################################################################################################################################################################################################

####################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################