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
    #include <algorithm>
    #include <ctime>
    #include <string>
    #include <tuple>
    #include <unordered_map>
    #include <unordered_set>
    #include <vector>

    /** INTERNAL **/
    #include <Maze.cpp>
    #include <Player.cpp>
    #include <Shell.cpp>
    #include <ToString.cpp>
    
    /** NAMESPACES **/
    using namespace std;

/**********************************************************************************************************************************************************************************************************************************/
/************************************************************************************************************** CLASS *************************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
    
    #ifndef _RANDOM_MAZE_
    #define _RANDOM_MAZE_
        
        class RandomMaze : public Maze
        {
            
            /**********************************************************************************************************************************************************************************************************/
            /************************************************************************************************ CONSTANTS ***********************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Max number of moves required to cross mud
                
                /** CODE **/
                protected : const int MAX_MUD_VALUE = 10;
            
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Min number of moves required to cross mud
                
                /** CODE **/
                protected : const int MIN_MUD_VALUE = 2;
            
            /**********************************************************************************************************************************************************************************************************/
            /********************************************************************************************** CONSTRUCTORS **********************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Constructor for the random maze
                // Builds a maze using all given parameters
                
                /** CODE **/
                public : RandomMaze (int width, int height, double density, double mudProbability, int nbPiecesOfCheese, vector<Player*> players, bool symmetric) : Maze(players)
                {
                    
                    // Random seed
                    srand(time(0));
                    
                    // Information
                    string asymmetricString = (symmetric ? "" : "a");
                    Shell::getInstance().info("Creating random " + asymmetricString + "symmetric maze of size " + to_string(width) + "x" + to_string(height) + " with density " + double_to_string(density));
                    
                    // We create the maze map with or without symmetry and add pieces of cheese
                    createMap(width, height, density, mudProbability, symmetric);
                    addPiecesOfCheese(width, height, nbPiecesOfCheese, players, symmetric);
                    
                }
            
            /**********************************************************************************************************************************************************************************************************/
            /*********************************************************************************************** DESTRUCTOR ***********************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Empty destructor
                
                /** CODE **/
                public : virtual ~RandomMaze ()
                {}
                
            /**********************************************************************************************************************************************************************************************************/
            /************************************************************************************************* METHODS ************************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Adds the cheese to the maze randomly
                // The cheese is added symmetrically if asked
                
                /** CODE **/
                private : void addPiecesOfCheese (int width, int height, int nbPiecesOfCheese, vector<Player*> players, bool symmetric)
                {
                
                    // We check that the number of pieces of cheese asked can be placed in the maze
                    int nbCells = width * height;
                    int nbPlayers = players.size();
                    if ((symmetric && nbPiecesOfCheese > nbCells - 2) || (!symmetric && nbPiecesOfCheese > nbCells - nbPlayers))
                        Shell::getInstance().error("Cannot put the required number of pieces of cheese into the maze (not enough cells)");
                
                    // If symmetric, we cannot have an even number of cells and an odd number of pieces of cheese
                    if (symmetric && nbCells % 2 == 0 && nbPiecesOfCheese % 2 == 1)
                        Shell::getInstance().error("Cannot add an odd number of pieces of cheese to a maze with an even number of cells while ensuring symmetry");
                    
                    // In some cases, we know that a piece of cheese must be placed in the center of the maze
                    unordered_set<int> piecesOfCheese;
                    if (symmetric && nbPiecesOfCheese % 2 == 1)
                        piecesOfCheese.insert(nbCells / 2);
                    
                    // We put the possible cells that can receive a piece of cheese in a randomized vector
                    vector<int> allCells;
                    int upperBound = (symmetric ? nbCells / 2 : nbCells);
                    vector<int> locations = Maze::startingLocations();
                    for (int cell = 0 ; cell < upperBound ; cell++)
                        if ((cell != locations[0]) && !((symmetric || nbPlayers > 1) && cell == locations[1]))
                            allCells.push_back(cell);
                    random_shuffle(allCells.begin(), allCells.end());
                    
                    // We extract some cells until the chosen number of pieces of cheese is reached
                    while (piecesOfCheese.size() != (unsigned long)(nbPiecesOfCheese))
                    {
                        int cell = allCells.back();
                        allCells.pop_back();
                        piecesOfCheese.insert(cell);
                        if (symmetric)
                        {
                            int correspondingCell = nbCells - cell - 1;
                            piecesOfCheese.insert(correspondingCell);
                        }
                    }
                    
                    // We save the locations
                    Maze::setPiecesOfCheese(piecesOfCheese);
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Creates a random map for the maze
                // The map is symmetric if asked
                // Density 1 corresponds to the most dense connected maze
                
                /** CODE **/
                private : void createMap (int width, int height, double density, double mudProbability, bool symmetric)
                {
                    
                    // We create a vector of all walls and associate a distinct label to every pair of symmetric cells
                    vector<tuple<int, int>> walls;
                    unordered_map<int, int> cellsLabels;
                    int nbCells = width * height;
                    for (int cell1 = 0 ; cell1 < nbCells ; cell1++)
                    {
                        
                        // Creation of the wall
                        int cell1Line = cell1 / width;
                        int cell1Column = cell1 % width;
                        for (int cell2 = cell1 + 1 ; cell2 < nbCells ; cell2++)
                        {
                            int cell2Line = cell2 / width;
                            int cell2Column = cell2 % width;
                            if (abs(cell1Line - cell2Line) + abs(cell1Column - cell2Column) == 1)
                                walls.push_back(make_tuple(cell1, cell2));
                        }
                        
                        // Labels (considering the symmetry)
                        if (!symmetric || cell1 < (double)(nbCells) / 2.0)
                            cellsLabels[cell1] = cell1;
                        else
                            cellsLabels[cell1] = nbCells - cell1 - 1;
                        
                    }
                    
                    // We shuffle the walls and initilize the maze map
                    random_shuffle(walls.begin(), walls.end());
                    unordered_map<int, unordered_map<int, int>> map;
                    for (int cell = 0 ; cell < nbCells ; cell++)
                        map[cell] = {};
                    
                    // We join cells by removing walls until the maze is connected
                    while (true)
                    {
                        
                        // We remove the first wall we find that separates cells with distinct labels
                        tuple<int, int> wallToRemove = make_tuple(-1, -1);
                        for (auto& wall : walls)
                        {
                            if (cellsLabels[get<0>(wall)] != cellsLabels[get<1>(wall)])
                            {
                                wallToRemove = wall;
                                break;
                            }
                        }
                        
                        // If no such wall exists, the maze is connected
                        if (get<0>(wallToRemove) == -1)
                            break;
                        walls.erase(remove(walls.begin(), walls.end(), wallToRemove), walls.end());
                        
                        // We join the cells and fill the map
                        int labelToReplace = cellsLabels[get<1>(wallToRemove)];
                        int newLabel = cellsLabels[get<0>(wallToRemove)];
                        for (int cell = 0 ; cell < nbCells ; cell++)
                            if (cellsLabels[cell] == labelToReplace)
                                cellsLabels[cell] = newLabel;
                        int weight = randomEdgeWeight(mudProbability);
                        map[get<0>(wallToRemove)][get<1>(wallToRemove)] = weight;
                        map[get<1>(wallToRemove)][get<0>(wallToRemove)] = weight;

                        // We remove the symmetric wall (the labels are already updated)
                        if (symmetric)
                        {
                            tuple<int, int> symmetricWallToRemove = make_pair(nbCells - get<1>(wallToRemove) - 1, nbCells - get<0>(wallToRemove) - 1);
                            map[get<0>(symmetricWallToRemove)][get<1>(symmetricWallToRemove)] = weight;
                            map[get<1>(symmetricWallToRemove)][get<0>(symmetricWallToRemove)] = weight;
                            walls.erase(remove(walls.begin(), walls.end(), symmetricWallToRemove), walls.end());
                        }
                        
                    }
                    
                    // When the maze is symmetric and has an even number of cells, the previous algorithm produces 2 connected components, so we merge them by removing the maze center
                    if (symmetric && nbCells % 2 == 0)
                    {
                        vector<tuple<int, int>> centerWalls;
                        if (height % 2 == 1)
                            centerWalls.push_back(make_pair(nbCells / 2 - 1, nbCells / 2));
                        else if (width % 2 == 1)    
                            centerWalls.push_back(make_pair(nbCells / 2 - width / 2 - 1, nbCells / 2 + width / 2));
                        else
                        {
                            centerWalls.push_back(make_pair(nbCells / 2 - width / 2 - 1, nbCells / 2 - width / 2));
                            centerWalls.push_back(make_pair(nbCells / 2 - width / 2 - 1, nbCells / 2 + width / 2 - 1));
                            centerWalls.push_back(make_pair(nbCells / 2 - width / 2, nbCells / 2 + width / 2));
                            centerWalls.push_back(make_pair(nbCells / 2 + width / 2 - 1, nbCells / 2 + width / 2));
                        }
                        for (auto& wall : centerWalls)
                        {
                            int weight = randomEdgeWeight(mudProbability);
                            map[get<0>(wall)][get<1>(wall)] = weight;
                            map[get<1>(wall)][get<0>(wall)] = weight;
                            walls.erase(remove(walls.begin(), walls.end(), wall), walls.end());
                        }
                    }
                    
                    // We remove walls to match the requested density, considering that density 1 is the connected graph
                    int nbWallsForDensity1 = walls.size();
                    while (walls.size() > density * nbWallsForDensity1)
                    {
                        
                        // Suppression of a wall
                        tuple<int, int> wall = walls.back();
                        int weight = randomEdgeWeight(mudProbability);
                        map[get<0>(wall)][get<1>(wall)] = weight;
                        map[get<1>(wall)][get<0>(wall)] = weight;
                        walls.pop_back();
                        
                        // We remove the symmetric wall
                        if (symmetric)
                        {
                            tuple<int, int> symmetricWall = make_pair(nbCells - get<1>(wall) - 1, nbCells - get<0>(wall) - 1);
                            map[get<0>(symmetricWall)][get<1>(symmetricWall)] = weight;
                            map[get<1>(symmetricWall)][get<0>(symmetricWall)] = weight;
                            walls.erase(remove(walls.begin(), walls.end(), symmetricWall), walls.end());
                        }
                        
                    }
                    
                    // We save the map
                    Maze::setMap(map, width, height);
                    
                }
            
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Returns a random weight for an existing edge
                
                /** CODE **/
                private : int randomEdgeWeight (double mudProbability)
                {

                    // We test if we have mud
                    if (double(rand()) / RAND_MAX < mudProbability)
                        return rand() % (MAX_MUD_VALUE - 1) + MIN_MUD_VALUE;
                    return 1;
                    
                }
            
            /**********************************************************************************************************************************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
            
        };
        
    #endif

/**********************************************************************************************************************************************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
