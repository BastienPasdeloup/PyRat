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
############################################### SCRIPT DESCRIPTION ############################################################################################# PRÉSENTATION DU SCRIPT ############################################
####################################################################################################################################################################################################################################
#                                                                                                                 #                                                                                                                #
#    This script starts a single player game using a given maze file                                              #    Ce script démarre une partie à un joueur en utilisant un fichier de labyrinthe fourni                       #
#    Command line: {thisScript} <mazeFile> <playerFileName>                                                       #    Ligne de commande : {thisScript} <mazeFile> <playerFileName>                                                #
#                                                                                                                 #                                                                                                                #
####################################################################################################################################################################################################################################
#                                                                                                                 #                                                                                                                #
#    <mazeFile> : string                                                                                          #    <mazeFile> : string                                                                                         #
#    -------------------                                                                                          #    -------------------                                                                                         #
#                                                                                                                 #                                                                                                                #
#        Path to the file describing the maze                                                                     #        Chemin vers le fichier décrivant le labyrinthe                                                          #
#                                                                                                                 #                                                                                                                #
####################################################################################################################################################################################################################################

# Imports
import LaunchersLibrary
import sys

# Command line verification
if len(sys.argv) != 3 :
    print("[ERROR] Wrong arguments count (usage: " + sys.argv[0] + " <mazeFile> <playerFileName>)")
    exit()
MAZE_FILE_NAME = sys.argv[1]
PLAYER_FILE_NAME = sys.argv[2]

####################################################################################################################################################################################################################################
################################################### CONSTANTS ######################################################################################################## CONSTANTES ##################################################
####################################################################################################################################################################################################################################
#                                                                                                                 #                                                                                                                #
#    Useful constants for the script                                                                              #    Constantes utiles pour le script                                                                            #
#                                                                                                                 #                                                                                                                #
####################################################################################################################################################################################################################################
#                                                                                                                 #                                                                                                                #
#    TIMING_INFORMATION : floats pair | string                                                                    #    TIMING_INFORMATION : floats pair | string                                                                   #
#    -----------------------------------------                                                                    #    -----------------------------------------                                                                   #
#                                                                                                                 #                                                                                                                #
#        First entry is the number of seconds allocated to the "preprocessing" function                           #        La première case est le nombre de secondes allouées à la fonction "preprocessing"                       #
#        Second entry is the number of seconds allocated to the "turn" function                                   #        La seconde case est le nombre de secondes allouées à la fonction "turn"                                 #
#        Instead of a pair, this parameter can be a string                                                        #        Au lieu d'une paire, ce paramètre peut être une chaîne                                                  #
#        In that case, it denotes a synchronous game defined as follows:                                          #        Dans ce cas, il représente une partie synchrone comme suit :                                            #
#        If it is "synchronous", both players will move simultaneously                                            #        Si c'est "synchronous", les joueurs bougeront simultanément                                             #
#        If it is "semi-synchronous", players will move when a decision is received                               #        Si c'est "semi-synchronous", les joueurs bougeront quand une décision est reçue                         #
#        This latter case differs from asynchronous since it is adapted to human speed                            #        Ce dernier cas diffère du mode asynchrone car adapté à la vitesse d'un humain                           #
#                                                                                                                 #                                                                                                                #
#    TIMEOUT : float                                                                                              #    TIMEOUT : float                                                                                             #
#    ---------------                                                                                              #    ---------------                                                                                             #
#                                                                                                                 #                                                                                                                #
#        Time after which we stop the game anyway                                                                 #        Temps après lequel la partie est arrêtée quoi qu'il arrive                                              #
#        Set this constant to None to disable the timeout                                                         #        Mettez cette constante à None pour désactiver le timeout                                                #
#                                                                                                                 #                                                                                                                #
#    SHOW_GUI_AND_SHELLS : bool                                                                                   #    SHOW_GUI_AND_SHELLS : bool                                                                                  #
#    --------------------------                                                                                   #    --------------------------                                                                                  #
#                                                                                                                 #                                                                                                                #
#        Indicates if the GUI and the shells should appear or not                                                 #        Indique si l'interface graphique et les terminaux doivent apparaître ou pas                             #
#        If not, the shells will still appear in case of an error but will close as soon as possible              #        Si non, les terminaux apparaîtront quand même en cas d'erreur mais se fermeront dès que possible        #
#        Setting it to False is useful for automatic testing of programs                                          #        Mettre cette constante à False est utile pour faire des tests automatiques                              #
#                                                                                                                 #                                                                                                                #
#    OUTPUT_DIRECTORY : string                                                                                    #    OUTPUT_DIRECTORY : string                                                                                   #
#    -------------------------                                                                                    #    -------------------------                                                                                   #
#                                                                                                                 #                                                                                                                #
#        Every game that finishes is exported to this directory, erasing any other previous game there            #        Toute partie qui se termine est exportée dans ce dossier, en écrasant toute partie s'y trouvant         #
#                                                                                                                 #                                                                                                                #
####################################################################################################################################################################################################################################

# Time configuration
TIMING_INFORMATION = (3.0, 0.1)
TIMEOUT = None

# Other useful constants
SHOW_GUI_AND_SHELLS = True
OUTPUT_DIRECTORY = "./savedGames/previousGame/"

####################################################################################################################################################################################################################################
############################################################################################################## SCRIPT ##############################################################################################################
####################################################################################################################################################################################################################################

# We start the game
gameInfo = LaunchersLibrary.startCustomGame(MAZE_FILE_NAME, TIMING_INFORMATION, SHOW_GUI_AND_SHELLS, OUTPUT_DIRECTORY, TIMEOUT, PLAYER_FILE_NAME)

# We print the summary of the game
if gameInfo == {} :
    print("An error occurred during the game")
else :
    print(gameInfo)

####################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################