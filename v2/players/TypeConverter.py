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
import numpy
import os
import socket

####################################################################################################################################################################################################################################
############################################################################################################### CLASS ##############################################################################################################
####################################################################################################################################################################################################################################

class TypeConverter :
    
    ############################################################################################################################################################################################################################
    ######################################################################################################### CONSTANTS ########################################################################################################
    ############################################################################################################################################################################################################################
        
        ### DOCUMENTATION ###
        # Maximum value allowed to be used for a port

        ### CODE ###
        MAX_PORT = 65535
        
    ############################################################################################################################################################################################################################
        
        ### DOCUMENTATION ###
        # Minimum value allowed to be used for a port

        ### CODE ###
        MIN_PORT = 1024
        
    ############################################################################################################################################################################################################################
    ####################################################################################################### CONSTRUCTORS #######################################################################################################
    ############################################################################################################################################################################################################################
        
        ### DOCUMENTATION ###
        # Default constructor
        
        ### CODE ###
        def __init__ (self) :
            
            pass
        
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
        # Checks if the given string is a valid boolean
        
        ### CODE ###
        def toBoolean (self, value) :
            
            # Must be equal to true or false
            if value.lower() == "true" and value.lower() == "false" :
                raise Exception(str(value) + " is not a valid boolean")
            
            # Done
            return value.lower() == "true"
        
    ############################################################################################################################################################################################################################
        
        ### DOCUMENTATION ###
        # Checks if the given string is a valid double greater than the given bound
        
        ### CODE ###
        def toDoubleGreaterThan (self, doubleString, minBound) :
            
            # Must be a double greater or equal to 0
            try :
                value = float(doubleString)
                if value < minBound :
                    raise ValueError
            except ValueError :
                raise Exception(str(doubleString) + " is not a valid double greater than " + str(minBound))
            
            # Done
            return value
        
    ############################################################################################################################################################################################################################
        
        ### DOCUMENTATION ###
        # Checks if the given string is a valid path
        # Returns the string itself if it is the case
        
        ### CODE ###
        def toPath (self, fileName) :
            
            # We check if the string is a valid file name or directory
            if not os.path.exists(fileName) :
                raise Exception(str(fileName) + " is not a valid path")
            
            # Done
            return fileName
        
    ############################################################################################################################################################################################################################
        
        ### DOCUMENTATION ###
        # Checks if the given string is a valid IP address
        # Returns the string itself if it is the case
        
        ### CODE ###
        def toIP (self, ip) :
            
            # We check if the string is a valid IP address
            try :
                socket.inet_aton(ip)
            except socket.error :
                raise Exception(str(ip) + " is not a valid IP address")
            
            # Done
            return ip
        
    ############################################################################################################################################################################################################################
        
        ### DOCUMENTATION ###
        # Converts the given location to an index
        
        ### CODE ###
        def toIndex (self, location, width) :
            
            # Done
            return location[0] * width + location[1]
        
    ############################################################################################################################################################################################################################
        
        ### DOCUMENTATION ###
        # Converts the given list of locations to a numpy array
        
        ### CODE ###
        def toNumpyArray (self, listOfLocations, width) :
            
            # Conversion
            listOfIndices = []
            for location in listOfLocations :
                locationIndex = self.toIndex(location, width)
                listOfIndices.append(locationIndex)
            
            # Done
            return numpy.array(listOfIndices)
        
    ############################################################################################################################################################################################################################
        
        ### DOCUMENTATION ###
        # Converts the given maze map to a numpy adjacency matrix
        
        ### CODE ###
        def toNumpyMatrix (self, mazeMap, width) :
            
            # Conversion
            adjacencyMatrix = numpy.zeros((len(mazeMap.keys()), len(mazeMap.keys())))
            for node in mazeMap :
                nodeIndex = self.toIndex(node, width)
                for neighbor in mazeMap[node] :
                    neighborIndex = self.toIndex(neighbor, width)
                    adjacencyMatrix[nodeIndex][neighborIndex] = mazeMap[node][neighbor]
                    adjacencyMatrix[neighborIndex][nodeIndex] = mazeMap[neighbor][node]
            
            # Done
            return adjacencyMatrix
        
    ############################################################################################################################################################################################################################
        
        ### DOCUMENTATION ###
        # Checks if the given string is a valid player number
        
        ### CODE ###
        def toPlayerNumber (self, number) :
            
            # Must be 1 or 2
            if number == "1" :
                return 1
            elif number == "2" :
                return 2
            else :
                raise Exception(str(number) + " is not a valid player number")
        
    ############################################################################################################################################################################################################################
        
        ### DOCUMENTATION ###
        # Checks if the given string is a valid port
        
        ### CODE ###
        def toPort (self, port) :
            
            # Must be an integer within some bounds
            try :
                value = int(port)
                if value < TypeConverter.MIN_PORT or value > TypeConverter.MAX_PORT :
                    raise ValueError
            except ValueError :
                raise Exception(str(port) + " is not a valid port")
            
            # Done
            return value
        
    ############################################################################################################################################################################################################################
        
        ### DOCUMENTATION ###
        # Converts a string representing a data structure into the actual structure
        # Non-given optional keys will be initialized with a None value
        
        ### CODE ###
        def toStructure (self, message, compulsoryArguments, optionalArguments) :
            
            # Conversion into a structure
            try :
                structure = ast.literal_eval(message)
                if type(structure) is not dict :
                    raise SyntaxError
            except SyntaxError :
                raise Exception(str(message) + " is not a valid structure")
            
            # We check if the compulsory keys appear in the structure
            for key in compulsoryArguments :
                if key not in structure.keys() :
                    raise Exception("Missing element " + key + " in received message")
            
            # Default values for optional arguments
            for key in optionalArguments :
                if key not in structure.keys() :
                    structure[key] = None
            
            # Done
            return structure
        
    ############################################################################################################################################################################################################################
    ############################################################################################################################################################################################################################

####################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################