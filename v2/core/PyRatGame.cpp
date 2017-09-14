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
    #include <string>
    #include <thread>
    #include <unistd.h>
    #include <vector>
    
    /** INTERNAL **/
    #include <GUI.cpp>
    #include <Maze.cpp>
    #include <Moves.cpp>
    #include <Player.cpp>
    #include <Shell.cpp>
    #include <ToString.cpp>
    
    /** NAMESPACES **/
    using namespace std;

/**********************************************************************************************************************************************************************************************************************************/
/************************************************************************************************************** CLASS *************************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
    
    #ifndef _PYRAT_GAME_
    #define _PYRAT_GAME_
        
        class PyRatGame
        {
            
            /**********************************************************************************************************************************************************************************************************/
            /************************************************************************************************ CONSTANTS ***********************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Name of the file where to export the game result
                
                /** CODE **/
                private : const string OUTPUT_FILE_NAME = "results.txt";
            
            /**********************************************************************************************************************************************************************************************************/
            /*********************************************************************************************** ATTRIBUTES ***********************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // GUI object
                
                /** CODE **/
                private : GUI* _gui;
            
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Time given to the players for the preprocessing step
                
                /** CODE **/
                private : double _preprocessingTime;
                
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Maze object
                
                /** CODE **/
                private : Maze* _maze;
            
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Players objects
                
                /** CODE **/
                private : vector<Player*> _players;
            
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Synchronicity mode
                // If it is "synchronous", both players play at the same time
                // If it is "semi-synchronous", players play when available
                
                /** CODE **/
                private : string _synchronicity;
            
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Number of the current turn
                
                /** CODE **/
                private : int _turnNumber = 0;
                
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Time given to the players for the turn step
                
                /** CODE **/
                private : double _turnTime;
                
            /**********************************************************************************************************************************************************************************************************/
            /********************************************************************************************** CONSTRUCTORS **********************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Constructor with all needed game objects
                
                /** CODE **/
                public : PyRatGame (Maze* maze, GUI* gui, vector<Player*> players, double preprocessingTime, double turnTime, string synchronicity) : _gui(gui), _preprocessingTime(preprocessingTime), _maze(maze), _players(players), _synchronicity(synchronicity), _turnTime(turnTime)
                {}
            
            /**********************************************************************************************************************************************************************************************************/
            /*********************************************************************************************** DESTRUCTOR ***********************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Empty destructor
                
                /** CODE **/
                public : virtual ~PyRatGame ()
                {}
                
            /**********************************************************************************************************************************************************************************************************/
            /************************************************************************************************* METHODS ************************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Checks if the preprocessing step is over
                
                /** CODE **/
                private : void checkIfPreprocessing ()
                {
                    
                    // We check if players are in preprocessing step
                    vector<thread> playersThreads;
                    for (auto player : _players)
                        playersThreads.push_back(thread(&Player::checkIfPreprocessing, player));
                    
                    // We wait until all functions finish
                    for (auto& playerThread : playersThreads)
                        playerThread.join();

                }
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Checks if some players are connected to abort the game if all players crashed
                
                /** CODE **/
                private : void checkIfPlayersConnected ()
                {
                    
                    // If all players are not connected, we stop the game
                    bool somePlayersConnected = false;
                    for (auto player : _players)
                        somePlayersConnected |= player->isConnected();
                    if (!somePlayersConnected)
                        Shell::getInstance().error("No player has connected or all players have crashed");
                    
                }
            
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Connects the elements together in various threads
                
                /** CODE **/
                private : void connectElements ()
                {
                    
                    // We connect to the GUI and to the clients in different threads
                    Shell::getInstance().info("Waiting for game elements to connect");
                    vector<thread> elementsThreads;
                    if (_gui)
                        elementsThreads.push_back(thread(&GUI::establishConnection, _gui));
                    for (auto player : _players)
                        elementsThreads.push_back(thread(&Player::establishConnection, player));
                    
                    // We wait until all elements are connected
                    for (auto& elementThread : elementsThreads)
                        elementThread.join();
                    
                    // If all players crashed, we stop the game
                    checkIfPlayersConnected();
                    
                }
            
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Initializes the players names in various threads
                
                /** CODE **/
                private : void initializePlayersNames ()
                {
                    
                    // We ask the players for their names
                    vector<thread> playersThreads;
                    for (auto player : _players)
                        playersThreads.push_back(thread(&Player::initializeName, player));
                    
                    // We wait until all names are received
                    for (auto& playerThread : playersThreads)
                        playerThread.join();
                    
                    // If all players crashed, we stop the game
                    checkIfPlayersConnected();
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Asks for the players moves in various threads then updates the scores
                // Returns a boolean indicating if the turn should be ignored (for semi-synchronous games)
                
                /** CODE **/
                private : bool movePlayers ()
                {
                    
                    // We check if the players have sent new moves
                    vector<thread> playersThreads;
                    for (auto player : _players)
                        playersThreads.push_back(thread(&Player::newMove, player));
                    
                    // We wait until all decisions are verified
                    for (auto& playerThread : playersThreads)
                        playerThread.join();
                    
                    // If all players crashed, we stop the game
                    checkIfPlayersConnected();
                    
                    // For semi-synchronous games, if nobody moves or if one player is in mud and the other didn't move, the turn is cancelled
                    if (_synchronicity == string("semi-synchronous"))
                    {
                        bool atLeastOnePlayerMoved = false;
                        bool allPlayersInMud = true;
                        for (auto player : _players)
                        {
                            atLeastOnePlayerMoved |= (!player->inMud() && player->getMove() != MOVE_MISSED);
                            allPlayersInMud &= player->inMud();
                        }
                        if (!atLeastOnePlayerMoved && !allPlayersInMud)
                        {
                            for (auto player : _players)
                                player->cancelMissedMove();
                            return true;
                        }
                    }

                    // We apply the moves
                    string moves;
                    for (auto player : _players)
                    {
                        _maze->movePlayer(player);
                        moves += "[" + player->getMove() + "]";
                    }
                    Shell::getInstance().info("Received : " + moves);

                    // We update the score
                    _maze->updateCheese();
                    return false;

                }
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Saves the game result to the output file
                
                /** CODE **/
                public : void save (string outputDirectory, string gameID)
                {
                    
                    // We create the destination file
                    fstream outputFile;
                    outputFile.open(outputDirectory + "/" + OUTPUT_FILE_NAME, fstream::trunc | fstream::out);
                    
                    // We export the players names and scores
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
                    outputFile << "############################################################################################################# CONTENTS #############################################################################################################" << endl;
                    outputFile << "####################################################################################################################################################################################################################################" << endl << endl;
                    outputFile << "# Game information" << endl;
                    TypeConverter converter;
                    outputFile << "{\"gameID\" : \"" << gameID << "\", \"turns\" : " << to_string(_turnNumber) << ", ";
                    for (unsigned int i = 0 ; i < _players.size() ; i++)
                    {
                        outputFile << "\"player" << i + 1 << "\" : {\"name\" : \"" + converter.toJSON(_players[i]->getName()) << "\", ";
                        outputFile <<                              "\"score\" : " << double_to_string(_players[i]->getScore()) << ", ";
                        outputFile <<                              "\"nbValidDecisions\" : " << to_string(_players[i]->getNbValidDecisions()) << ", ";
                        outputFile <<                              "\"nbInvalidDecisions\" : " << to_string(_players[i]->getNbInvalidDecisions()) << ", ";
                        outputFile <<                              "\"nbTimingsMissed\" : " << to_string(_players[i]->getNbTimingsMissed()) << ", ";
                        outputFile <<                              "\"totalNbMoves\" : " << to_string(_players[i]->getNbMovesPerformed()) << ", ";
                        outputFile <<                              "\"nbMudPenalties\" : " << to_string(_players[i]->getNbMudPenalties()) << ", ";
                        outputFile <<                              "\"preprocessingComputationTime\" : " << double_to_string(_players[i]->getPreprocessingComputationTime()) << ", ";
                        outputFile <<                              "\"turnsComputationTime\" : " << double_to_string(_players[i]->getTurnsComputationTime()) << "}";
                        if (i != _players.size() - 1)
                            outputFile << ", ";
                    }
                    outputFile << "}" << endl << endl;
                    outputFile << "####################################################################################################################################################################################################################################" << endl;
                    outputFile << "####################################################################################################################################################################################################################################";
                    
                    // Done
                    outputFile.close();
                    
                }
            
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Sends the preprocessing information to the players in various threads
                
                /** CODE **/
                private : void sendInitialInformationToPlayers ()
                {

                    // We prepare the information to send
                    string mazeMap = _maze->mapToString();
                    string mazeWidth = to_string(_maze->getWidth());
                    string mazeHeight = to_string(_maze->getHeight());
                    vector<string> playersLocations;
                    for (auto player : _players)
                        playersLocations.push_back(_maze->getNiceCurrentPlayerLocation(player));
                    string piecesOfCheese = _maze->piecesOfCheeseToString();
                    string timeAllowed = double_to_string(_preprocessingTime);
                    
                    // We send the information to the players
                    vector<thread> playersThreads;
                    for (unsigned int i = 0 ; i < _players.size() ; i++)
                        playersThreads.push_back(thread(&Player::sendInitialInformation, _players[i], mazeMap, mazeWidth, mazeHeight, playersLocations[i], (playersLocations.size() > 1) ? playersLocations[1 - i] : "", piecesOfCheese, timeAllowed));
                    
                    // We wait until all information has been sent
                    for (auto& playerThread : playersThreads)
                        playerThread.join();
                    
                }
            
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Sends the turn information to the players in various threads
                
                /** CODE **/
                private : void sendTurnInformationToPlayers (bool previousTurnIgnored, bool finalInformation)
                {
                    
                    // We prepare the information to send
                    vector<string> playersLocations;
                    vector<string> playersScores;
                    for (auto player : _players)
                    {
                        playersLocations.push_back(_maze->getNiceCurrentPlayerLocation(player));
                        playersScores.push_back(double_to_string(player->getScore()));
                    }
                    string piecesOfCheese = _maze->piecesOfCheeseToString();
                    string timeAllowed = double_to_string(_turnTime);
                    
                    // We send the information to the players
                    vector<thread> playersThreads;
                    for (unsigned int i = 0 ; i < _players.size() ; i++)
                        playersThreads.push_back(thread(&Player::sendTurnInformation, _players[i], playersLocations[i], (playersLocations.size() > 1) ? playersLocations[1 - i] : "", playersScores[i], (playersScores.size() > 1) ? playersScores[1 - i] : "", piecesOfCheese, timeAllowed, previousTurnIgnored, finalInformation));
                    
                    // We wait until all information has been sent
                    for (auto& playerThread : playersThreads)
                        playerThread.join();
                    
                }
            
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Shows the game result into the shell
                
                /** CODE **/
                private : void showResult ()
                {
                    
                    // One player only
                    if (_players.size() == 1)
                        Shell::getInstance().info("Player " + _players[0]->getName() + " got all the cheese!");
                    
                    // Two players
                    else
                    {
                        Shell::getInstance().info("Final score: <b>" + _players[0]->getName() + "</b> " + double_to_string(_players[0]->getScore()) + " / " + double_to_string(_players[1]->getScore()) + " <b>" + _players[1]->getName() + "</b>");
                        if (_players[0]->getScore() > _players[1]->getScore())
                            Shell::getInstance().info("Final score: <b>" + _players[0]->getName() + "</b> wins!");
                        else if (_players[0]->getScore() < _players[1]->getScore())
                            Shell::getInstance().info("Final score: <b>" + _players[1]->getName() + "</b> wins!");
                        else
                            Shell::getInstance().info("The game is a tie!");
                    }
                    
                }
            
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Main game loop
                // First, the names are set
                // Then, the preprocessing information is sent
                // Then, the turns occur while there still is cheese
                
                /** CODE **/
                public : void start ()
                {

                    // We initialize the game elements and get the players names
                    connectElements();
                    initializePlayersNames();
                    
                    // When everything is ready, we send the information to the GUI
                    if (_gui)
                        _gui->start(_maze, _players);

                    // When everything is ready, we start the game by sending the initial information to the players
                    sendInitialInformationToPlayers();
                    usleep(_preprocessingTime * 1000000);

                    // We start exchanging with the programs
                    // Every turn consists in checking if preprocessing is over, then sending turn information and applying decisions
                    bool ignoreTurn = false;
                    while (_maze->containsCheese())
                    {
                        checkIfPreprocessing();
                        _turnNumber++;
                        sendTurnInformationToPlayers(ignoreTurn, false);
                        usleep(_turnTime * 1000000);
                        ignoreTurn = movePlayers();
                        if (ignoreTurn)
                            _turnNumber--;
                        if (_gui && !ignoreTurn)
                            _gui->update(_maze, _players);
                    }

                    // Game is over
                    sendTurnInformationToPlayers(ignoreTurn, true);
                    showResult();

                }
                
            /**********************************************************************************************************************************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
            
        };
        
    #endif

/**********************************************************************************************************************************************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
