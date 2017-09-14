/**********************************************************************************************************************************************************************************************************************************/
/************************************************************************************************************* LICENSE ************************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
//
//    Copyright © 2016 Bastien Pasdeloup (name.surname@gmail.com) and Télécom Bretagne
//
//    This file is part of PyRat.
//
//    PyRat is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.
//
//    PyRat is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with PyRat.  If not, see <http://www.gnu.org/licenses/>.
//
/**********************************************************************************************************************************************************************************************************************************/
/****************************************************************************************************** INCLUDES & NAMESPACES *****************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/

    /** EXTERNAL **/
    #include <fstream>
    #include <regex>
    #include <string>
    
    /** INTERNAL **/
    #include <Moves.cpp>
    #include <NetworkServer.cpp>
    #include <Shell.cpp>
    #include <TypeConverter.cpp>
    
    /** NAMESPACES **/
    using namespace std;

/**********************************************************************************************************************************************************************************************************************************/
/************************************************************************************************************** CLASS *************************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
    
    #ifndef _PLAYER_
    #define _PLAYER_
        
        /** CLASS DEFINITION **/
        class Player : public NetworkServer
        {
            
            /**********************************************************************************************************************************************************************************************************/
            /************************************************************************************************ CONSTANTS ***********************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Name of the file where to export the player's decisions
                // The tag [NUMBER] is replaced by the player's number
                
                /** CODE **/
                private : static constexpr const char* OUTPUT_FILE_NAME = "player[NUMBER].py";
            
            /**********************************************************************************************************************************************************************************************************/
            /*********************************************************************************************** ATTRIBUTES ***********************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Number of moves we lose when crossing mud
                
                /** CODE **/
                private : int _blocked = 0;

            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // History of the moves for the player
                
                /** CODE **/
                private : vector<string> _moves;
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Name of the player
                
                /** CODE **/
                private : string _name = "Did not connect";
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Number of additional moves caused by mud
                
                /** CODE **/
                private : int _nbMudPenalties = 0;
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Indicates if turn information has ever been sent
                
                /** CODE **/
                private : bool _neverSentTurnInformation = true;
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Number of the player
                
                /** CODE **/
                private : int _number;
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Computation time for the player's preprocessing
                
                /** CODE **/
                private : double _preprocessingComputationTime = 0.0;
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Indicates if we should wait for an answer in any case
                
                /** CODE **/
                private : bool _synchronous;
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Current score of the player
                
                /** CODE **/
                private : double _score = 0.0;
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Total computation time for all the player's turns
                
                /** CODE **/
                private : double _turnsComputationTime = 0.0;
                
            /**********************************************************************************************************************************************************************************************************/
            /********************************************************************************************** CONSTRUCTORS **********************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Constructor initializing the player as a network interface
                
                /** CODE **/
                public : Player (string address, int port, int number, bool synchronous) : NetworkServer(address, port), _number(number), _synchronous(synchronous)
                {
                    
                    // Information
                    Shell::getInstance().info("Creating interface to communicate with player " + to_string(number));
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
            /*********************************************************************************************** DESTRUCTOR ***********************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Empty destructor
                
                /** CODE **/
                public : virtual ~Player ()
                {}
                
            /**********************************************************************************************************************************************************************************************************/
            /************************************************************************************************* METHODS ************************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Blocks the player in mud for some time
                
                /** CODE **/
                public : void block (int duration)
                {
                    
                    // We cross mud
                    _blocked = duration;
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Cancels the previous move if it is a missed move
                // Useful for semi-synchronous games
                
                /** CODE **/
                public : void cancelMissedMove ()
                {
                    
                    // We remove the last move received if it is missed
                    if (_moves.back() == MOVE_MISSED)
                        _moves.pop_back();
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Checks if player is still in preprocessing step
                
                /** CODE **/
                public : void checkIfPreprocessing ()
                {
                    
                    // If we have already exited preprocessing, we do nothing
                    if (_preprocessingComputationTime == 0.0)
                    {
                    
                        // We read the socket for the computation time in blocking or non-blocking mode depending on if the game is synchronous
                        string message = NetworkObject::receiveMessage(_synchronous);
                        if (message.length() > 0)
                        {
                            TypeConverter converter;
                            double time = converter.toDouble(message);
                            _preprocessingComputationTime = time;
                            Shell::getInstance().info("Player " + to_string(_number) + " finished preprocessing in " + message + "s");
                        }
                    }
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Adds points to the player
                
                /** CODE **/
                public : void eatCheese (double portion)
                {
                    
                    // We increase the score
                    _score += portion;
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Connects to the player file
                
                /** CODE **/
                public : void establishConnection ()
                {
                    
                    // We overload the method to add a message
                    NetworkServer::establishConnection();
                    if (NetworkObject::isConnected())
                        Shell::getInstance().info("Player " + to_string(_number) + " is now connected");
                    else
                        Shell::getInstance().warning("Player " + to_string(_number) + " did not connect");
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Getter for the last move
                
                /** CODE **/
                public : string getMove ()
                {
                    
                    // We return the last move received
                    return _moves.back();
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Getter for the name
                
                /** CODE **/
                public : string getName ()
                {
                    
                    // We return the name attribute
                    return _name;
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Returns the number of invalid decisions taken
                
                /** CODE **/
                public : int getNbInvalidDecisions ()
                {
                    
                    // We count the number of invalid moves
                    return count(_moves.begin(), _moves.end(), MOVE_INVALID);
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Computes the total number of moves performed by the player
                
                /** CODE **/
                public : int getNbMovesPerformed ()
                {
                    
                    // Sum of the number of valid decisions and penalties caused by mud
                    return getNbValidDecisions() + _nbMudPenalties;
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Getter for the number of additional moves caused by mud
                
                /** CODE **/
                public : int getNbMudPenalties ()
                {
                    
                    // We return the number of mud penalties attribute
                    return _nbMudPenalties;
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Computes the number of moves that missed the timing
                
                /** CODE **/
                public : int getNbTimingsMissed ()
                {
                    
                    // We count the number of missed moves
                    return count(_moves.begin(), _moves.end(), MOVE_MISSED);
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Computes the number of valid decisions that were received
                
                /** CODE **/
                public : int getNbValidDecisions ()
                {
                    
                    // We count the number of valid moves
                    return _moves.size() - getNbTimingsMissed() - getNbInvalidDecisions();
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Getter for the player number
                
                /** CODE **/
                public : int getNumber ()
                {
                    
                    // We return the number attribute
                    return _number;
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Getter for the output file name, given a player number
                
                /** CODE **/
                public : static string getOutputFileName (string outputDirectory, int playerNumber)
                {
                    
                    // We return the constant with the tag replaced
                    return outputDirectory + "/" + regex_replace(string(Player::OUTPUT_FILE_NAME), regex("\\[NUMBER\\]"), to_string(playerNumber));
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Getter for the preprocessing computation time
                
                /** CODE **/
                public : double getPreprocessingComputationTime ()
                {
                    
                    // We return the computation time for preprocessing attribute
                    return _preprocessingComputationTime;
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Getter for the score
                
                /** CODE **/
                public : double getScore ()
                {
                    
                    // We return the score attribute
                    return _score;
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Getter for the turns computation time
                
                /** CODE **/
                public : double getTurnsComputationTime ()
                {
                    
                    // We return the total computation time for turns attribute
                    return _turnsComputationTime;
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Asks the player file for the player's name
                
                /** CODE **/
                public : void initializeName ()
                {
                    
                    // We read the socket until a name is given
                    if (NetworkObject::isConnected())
                    {
                        _name = NetworkObject::receiveMessage(true);
                        if (_name.size() == 0)
                            Shell::getInstance().error("Cannot set name to an empty string");
                        Shell::getInstance().info("Player " + to_string(_number) + " is now known as <b>" + _name + "</b>");
                    }
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Checks if the player is crossing mud
                
                /** CODE **/
                public : bool inMud ()
                {
                    
                    // Checks if we are in mud
                    return _blocked > 0;
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Checks if the player has sent a new move
                // If so, the move is added to the list of moves
                // If not, an invalid move is added instead
                // Computation time is not measured when continuing in mud
                
                /** CODE **/
                public : void newMove ()
                {
                    
                    // If we are still preprocessing, we miss the timing
                    if (_preprocessingComputationTime == 0.0)
                        _moves.push_back(MOVE_MISSED);
                
                    // If we are in mud, we do nothing
                    else if (inMud())
                        _nbMudPenalties++;
                    
                    // Otherwise, we check for a move
                    else
                    {
                    
                        // We read the socket for a turn information in blocking or non-blocking mode depending on if the game is synchronous
                        string message = NetworkObject::receiveMessage(_synchronous);
                        
                        // We check if the message arrived
                        TypeConverter converter;
                        if (message.length() == 0)
                            _moves.push_back(MOVE_MISSED);
                        
                        // We check if the message has a correct form
                        else if (message.length() > 1 && !converter.isDouble(message.substr(1, message.length() - 1)))
                            _moves.push_back(MOVE_INVALID);
                        
                        // It must match a correct move
                        else
                        {
                            string move = message.substr(0, 1);
                            double time = converter.toDouble(message.substr(1, message.length() - 1));
                            _turnsComputationTime += time;
                            if (move == MOVE_UP || move == MOVE_DOWN || move == MOVE_LEFT || move == MOVE_RIGHT)
                                _moves.push_back(move);
                            else if (move == MOVE_MISSED)
                                _moves.push_back(MOVE_MISSED);
                            else
                                _moves.push_back(MOVE_INVALID);
                        }
                        
                    }
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Makes the player advance in mud
                
                /** CODE **/
                public : void reduceBlocking ()
                {
                    
                    // We advance in mud
                    _blocked--;
                    
                }
            
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Saves the player's decision in the form of an AI Python file
                
                /** CODE **/
                public : void save (string outputDirectory)
                {
                    
                    // We create the destination file
                    fstream outputFile;
                    string fileName = Player::getOutputFileName(outputDirectory, _number);
                    outputFile.open(fileName, fstream::trunc | fstream::out);
                    
                    // We write the file as if it was a normal player file
                    outputFile << "#!/usr/bin/env python3" << endl;
                    outputFile << "# -*- coding: utf-8 -*-" << endl;
                    outputFile << "####################################################################################################################################################################################################################################" << endl;
                    outputFile << "############################################################################################################## LICENSE #############################################################################################################" << endl;
                    outputFile << "####################################################################################################################################################################################################################################" << endl;
                    outputFile << "#" << endl;
                    outputFile << "#    Copyright © 2016 Bastien Pasdeloup (name.surname@gmail.com) and Télécom Bretagne" << endl;
                    outputFile << "#" << endl;
                    outputFile << "#    This file is part of PyRat." << endl;
                    outputFile << "#" << endl;
                    outputFile << "#    PyRat is free software: you can redistribute it and/or modify" << endl;
                    outputFile << "#    it under the terms of the GNU General Public License as published by" << endl;
                    outputFile << "#    the Free Software Foundation, either version 3 of the License, or" << endl;
                    outputFile << "#    (at your option) any later version." << endl;
                    outputFile << "#" << endl;
                    outputFile << "#    PyRat is distributed in the hope that it will be useful," << endl;
                    outputFile << "#    but WITHOUT ANY WARRANTY; without even the implied warranty of" << endl;
                    outputFile << "#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the" << endl;
                    outputFile << "#    GNU General Public License for more details." << endl;
                    outputFile << "#" << endl;
                    outputFile << "#    You should have received a copy of the GNU General Public License" << endl;
                    outputFile << "#    along with PyRat.  If not, see <http://www.gnu.org/licenses/>." << endl;
                    outputFile << "#" << endl;
                    outputFile << "####################################################################################################################################################################################################################################" << endl;
                    outputFile << "############################################# PRE-DEFINED CONSTANTS ########################################################################################### CONSTANTES PRÉ-DÉFINIES ############################################" << endl;
                    outputFile << "####################################################################################################################################################################################################################################" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#    In this section, you will find some pre-defined constants that are needed for the game                       #    Dans cette section, vous trouvez des constantes pré-définies nécessaires pour la partie                     #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "####################################################################################################################################################################################################################################" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#    TEAM_NAME : string                                                                                           #    TEAM_NAME : string                                                                                          #" << endl;
                    outputFile << "#    ------------------                                                                                           #    ------------------                                                                                          #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#        This constant represents your name as a team                                                             #        Cette constante représente le nom de votre équipe                                                       #" << endl;
                    outputFile << "#        Please change the default value to a string of your choice                                               #        Veuillez en changer la valeur par une chaîne de caractères de votre choix                               #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#    MOVE_XXX : char                                                                                              #    MOVE_XXX : char                                                                                             #" << endl;
                    outputFile << "#    ---------------                                                                                              #    ---------------                                                                                             #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#        The four MOVE_XXX constants represent the possible directions where to move                              #        Les quatre constantes MOVE_XXX représentent les directions possibles où se déplacer                     #" << endl;
                    outputFile << "#        The \"turn\" function should always return one of these constants                                          #        La fonction \"turn\" doit toujours renvoyer l'une d'entre elles                                           #" << endl;
                    outputFile << "#        Please do not edit them (any other value will be considered incorrect)                                   #        Merci de ne pas les éditer (toute autre valeur sera considérée comme incorrecte)                        #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "####################################################################################################################################################################################################################################" << endl << endl;
                    outputFile << "TEAM_NAME = \"" << _name << "\"" << endl << endl;
                    outputFile << "MOVE_DOWN = 'D'" << endl;
                    outputFile << "MOVE_LEFT = 'L'" << endl;
                    outputFile << "MOVE_RIGHT = 'R'" << endl;
                    outputFile << "MOVE_UP = 'U'" << endl;
                    outputFile << "MOVE_INVALID = 'X'" << endl;
                    outputFile << "MOVE_MISSED = '_'" << endl << endl;
                    outputFile << "####################################################################################################################################################################################################################################" << endl;
                    outputFile << "########################################### SPACE FOR FREE EXPRESSION ######################################################################################### ZONE D'EXPRESSION LIBRE ############################################" << endl;
                    outputFile << "####################################################################################################################################################################################################################################" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#    In this file, you will two functions: \"preprocessing\" and \"turn\"                                             #    Dans ce fichier, vous trouverez deux fonctions : \"preprocessing\" et \"turn\"                                  #" << endl;
                    outputFile << "#    You need to edit these functions to create your PyRat program                                                #    Vous devez éditer ces fonctions pour réaliser votre programme PyRat                                         #" << endl;
                    outputFile << "#    However, you are not limited to them, and you can write any Python code in this file                         #    Toutefois, vous n'êtes pas limité(e), et vous pouvez écrire n'importe quel code Python dans ce fichier      #" << endl;
                    outputFile << "#    Please use the following space to write your additional constants, variables, functions...                   #    Merci d'utiliser l'espace ci-dessous pour écrire vos constantes, variables, fonctions...                    #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "####################################################################################################################################################################################################################################" << endl << endl;
                    outputFile << "# List of all moves" << endl;
                    outputFile << "moves = [";
                    for (unsigned int i = 0 ; i < _moves.size() ; i++)
                    {
                        if (i > 0)
                            outputFile << ", ";
                        if (_moves[i] == MOVE_DOWN)
                            outputFile << "MOVE_DOWN";
                        else if (_moves[i] == MOVE_LEFT)
                            outputFile << "MOVE_LEFT";
                        else if (_moves[i] == MOVE_RIGHT)
                            outputFile << "MOVE_RIGHT";
                        else if (_moves[i] == MOVE_UP)
                            outputFile << "MOVE_UP";
                        else if (_moves[i] == MOVE_INVALID)
                            outputFile << "MOVE_INVALID";
                        else
                            outputFile << "MOVE_MISSED";
                    }
                    outputFile << "]" << endl << endl;
                    outputFile << "####################################################################################################################################################################################################################################" << endl;
                    outputFile << "############################################# PREPROCESSING FUNCTION ######################################################################################### FONCTION DE PRÉ-TRAITEMENT ##########################################" << endl;
                    outputFile << "####################################################################################################################################################################################################################################" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#    This function is executed once at the very beginning of the game                                             #    Cette fonction est exécutée une unique fois au tout début de la partie                                      #" << endl;
                    outputFile << "#    It allows you to make some computations before the players are allowed to move                               #    Vous pouvez y effectuer des calculs avant que les joueurs ne puissent commencer à bouger                    #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "####################################################################################################################################################################################################################################" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#    mazeMap : dict(pair(int, int), dict(pair(int, int), int))                                                    #    mazeMap : dict(pair(int, int), dict(pair(int, int), int))                                                   #" << endl;
                    outputFile << "#    ---------------------------------------------------------                                                    #    ---------------------------------------------------------                                                   #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#        Map of the maze as a data structure                                                                      #        Structure de données représentant la carte du labyrinthe                                                #" << endl;
                    outputFile << "#        mazeMap[x] gives you the neighbors of cell x                                                             #        mazeMap[x] renvoie les voisins de la case x                                                             #" << endl;
                    outputFile << "#        mazeMap[x][y] gives you the weight of the edge linking cells x and y                                     #        mazeMap[x][y] renvoie le poids de l'arête reliant les cases x et y                                      #" << endl;
                    outputFile << "#        if mazeMap[x][y] is undefined, there is no edge between cells x and y                                    #        Si mazeMap[x][y] n'est pas défini, les cases x et y ne sont pas reliées par une arête                   #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#    mazeWidth : int                                                                                              #    mazeWidth : int                                                                                             #" << endl;
                    outputFile << "#    ---------------                                                                                              #    ---------------                                                                                             #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#        Width of the maze, in number of cells                                                                    #        Largeur du labyrinthe, en nombre de cases                                                               #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#    mazeHeight : int                                                                                             #    mazeHeight : int                                                                                            #" << endl;
                    outputFile << "#    ----------------                                                                                             #    ----------------                                                                                            #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#        Height of the maze, in number of cells                                                                   #        Hauteur du labyrinthe, en nombre de cases                                                               #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#    playerLocation : pair(int, int)                                                                              #    playerLocation : pair(int, int)                                                                             #" << endl;
                    outputFile << "#    -------------------------------                                                                              #    -------------------------------                                                                             #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#        Initial location of your character in the maze                                                           #        Emplacement initial de votre personnage dans le labyrinthe                                              #" << endl;
                    outputFile << "#        It is a pair (line, column), with (0, 0) being the top-left cell in the maze                             #        C'est une paire (ligne, colonne), (0, 0) étant la case en haut à gauche du labyrinthe                   #" << endl;
                    outputFile << "#        playerLocation[0] gives you your current line                                                            #        playerLocation[0] renvoie votre ligne actuelle                                                          #" << endl;
                    outputFile << "#        playerLocation[1] gives you your current column                                                          #        playerLocation[1] renvoie votre colonne actuelle                                                        #" << endl;
                    outputFile << "#        mazeMap[playerLocation] gives you the cells you can access directly                                      #        mazeMap[playerLocation] renvoie les cases auxquelles vous pouvez accéder directement                    #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#    opponentLocation : pair(int, int)                                                                            #    opponentLocation : pair(int, int)                                                                           #" << endl;
                    outputFile << "#    ---------------------------------                                                                            #    ---------------------------------                                                                           #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#        Initial location opponent's character in the maze                                                        #        Emplacement initial du personnage de votre adversaire dans le labyrinthe                                #" << endl;
                    outputFile << "#        The opponent's location can be used just as playerLocation                                               #        La position de l'adversaire peut être utilisée comme pour playerLocation                                #" << endl;
                    outputFile << "#        If you are playing in single-player mode, this variable is undefined                                     #        Si vous jouez en mode un joueur, cette variable n'est pas définie                                       #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#    piecesOfCheese : list(pair(int, int))                                                                        #    piecesOfCheese : list(pair(int, int))                                                                       #" << endl;
                    outputFile << "#    -------------------------------------                                                                        #    -------------------------------------                                                                       #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#        Locations of all pieces of cheese in the maze                                                            #        Emplacements des morceaux de fromage dans le labyrinthe                                                 #" << endl;
                    outputFile << "#        The locations are given in no particular order                                                           #        Les emplacements sont données dans un ordre quelconque                                                  #" << endl;
                    outputFile << "#        As for the players locations, these locations are pairs (line, column)                                   #        Comme pour les positions des joueurs, ces emplacements sont des paires (ligne, colonne)                 #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#    timeAllowed : float                                                                                          #    timeAllowed : float                                                                                         #" << endl;
                    outputFile << "#    -------------------                                                                                          #    -------------------                                                                                         #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#        Time that is allowed for preprocessing, in seconds                                                       #        Temps alloué pour le pré-traitement, en secondes                                                        #" << endl;
                    outputFile << "#        After this time, players will have the right to move                                                     #        Après ce temps, les joueurs pourront commencer à bouger                                                 #" << endl;
                    outputFile << "#        If your preprocessing is too long, you will still finish it                                              #        Si votre pré-traitement est trop long, vous terminerez quand même son exécution                         #" << endl;
                    outputFile << "#        However, it will not prevent your opponent from moving                                                   #        Toutefois, cela n'empêchera pas votre adversaire de bouger                                              #" << endl;
                    outputFile << "#        Make sure to finish your preprocessing within the allowed time                                           #        Assurez vous de terminer votre pré-traitement dans le temps imparti                                     #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "####################################################################################################################################################################################################################################" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#    This function does not return anything                                                                       #    Cette fonction ne renvoie rien                                                                              #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "####################################################################################################################################################################################################################################" << endl << endl;
                    outputFile << "def preprocessing (mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed) :" << endl << endl;
                    outputFile << "    # Nothing to do" << endl;
                    outputFile << "    pass" << endl << endl;
                    outputFile << "####################################################################################################################################################################################################################################" << endl;
                    outputFile << "################################################# TURN FUNCTION ############################################################################################### FONCTION DE TOUR DE JEU ############################################" << endl;
                    outputFile << "####################################################################################################################################################################################################################################" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#    Once the preprocessing is over, the game starts and players can start moving                                 #    Une fois le pré-traitement terminé, la partie démarre et les joueurs peuvent commencer à bouger             #" << endl;
                    outputFile << "#    The \"turn\" function is called at regular times                                                               #    La fonction \"turn\" est appelée à intervalles réguliers                                                      #" << endl;
                    outputFile << "#    You should determine here your next move, given a game configuration                                         #    Vous devez déterminer ici votre prochain mouvement, étant donnée une configuration du jeu                   #" << endl;
                    outputFile << "#    This decision will then be applied, and your character will move in the maze                                 #    Cette décision sera ensuite appliquée, et votre personnage se déplacera dans le labyrinthe                  #" << endl;
                    outputFile << "#    Then, the \"turn\" function will be called again with the new game configuration                               #    Ensuite, la fonction \"turn\" sera appelée à nouveau, avec la nouvelle configuration du jeu                   #" << endl;
                    outputFile << "#    This process is repeated until the game is over                                                              #    Ce processus est répété jusqu'à la fin de la partie                                                         #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "####################################################################################################################################################################################################################################" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#    mazeMap : dict(pair(int, int), dict(pair(int, int), int))                                                    #    mazeMap : dict(pair(int, int), dict(pair(int, int), int))                                                   #" << endl;
                    outputFile << "#    ---------------------------------------------------------                                                    #    ---------------------------------------------------------                                                   #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#        Same argument as for the \"preprocessing\" function                                                        #        Même paramètre que pour la fonction \"preprocessing\"                                                     #" << endl;
                    outputFile << "#        The value of mazeMap does not change between two calls of function \"turn\"                                #        La valeur de mazeMap ne change pas d'un appel à l'autre de la fonction \"turn\"                           #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#    mazeWidth : int                                                                                              #    mazeWidth : int                                                                                             #" << endl;
                    outputFile << "#    ---------------                                                                                              #    ---------------                                                                                             #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#        Same argument as for the \"preprocessing\" function                                                        #        Même paramètre que pour la fonction \"preprocessing\"                                                     #" << endl;
                    outputFile << "#        The value of mazeWidth does not change between two calls of function \"turn\"                              #        La valeur de mazeWidth ne change pas d'un appel à l'autre de la fonction \"turn\"                         #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#    mazeHeight : int                                                                                             #    mazeHeight : int                                                                                            #" << endl;
                    outputFile << "#    ----------------                                                                                             #    ----------------                                                                                            #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#        Same argument as for the \"preprocessing\" function                                                        #        Même paramètre que pour la fonction \"preprocessing\"                                                     #" << endl;
                    outputFile << "#        The value of mazeHeight does not change between two calls of function \"turn\"                             #        La valeur de mazeHeight ne change pas d'un appel à l'autre de la fonction \"turn\"                        #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#    playerLocation : pair(int, int)                                                                              #    playerLocation : pair(int, int)                                                                             #" << endl;
                    outputFile << "#    -------------------------------                                                                              #    -------------------------------                                                                             #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#        Current location of your character in the maze                                                           #        Emplacement actuel de votre personnage dans le labyrinthe                                               #" << endl;
                    outputFile << "#        At the first call of function \"turn\", it will be your initial location                                   #        Au premier appel de la fonction \"turn\", ce sera votre emplacement initial                               #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#    opponentLocation : pair(int, int)                                                                            #    opponentLocation : pair(int, int)                                                                           #" << endl;
                    outputFile << "#    ---------------------------------                                                                            #    ---------------------------------                                                                           #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#        Current location of your opponent's character in the maze                                                #        Emplacement actuel de votre personnage dans le labyrinthe                                               #" << endl;
                    outputFile << "#        At the first call of function \"turn\", it will be your opponent's initial location                        #        Au premier appel de la fonction \"turn\", ce sera votre emplacement initial                               #" << endl;
                    outputFile << "#        If you are playing in single-player mode, this variable is undefined                                     #        Si vous jouez en mode un joueur, cette variable n'est pas définie                                       #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#    playerScore : float                                                                                          #    playerScore: float                                                                                          #" << endl;
                    outputFile << "#    -------------------                                                                                          #    ------------------                                                                                          #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#        Your current score when the turn begins                                                                  #        Votre score actuel au début du tour                                                                     #" << endl;
                    outputFile << "#        It is initialized at 0, and increases by 1 when you eat a piece of cheese                                #        Il est initialisé à 0, et augmente de 1 pour chaque morceau de fromage mangé                            #" << endl;
                    outputFile << "#        If you reach the same piece of cheese as your opponent at the same moment, it is worth 0.5 points        #        Si vous arrivez sur le même morceau de fromage que votre adversaire au même moment, il vaut 0.5 points  #" << endl;
                    outputFile << "#        If you are playing in single-player mode, this variable is undefined                                     #        Si vous jouez en mode un joueur, cette variable n'est pas définie                                       #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#    opponentScore : float                                                                                        #    opponentScore: float                                                                                        #" << endl;
                    outputFile << "#    ---------------------                                                                                        #    --------------------                                                                                        #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#        The score of your opponent when the turn begins                                                          #        Le score de votre adversaire au début du tour                                                           #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#    piecesOfCheese : list(pair(int, int))                                                                        #    piecesOfCheese : list(pair(int, int))                                                                       #" << endl;
                    outputFile << "#    -------------------------------------                                                                        #    -------------------------------------                                                                       #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#        Locations of all remaining pieces of cheese in the maze                                                  #        Emplacements des morceaux de fromage restants dans le labyrinthe                                        #" << endl;
                    outputFile << "#        The list is updated at every call of function \"turn\"                                                     #        La liste est mise à jour à chaque appel de la fonction \"turn\"                                           #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#    timeAllowed : float                                                                                          #    timeAllowed : float                                                                                         #" << endl;
                    outputFile << "#    -------------------                                                                                          #    -------------------                                                                                         #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#        Time that is allowed for determining the next move to perform, in seconds                                #        Temps alloué pour le calcul du prochain mouvement, en secondes                                          #" << endl;
                    outputFile << "#        After this time, the decided move will be applied                                                        #        Après ce temps, le mouvement choisi sera appliqué                                                       #" << endl;
                    outputFile << "#        If you take too much time, you will still finish executing your code, but you will miss the deadline     #        Si vous prenez trop de temps, votre code finira quand-même son excution, mais vous raterez le timing    #" << endl;
                    outputFile << "#        Your move will then be considered the next time PyRat checks for players decisions                       #        Votre mouvement sera alors considéré la prochaine fois que PyRat vérifiera les décisions des joueurs    #" << endl;
                    outputFile << "#        However, it will not prevent your opponent from moving if he respected the deadline                      #        Toutefois, cela n'empêchera pas votre adversaire de bouger s'il a respecté le timing                    #" << endl;
                    outputFile << "#        Make sure to finish your computations within the allowed time                                            #        Assurez vous de terminer vos calculs dans le temps imparti                                              #" << endl;
                    outputFile << "#        Also, save some time to ensure that PyRat will receive your decision before the deadline                 #        Aussi, gardez un peu de temps pour garantir que PyRat recevra votre decision avant la fin du temps      #" << endl;
                    outputFile << "#        If you are playing in synchronous mode, this variable is undefined                                       #        Si vous jouez en mode synchrone, cette variable n'est pas définie                                       #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "####################################################################################################################################################################################################################################" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "#    This function should return one of the following constants: MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, MOVE_UP        #    Cette fonction renvoie l'une des constantes suivantes : MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, MOVE_UP           #" << endl;
                    outputFile << "#    The returned constant represents the move you decide to perform: down, left, right, up                       #    La constante renvoyée représente le mouvement que vous décidez d'effectuer : bas, gauche, droite, haut      #" << endl;
                    outputFile << "#    Any other value will be considered incorrect                                                                 #    Toute autre valeur sera considérée comme incorrecte                                                         #" << endl;
                    outputFile << "#                                                                                                                 #                                                                                                                #" << endl;
                    outputFile << "####################################################################################################################################################################################################################################" << endl << endl;
                    outputFile << "def turn (mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed) :" << endl << endl;
                    outputFile << "    # We return the next move" << endl;
                    outputFile << "    move = moves[0]" << endl;
                    outputFile << "    print(\"Move: [\" + move + \"]\")" << endl;
                    outputFile << "    moves.pop(0)" << endl;
                    outputFile << "    return move" << endl << endl;
                    outputFile << "####################################################################################################################################################################################################################################" << endl;
                    outputFile << "####################################################################################################################################################################################################################################";
                    
                    // Done
                    outputFile.close();
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Sends the preprocessing information to the player
                // The message is send as a JSON-like string
                
                /** CODE **/
                public : void sendInitialInformation (string mazeMap, string mazeWidth, string mazeHeight, string playerLocation, string opponentLocation, string piecesOfCheese, string timeAllowed)
                {
                    
                    // We send the information in JSON style
                    string message = "{\"mazeMap\": " + mazeMap + ", "
                                    + "\"mazeWidth\": " + mazeWidth + ", "
                                    + "\"mazeHeight\": " + mazeHeight + ", "
                                    + "\"playerLocation\": " + playerLocation + ", "
                                    + (opponentLocation.empty() ? "" : "\"opponentLocation\": " + opponentLocation + ", ")
                                    + "\"piecesOfCheese\": " + piecesOfCheese + ", "
                                    + "\"timeAllowed\": " + timeAllowed + "}";

                    // We send the message
                    NetworkObject::sendMessage(message);
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Sends the turn information to the player
                // The message is send as a JSON-like string
                
                /** CODE **/
                public : void sendTurnInformation (string playerLocation, string opponentLocation, string playerScore, string opponentScore, string piecesOfCheese, string timeAllowed, bool previousTurnIgnored, bool finalInformation)
                {

                    // We send the turn information only if the following cases:
                    // It is the last message of the game
                    // The program just wend out of preprocessing
                    // A new decision will be needed during next turn (will get out of mud, normal turn... which is not the case if player missed a turn)
                    if (finalInformation || (_neverSentTurnInformation && _preprocessingComputationTime > 0.0) || (!inMud() && _preprocessingComputationTime > 0.0 && !previousTurnIgnored && _moves.back() != MOVE_MISSED))
                    {

                        // We send the information in JSON style
                        string message = "{\"playerLocation\": " + playerLocation + ", "
                                        + (opponentLocation.empty() ? "" : "\"opponentLocation\": " + opponentLocation + ", ")
                                        + "\"playerScore\": " + playerScore + ", "
                                        + (opponentScore.empty() ? "" : "\"opponentScore\": " + opponentScore + ", ")
                                        + (_synchronous ? "" : "\"timeAllowed\": " + timeAllowed + ", ")
                                        + "\"piecesOfCheese\": " + piecesOfCheese + "}";

                        // We send the message
                        NetworkObject::sendMessage(message);
                        _neverSentTurnInformation = false;
                        
                    }

                }
                
            /**********************************************************************************************************************************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
            
        };
        
    #endif

/**********************************************************************************************************************************************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
