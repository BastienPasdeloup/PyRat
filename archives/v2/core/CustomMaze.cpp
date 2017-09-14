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
    #include <string>
    #include <unordered_map>
    #include <unordered_set>

    /** INTERNAL **/
    #include <Maze.cpp>
    #include <Shell.cpp>
    #include <TypeConverter.cpp>
    
    /** NAMESPACES **/
    using namespace std;

/**********************************************************************************************************************************************************************************************************************************/
/************************************************************************************************************** CLASS *************************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
    
    #ifndef _CUSTOM_MAZE_
    #define _CUSTOM_MAZE_
        
        class CustomMaze : public Maze
        {
            
            /**********************************************************************************************************************************************************************************************************/
            /********************************************************************************************** CONSTRUCTORS **********************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Constructor using a custom maze file
                
                /** CODE **/
                public : CustomMaze (string fileName, vector<Player*> players) : Maze(players)
                {
                    
                    // Information
                    Shell::getInstance().info("Creating maze from file " + fileName);
                    
                    // We extract the information from the file
                    loadMazeFromFile(fileName);
                    loadPiecesOfCheeseFromFile(fileName);
                    
                }
            
            /**********************************************************************************************************************************************************************************************************/
            /*********************************************************************************************** DESTRUCTOR ***********************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Empty destructor
                
                /** CODE **/
                public : virtual ~CustomMaze ()
                {}
                
            /**********************************************************************************************************************************************************************************************************/
            /************************************************************************************************* METHODS ************************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Loads the pieces of cheese from the maze file
                
                /** CODE **/
                private : void loadPiecesOfCheeseFromFile (string fileName)
                {
                    
                    // We read the interesting tags in the file
                    TypeConverter converter;
                    int width = converter.toInt(readTagLine(fileName, Maze::WIDTH_TAG));
                    unordered_set<int> piecesOfCheese = toCheeseSet(readTagLine(fileName, Maze::CHEESE_TAG), width);
                    
                    // We save the locations
                    Maze::setPiecesOfCheese(piecesOfCheese);
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Loads the maze map from the maze file
                
                /** CODE **/
                private : void loadMazeFromFile (string fileName)
                {
                    
                    // We read the interesting tags in the file
                    TypeConverter converter;
                    int height = converter.toInt(readTagLine(fileName, Maze::HEIGHT_TAG));
                    int width = converter.toInt(readTagLine(fileName, Maze::WIDTH_TAG));
                    unordered_map<int, unordered_map<int, int>> map = toMap(readTagLine(fileName, Maze::MAP_TAG), width, height);
                    
                    // We save the map
                    Maze::setMap(map, width, height);
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Reads the text corresponding to a given tag in the maze file
                
                /** CODE **/
                private : string readTagLine (string fileName, string tagToFind)
                {
                    
                    // We keep a set of the other tags we may find
                    unordered_set<string> otherTags;
                    if (tagToFind != Maze::CHEESE_TAG)
                        otherTags.insert(Maze::CHEESE_TAG);
                    if (tagToFind != Maze::HEIGHT_TAG)
                        otherTags.insert(Maze::HEIGHT_TAG);
                    if (tagToFind != Maze::WIDTH_TAG)
                        otherTags.insert(Maze::WIDTH_TAG);
                    if (tagToFind != Maze::MAP_TAG)
                        otherTags.insert(Maze::MAP_TAG);
                    
                    // We open the file and read its contents
                    ifstream inputFile(fileName);
                    string line;
                    string tagString;
                    bool tagFound = false;
                    while (getline(inputFile, line))
                    {
                        line.erase(remove(line.begin(), line.end(), ' '), line.end());
                        if (line.substr(0, tagToFind.size()) == tagToFind)
                        {
                            tagFound = true;
                            line.erase(0, tagToFind.size());
                        }
                        if (tagFound)
                        {
                            if (line.substr(0, Maze::COMMENT_TAG.size()) == Maze::COMMENT_TAG)
                                continue;
                            else
                            {
                                bool newTagStarted = false;
                                for (auto& otherTag : otherTags)
                                {
                                    if (line.substr(0, otherTag.size()) == otherTag)
                                    {
                                        newTagStarted = true;
                                        break;
                                    }
                                }
                                if (newTagStarted)
                                    break;
                            }
                            tagString += line;
                        }
                    }
                    
                    // Verification that we have found the tag
                    if (!tagFound)
                        Shell::getInstance().error("Could not find the " + tagToFind + " tag");
                    
                    // Done
                    return tagString;
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/

                /** DOCUMENTATION **/
                // Transforms the string representing the nice cheese locations into the corresponding set of ints
                
                /** CODE **/
                private : unordered_set<int> toCheeseSet (string cheeseString, int width)
                {
                    
                    // We iterate over the pieces of cheese
                    cheeseString = cheeseString.substr(0, cheeseString.size() - 1);
                    TypeConverter converter;
                    unordered_set<int> ints;
                    string cheeseEntry;
                    stringstream cheeseEntryStream(cheeseString);
                    while (getline(cheeseEntryStream, cheeseEntry, ')'))
                    {
                        cheeseEntry = cheeseEntry.substr(2, cheeseEntry.size() - 1);
                        int separatorIndex = cheeseEntry.find_first_of(",");
                        int cheese = converter.toInt(cheeseEntry.substr(0, separatorIndex)) * width + converter.toInt(cheeseEntry.substr(separatorIndex + 1));
                        ints.insert(cheese);
                    }
                    
                    // Done
                    return ints;
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/

                /** DOCUMENTATION **/
                // Transforms the string representing the nice map into the corresponding map of ints
                
                /** CODE **/
                private : unordered_map<int, unordered_map<int, int>> toMap (string mapString, int width, int height)
                {
                    
                    // We transform the string into a data structure
                    TypeConverter converter;
                    unordered_map<int, unordered_map<int, int>> map;
                    mapString = mapString.substr(0, mapString.size() - 1);
                    string mapStringEntry;
                    stringstream mapStringStream(mapString);
                    while (getline(mapStringStream, mapStringEntry, '}'))
                    {
                        
                        // Separation key/value
                        mapStringEntry.erase(0, 1);
                        int separatorIndexKeyValue = mapStringEntry.find_first_of("{");
                        string key1String = mapStringEntry.substr(0, separatorIndexKeyValue - 1);
                        string value1String = mapStringEntry.substr(separatorIndexKeyValue + 2, mapStringEntry.size() - separatorIndexKeyValue - 1);
                        
                        // Key 1
                        int separatorIndexLineColumn = key1String.find_first_of(",");
                        int key1 = converter.toInt(key1String.substr(1, separatorIndexLineColumn - 1)) * width + converter.toInt(key1String.substr(separatorIndexLineColumn + 1, key1String.size() - separatorIndexLineColumn - 2));
                        map[key1] = {};
                        
                        // Value 1
                        string value1StringEntry;
                        stringstream value1StringStream(value1String);
                        while (getline(value1StringStream, value1StringEntry, '('))
                        {
                            
                            // Key 2
                            if (value1StringEntry[value1StringEntry.size() - 1] == ',')
                                value1StringEntry = value1StringEntry.substr(0, value1StringEntry.size() - 1);
                            int separatorIndexLine = value1StringEntry.find_first_of(",");
                            int separatorIndexColumn = value1StringEntry.find_first_of(")");
                            int key2 = converter.toInt(value1StringEntry.substr(0, separatorIndexLine)) * width + converter.toInt(value1StringEntry.substr(separatorIndexLine + 1, separatorIndexColumn - 1));

                            // Value 2
                            int value2 = converter.toInt(value1StringEntry.substr(separatorIndexColumn + 2));
                            map[key1][key2] = value2;
                            
                        }
                        
                    }
                    
                    // We check that the madjacency matrix is symmetric
                    for (auto& cell1 : map)
                        for (auto& cell2 : cell1.second)
                            if (map[cell2.first].find(cell1.first) == map[cell2.first].end() || map[cell2.first][cell1.first] != cell2.second)
                                Shell::getInstance().error("Maze map is not bidirectional (there are <em>a</em> and <em>b</em> s.t. <em>mazeMap[a][b] != mazeMap[b][a]</em>)");
                    
                    // We check that the maze is connected
                    unordered_set<int> visitedCells;
                    unordered_set<int> cellsToVisit = {0};
                    while (!cellsToVisit.empty())
                    {
                        int nextCell = *cellsToVisit.begin();
                        cellsToVisit.erase(cellsToVisit.begin());
                        visitedCells.insert(nextCell);
                        for (auto& neighbor : map[nextCell])
                            if (visitedCells.find(neighbor.first) == visitedCells.end())
                                cellsToVisit.insert(neighbor.first);
                    }
                    if (visitedCells.size() != (unsigned int)(width * height))
                        Shell::getInstance().warning("Maze map is not connected (some cells cannot be reached)");
                    
                    // Done
                    return map;
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
            
        };
        
    #endif

/**********************************************************************************************************************************************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
