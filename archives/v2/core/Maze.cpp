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
    #include <unordered_map>
    #include <unordered_set>
    #include <vector>
    
    /** INTERNAL **/
    #include <Moves.cpp>
    #include <Shell.cpp>
    
    /** NAMESPACES **/
    using namespace std;

/**********************************************************************************************************************************************************************************************************************************/
/************************************************************************************************************** CLASS *************************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
    
    #ifndef _MAZE_
    #define _MAZE_
        
        class Maze
        {
            
            /**********************************************************************************************************************************************************************************************************/
            /************************************************************************************************ CONSTANTS ***********************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Tag to write in the export file to indicate the cheese locations
                
                /** CODE **/
                protected : const string CHEESE_TAG = "[CHEESE]";
            
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Tag to write in the export file to indicate the comments
                
                /** CODE **/
                protected : const string COMMENT_TAG = "#";
            
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Tag to write in the export file to indicate the maze height
                
                /** CODE **/
                protected : const string HEIGHT_TAG = "[HEIGHT]";
            
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Tag to write in the export file to indicate the maze map
                
                /** CODE **/
                protected : const string MAP_TAG = "[MAP]";
            
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Name of the file where to export the maze
                
                /** CODE **/
                private : const string OUTPUT_FILE_NAME = "maze.txt";
            
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Tag to write in the export file to indicate the maze width
                
                /** CODE **/
                protected : const string WIDTH_TAG = "[WIDTH]";
            
            /**********************************************************************************************************************************************************************************************************/
            /*********************************************************************************************** ATTRIBUTES ***********************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Height of the maze in number of cells
                
                /** CODE **/
                private : int _height;
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Map of the maze
                // Cells are numbered from 0 (top left) to _height * _width - 1 (bottom right) in lexical order
                
                /** CODE **/
                private : unordered_map<int, unordered_map<int, int>> _map;
            
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Locations of the remaining pieces of cheese
                
                /** CODE **/
                private : unordered_set<int> _piecesOfCheese;
            
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Locations of the pieces of cheese at the beginning of the game
                
                /** CODE **/
                private : unordered_set<int> _piecesOfCheeseAtBeginning;
            
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Destinations of the players that are crossing mud
                
                /** CODE **/
                private : unordered_map<Player*, int> _playersCurrentCrossings;
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Locations of the players in the maze
                
                /** CODE **/
                private : unordered_map<Player*, int> _playersCurrentLocations;
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Width of the maze in number of cells
                
                /** CODE **/
                private : int _width;
                
            /**********************************************************************************************************************************************************************************************************/
            /********************************************************************************************** CONSTRUCTORS **********************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Constructor with the players
                
                /** CODE **/
                protected : Maze (vector<Player*> players)
                {
                    
                    // We initialize the players locations with default values until the maze is loaded
                    // -1 is used for player 1 and -2 for player 2 (to find them in the unordered map)
                    for (unsigned int i = 1 ; i <= players.size() ; i++)
                        _playersCurrentLocations[players[i - 1]] = -i;
                    
                }
            
            /**********************************************************************************************************************************************************************************************************/
            /*********************************************************************************************** DESTRUCTOR ***********************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Empty destructor
                
                /** CODE **/
                protected : virtual ~Maze ()
                {}
                
            /**********************************************************************************************************************************************************************************************************/
            /************************************************************************************************* METHODS ************************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Indicates if all players are currently on the same cell
                // Returns the identifier of the cell if it is the case, -1 otherwise
                
                /** CODE **/
                private : int allPlayersOnSameCell ()
                {
                    
                    // We check the map
                    int previousCell = -1;
                    for (auto& playerLocation : _playersCurrentLocations)
                    {
                        if (previousCell == -1)
                            previousCell = playerLocation.second;
                        if (playerLocation.second != previousCell)
                            return -1;
                    }
                    return previousCell;
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Returns a nice string representing the given set of cheese
                // The locations are written in the form (line, column)
                
                /** CODE **/
                private : string cheeseToString (unordered_set<int> cheeseToConvert)
                {
                    
                    // We return a string representing the locations of the pieces of cheese with every location written as (line, column)
                    string piecesOfCheeseAsString = "[";
                    for (auto& cheese : cheeseToConvert)
                    {
                        int cheeseLine = cheese / _width;
                        int cheeseColumn = cheese % _width;
                        piecesOfCheeseAsString += "(" + to_string(cheeseLine) + ", " + to_string(cheeseColumn) + "), ";
                    }
                    piecesOfCheeseAsString += "]";
                    piecesOfCheeseAsString = regex_replace(piecesOfCheeseAsString, regex(", ]"), "]");
                    
                    // Done
                    return piecesOfCheeseAsString;
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Indicates if cheese is remaining in the maze
                
                /** CODE **/
                public : bool containsCheese ()
                {
                    
                    // Checks if there is cheese remaining in the maze
                    return !_piecesOfCheese.empty();
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Getter for the maze height
                
                /** CODE **/
                public : int getHeight ()
                {
                    
                    // Getter for the height attribute
                    return _height;
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Returns the player location as a nice string (line, column)
                
                /** CODE **/
                public : string getNiceCurrentPlayerLocation (Player* player)
                {
                    
                    // Returns the pair (line, column) representing the player's location
                    return "(" + to_string(_playersCurrentLocations[player] / _width) + ", " + to_string(_playersCurrentLocations[player] % _width) + ")";
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Returns the number of moves it takes to the player to go to the target cell
                
                /** CODE **/
                public : int getPlayerCurrentCrossing (Player* player)
                {
                    
                    // We return the number of moves required to go there
                    return _playersCurrentCrossings[player];
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Getter for the maze width
                
                /** CODE **/
                public : int getWidth ()
                {
                    
                    // We return the width attribute
                    return _width;
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Returns the locations that can be used as starting locations
                // The first player will be in the bottom left corner
                // The second one will be in the top right corner
                
                /** CODE **/
                protected : vector<int> startingLocations ()
                {
                    
                    // The first registered player will go to the bottom-left cell, and the second to the top-right cell
                    return {_width * (_height - 1), _width - 1};
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Initializes the locations of the players at the beginning of the game
                
                /** CODE **/
                private : void initializePlayersLocations ()
                {
                    
                    // The first registered player will go to the bottom-left cell, and the second to the top-right cell
                    vector<int> locations = startingLocations();
                    for (auto& playerLocation : _playersCurrentLocations)
                    {
                        int startingLocation = (playerLocation.second == -1) ? locations[0] : locations[1];
                        _playersCurrentLocations[playerLocation.first] = startingLocation;
                    }
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Setter for the maze map
                // Must be called by the inheriting classes
                
                /** CODE **/
                protected : void setMap (unordered_map<int, unordered_map<int, int>> map, int width, int height)
                {
                    
                    // We set the attributes
                    _map = map;
                    _width = width;
                    _height = height;
                    
                    // We initialize the initial players locations
                    initializePlayersLocations();
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Returns a string representing the map with nice locations (line, column)
                
                /** CODE **/
                public : string mapToString ()
                {
                    
                    // We return a string representing the map with every cell written as (line, column)
                    string mapAsString = "{";
                    for (int cell1 = 0 ; cell1 < _width * _height ; cell1++)
                    {
                        int cell1Line = cell1 / _width;
                        int cell1Column = cell1 % _width;
                        mapAsString += "(" + to_string(cell1Line) + ", " + to_string(cell1Column) + ") : {";
                        for (auto& cell2 : _map[cell1])
                        {
                            
                            int cell2Line = cell2.first / _width;
                            int cell2Column = cell2.first % _width;
                            int edgeWeight = cell2.second;
                            mapAsString += "(" + to_string(cell2Line) + ", " + to_string(cell2Column) + ") : " + to_string(edgeWeight) + ", ";
                        }
                        mapAsString += "}, ";
                    }
                    mapAsString += "}";
                    mapAsString = regex_replace(mapAsString, regex(", }"), "}");

                    // Done
                    return mapAsString;
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Moves the player in the maze according to their decisions
                // If the player is stuck in mud, we make it advance
                
                /** CODE **/
                public : void movePlayer (Player* player)
                {
                    
                    // We compute the location associated to the last received move
                    int playerLine = _playersCurrentLocations[player] / _width;
                    int playerColumn = _playersCurrentLocations[player] % _width;
                    if (player->getMove() == MOVE_UP)
                        playerLine--;
                    else if (player->getMove() == MOVE_DOWN)
                        playerLine++;
                    else if (player->getMove() == MOVE_LEFT)
                        playerColumn--;
                    else if (player->getMove() == MOVE_RIGHT)
                        playerColumn++;
                    int potentialNewPlayerLocation = playerLine * _width + playerColumn;
                    
                    // We determine the weight of the path
                    int weight = 0;
                    if (playerLine >= 0 && playerLine < _height && playerColumn >= 0 && playerColumn < _width && _map[_playersCurrentLocations[player]].find(potentialNewPlayerLocation) != _map[_playersCurrentLocations[player]].end())
                        weight = _map[_playersCurrentLocations[player]][potentialNewPlayerLocation];
                    _playersCurrentCrossings[player] = weight;
                    
                    // If the move is invalid/missed or leads to a wall, we stop
                    if (weight == 0)
                        return;
                    
                    // If we are initiating a new move, we update the blockings
                    if (!player->inMud())
                        player->block(weight);
                    
                    // Otherwise, we advance in this direction
                    player->reduceBlocking();
                    
                    // If we are still in mud, nothing needs to be done
                    if (player->inMud())
                        return;
                    
                    // Otherwise, we have reached our destination
                    _playersCurrentLocations[player] = potentialNewPlayerLocation;
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Returns a string representing the remaining cheese in the form (line, column)
                
                /** CODE **/
                public : string piecesOfCheeseToString ()
                {
                    
                    // We return the representation of the cheese list
                    return cheeseToString(_piecesOfCheese);
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Saves the maze elements in the export file
                // Uses tags to separate the various elements
                // These tags are parsed when using a custom maze
                
                /** CODE **/
                public : void save (string outputDirectory)
                {
                    
                    // We create the destination file
                    fstream outputFile;
                    outputFile.open(outputDirectory + "/" + OUTPUT_FILE_NAME, fstream::trunc | fstream::out);
                    
                    // We export the dimensions of the maze and its map, in addition to the pieces of cheese
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
                    outputFile << "# Dimensions of the maze" << endl;
                    outputFile << HEIGHT_TAG << " " << to_string(_height) << endl;
                    outputFile << WIDTH_TAG << " " << to_string(_width) << endl << endl;
                    outputFile << "# Map of the maze" << endl;
                    outputFile << MAP_TAG << " " << mapToString() << endl << endl;
                    outputFile << "# Pieces of cheese" << endl;
                    outputFile << CHEESE_TAG << " " << cheeseToString(_piecesOfCheeseAtBeginning) << endl << endl;
                    outputFile << "####################################################################################################################################################################################################################################" << endl;
                    outputFile << "####################################################################################################################################################################################################################################";
                    
                    // Done
                    outputFile.close();
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Sets the pieces of cheese at the beginning of the game
                // Must be called by the inheriting classes
                
                /** CODE **/
                protected : void setPiecesOfCheese (unordered_set<int> piecesOfCheese)
                {
                    
                    // We set the attribute
                    _piecesOfCheese = piecesOfCheese;
                    _piecesOfCheeseAtBeginning = piecesOfCheese;
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // After the moves are performed, updates the players scores and the remaining cheese
                
                /** CODE **/
                public : void updateCheese ()
                {

                    // We check all cheese
                    int cellWithAllPlayers = allPlayersOnSameCell();
                    vector<int> cheeseToRemove;
                    for (auto& cheese : _piecesOfCheese)
                    {

                        // If both players are on the same cell, they may share the cheese
                        if (_playersCurrentLocations.size() > 1 && cellWithAllPlayers == cheese)
                        {
                            Shell::getInstance().info("Players share a piece of cheese together in a nice and friendly atmosphere");
                            for (auto& playerLocation : _playersCurrentLocations)
                                playerLocation.first->eatCheese(1.0 / double(_playersCurrentLocations.size()));
                            cheeseToRemove.push_back(cheese);
                        }
                        
                        // If there is only one player or both are in different cells, the cheese cannot be shared
                        else
                        {
                            for (auto& playerLocation : _playersCurrentLocations)
                            {
                                if (playerLocation.second == cheese)
                                {
                                    Shell::getInstance().info("<b>" + playerLocation.first->getName() + "</b> eats a piece of cheese");
                                    playerLocation.first->eatCheese(1.0);
                                    cheeseToRemove.push_back(cheese);
                                    break;
                                }
                            }
                        }
                        
                    }
                    
                    // We remove the cheese that was taken
                    for (auto& cheese : cheeseToRemove)
                        _piecesOfCheese.erase(cheese);

                }
                
            /**********************************************************************************************************************************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
            
        };
        
    #endif

/**********************************************************************************************************************************************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
