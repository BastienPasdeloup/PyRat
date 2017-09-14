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
#    This script starts a 2 players match using a random maze                                                     #    Ce script démarre une partie à 2 joueurs sur un labyrinthe aléatoire                                        #
#    Command line: {thisScript} <player1FileName> <player2FileName>                                               #    Ligne de commande : {thisScript} <player1FileName> <player2FileName>                                        #
#                                                                                                                 #                                                                                                                #
####################################################################################################################################################################################################################################
#                                                                                                                 #                                                                                                                #
#    <player1FileName> : string                                                                                   #    <player1FileName> : string                                                                                  #
#    --------------------------                                                                                   #    --------------------------                                                                                  #
#                                                                                                                 #                                                                                                                #
#        Path to the first player's AI file                                                                       #        Chemin vers le fichier d'AI pour le premier joueur                                                      #
#        This file must be derivated from the Template.py file                                                    #        Ce fichier doit être un dérivé du fichier Template.py                                                   #
#                                                                                                                 #                                                                                                                #
#    <player2FileName> : string                                                                                   #    <player2FileName> : string                                                                                  #
#    --------------------------                                                                                   #    --------------------------                                                                                  #
#                                                                                                                 #                                                                                                                #
#        Path to the second player's AI file                                                                      #        Chemin vers le fichier d'AI pour le second joueur                                                       #
#        This file must be derivated from the Template.py file                                                    #        Ce fichier doit être un dérivé du fichier Template.py                                                   #
#                                                                                                                 #                                                                                                                #
####################################################################################################################################################################################################################################

# Imports
import LaunchersLibrary
import sys

# Command line verification
if len(sys.argv) != 3 :
    print("[ERROR] Wrong arguments count (usage: " + sys.argv[0] + " <player1FileName> <player2FileName>)")
    exit()
PLAYER_1_FILE_NAME = sys.argv[1]
PLAYER_2_FILE_NAME = sys.argv[2]

####################################################################################################################################################################################################################################
################################################### CONSTANTS ######################################################################################################## CONSTANTES ##################################################
####################################################################################################################################################################################################################################
#                                                                                                                 #                                                                                                                #
#    Useful constants for the script                                                                              #    Constantes utiles pour le script                                                                            #
#                                                                                                                 #                                                                                                                #
####################################################################################################################################################################################################################################
#                                                                                                                 #                                                                                                                #
#    MAZE_WIDTH : int    MAZE_HEIGHT : int                                                                        #    MAZE_WIDTH : int    MAZE_HEIGHT : int                                                                       #
#    ----------------    -----------------                                                                        #    ----------------    -----------------                                                                       #
#                                                                                                                 #                                                                                                                #
#        Dimensions of the maze in number of cells                                                                #        Dimensions du labyrinthe en nombre de cases                                                             #
#        Both dimensions must be greater than one                                                                 #        Les deux dimensions doivent être supérieures à 1                                                        #
#                                                                                                                 #                                                                                                                #
#    MAZE_DENSITY : float                                                                                         #    MAZE_DENSITY : float                                                                                        #
#    --------------------                                                                                         #    --------------------                                                                                        #
#                                                                                                                 #                                                                                                                #
#        Density of walls in the maze                                                                             #        Densité de murs dans le labyrinthe                                                                      #
#        This is a float in [0, 1], with 0 meaning no walls and 1 meaning as many walls as possible               #        C'est un réel dans [0, 1], avec 0 signifiant aucun mur, et 1 signifiant autant de murs que possible     #
#        The maze will be connected, whatever its density                                                         #        Quelle que soit la densité, le labyrinthe restera connexe                                               #
#                                                                                                                 #                                                                                                                #
#    MUD_PROBABILITY : float                                                                                      #    MUD_PROBABILITY : float                                                                                     #
#    -----------------------                                                                                      #    -----------------------                                                                                     #
#                                                                                                                 #                                                                                                                #
#        Probability that a path between two cells is covered in mud, thus taking more time to cross              #        Probabilité qu'un chemin entre deux cases soit couvert de boue, prenant donc plus de temps à passer     #
#        This is a float in [0, 1]                                                                                #        C'est un réel dans [0, 1]                                                                               #
#                                                                                                                 #                                                                                                                #
#    MAZE_SYMMETRIC : bool                                                                                        #    MAZE_SYMMETRIC : bool                                                                                       #
#    ---------------------                                                                                        #    ---------------------                                                                                       #
#                                                                                                                 #                                                                                                                #
#        If set to True, the maze will be symetric                                                                #        Si mis à True, le labyrinthe sera symétrique                                                            #
#        In that case, the pieces of cheese will also be symletrically placed                                     #        Dans ce cas, les morceaux de fromage seront aussi placés symétriquement                                 #
#                                                                                                                 #                                                                                                                #
#    NB_PIECES_OF_CHEESE : int                                                                                    #    NB_PIECES_OF_CHEESE : int                                                                                   #
#    -------------------------                                                                                    #    -------------------------                                                                                   #
#                                                                                                                 #                                                                                                                #
#        Number of pieces of cheese in the maze                                                                   #        Nombre de morceaux de fromage dans le labyrinthe                                                        #
#        This number must be lower than MAZE_WIDTH * MAZE_HEIGHT - X, with X the number of players                #        Ce nombre doit être inférieur à MAZE_WIDTH * MAZE_HEIGHT - X, avec X le nombre de joueurs               #
#        If the maze has an even number of cells and is symmetric, then NB_PIECES_OF_CHEESE must be even          #        Si le labyrinthe a un nombre pair de cases et est symétrique, NB_PIECES_OF_CHEESE doit être pair        #
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
#    OUTPUT_DIRECTORY : string                                                                                    #    OUTPUT_DIRECTORY : string                                                                                   #
#    -------------------------                                                                                    #    -------------------------                                                                                   #
#                                                                                                                 #                                                                                                                #
#        Every game that finishes is exported to this directory, erasing any other previous game there            #        Toute partie qui se termine est exportée dans ce dossier, en écrasant toute partie s'y trouvant         #
#        Saved games can be played again using script LoadSavedGame.py                                            #        Les parties sauvegardées peuvent être rejouées en utilisant le script LoadSavedGame.py                  #
#                                                                                                                 #                                                                                                                #
####################################################################################################################################################################################################################################

# Maze configuration
MAZE_WIDTH = 25
MAZE_HEIGHT = 25
MAZE_DENSITY = 0.8
MUD_PROBABILITY = 0.1
MAZE_SYMMETRIC = True
NB_PIECES_OF_CHEESE = 41

# Time configuration
TIMING_INFORMATION = (3.0, 0.1)
TIMEOUT = 60.0

# Other useful constants
SHOW_GUI_AND_SHELLS = True
OUTPUT_DIRECTORY = "./savedGames/previousGame/"

####################################################################################################################################################################################################################################
############################################################################################################## SCRIPT ##############################################################################################################
####################################################################################################################################################################################################################################

# We start the game
gameInfo = LaunchersLibrary.startRandomGame(MAZE_WIDTH, MAZE_HEIGHT, MAZE_DENSITY, MUD_PROBABILITY, MAZE_SYMMETRIC, NB_PIECES_OF_CHEESE, TIMING_INFORMATION, SHOW_GUI_AND_SHELLS, OUTPUT_DIRECTORY, TIMEOUT, PLAYER_1_FILE_NAME, PLAYER_2_FILE_NAME)

# We print the summary of the game
if gameInfo == {} :
    print("An error occurred during the game")
else :
    print(gameInfo)

####################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################