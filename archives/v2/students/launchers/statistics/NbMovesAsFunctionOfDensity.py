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
#    This script studies the mean number of moves required to get a piece of cheese as a function of density      #    Ce script étudie le nombre moyen de mouvements pour avoir un morceau de fromage en fonction de la densité   #
#    Here, we study a 15x15 maze with no mud and a single piece of cheese in its center                           #    Ici, on étudie un labyrinthe sans boue de taille 15x15 avec un unique morceau de fromage en son centre      #
#    The tests are performed for each file given in the command line arguments                                    #    Les tests sont effectués pour chaque fichier dans les arguments de la ligne de commande                     #
#    Command line: {thisScript} <playerFileName>+                                                                 #    Ligne de commande : {thisScript} <playerFileName>+                                                          #
#                                                                                                                 #                                                                                                                #
####################################################################################################################################################################################################################################
#                                                                                                                 #                                                                                                                #
#    <playerFileName>+ : string                                                                                   #    <playerFileName>+ : string                                                                                  #
#    -------------------------                                                                                    #    -------------------------                                                                                   #
#                                                                                                                 #                                                                                                                #
#        Paths to the players' AI files                                                                           #        Chemins vers les fichiers d'IA des joueurs                                                              #
#        These files must be derivated from the Template.py file                                                  #        Ces fichiers doiventt être des dérivés du fichier Template.py                                           #
#                                                                                                                 #                                                                                                                #
####################################################################################################################################################################################################################################

# Imports
import LaunchersLibrary
import matplotlib.pyplot
import sys

# Command line verification
if len(sys.argv) < 2 :
    print("[ERROR] Wrong arguments count (usage: " + sys.argv[0] + " <playerFileName>+)")
    exit()
PLAYERS_FILE_NAMES = sys.argv[1:]

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
#    MAZE_DENSITIES : float list                                                                                  #    MAZE_DENSITIES : float list                                                                                 #
#    ---------------------------                                                                                  #    ---------------------------                                                                                 #
#                                                                                                                 #                                                                                                                #
#        Densities of walls in the maze to study                                                                  #        Densités de murs dans le labyrinthe à tester                                                            #
#        These are floats in [0, 1], with 0 meaning no walls and 1 meaning as many walls as possible              #        Ce sont des réels dans [0, 1], avec 0 signifiant aucun mur, et 1 signifiant autant de murs que possible #
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
#        If the maze has an even number of cells and is symmetric, then NB_PIECES_OF_CHEESE must be odd           #        Si le labyrinthe a un nombre pair de cases et est symétrique, NB_PIECES_OF_CHEESE doit être pair        #
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
#    NB_TESTS : int                                                                                               #    NB_TESTS : int                                                                                              #
#    --------------                                                                                               #    --------------                                                                                              #
#                                                                                                                 #                                                                                                                #
#        Number of tests to perform per density value                                                             #        Nombre de tests à effectuer par valeur de densité étudiée                                               #
#                                                                                                                 #                                                                                                                #
####################################################################################################################################################################################################################################

# Maze configuration
MAZE_WIDTH = 15
MAZE_HEIGHT = 15
MAZE_DENSITIES = [x * 0.1 for x in range(11)]
MUD_PROBABILITY = 0.0
MAZE_SYMMETRIC = True
NB_PIECES_OF_CHEESE = 1

# Time configuration
TIMING_INFORMATION = "synchronous"
TIMEOUT = None

# Other useful constants
SHOW_GUI_AND_SHELLS = False
OUTPUT_DIRECTORY = "./savedGames/previousGame/"
NB_TESTS = 100

####################################################################################################################################################################################################################################
############################################################################################################## SCRIPT ##############################################################################################################
####################################################################################################################################################################################################################################

# We perform tests for all given AIs for all values of the varying parameter
meanResultsPerFile = {fileName:[] for fileName in PLAYERS_FILE_NAMES}
for density in MAZE_DENSITIES :
    for fileName in PLAYERS_FILE_NAMES :
        meanResults = 0.0
        for test in range(NB_TESTS) :
            print(fileName + " -- Density " + str(density)[:3] + " -- Test " + str(test + 1) + "/" + str(NB_TESTS))
            gameInfo = LaunchersLibrary.startRandomGame(MAZE_WIDTH, MAZE_HEIGHT, density, MUD_PROBABILITY, MAZE_SYMMETRIC, NB_PIECES_OF_CHEESE, TIMING_INFORMATION, SHOW_GUI_AND_SHELLS, OUTPUT_DIRECTORY, TIMEOUT, fileName)
            if gameInfo == {} :
                print("An error occurred during the game")
                exit()
            meanResults += gameInfo["player1"]["totalNbMoves"] / NB_TESTS
        meanResultsPerFile[fileName].append(meanResults)

# We plot the result
for fileName in PLAYERS_FILE_NAMES :
    matplotlib.pyplot.plot(MAZE_DENSITIES, meanResultsPerFile[fileName])
matplotlib.pyplot.xlabel("Maze density")
matplotlib.pyplot.ylabel("Mean number of moves")
matplotlib.pyplot.legend(PLAYERS_FILE_NAMES)
matplotlib.pyplot.show()

####################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################