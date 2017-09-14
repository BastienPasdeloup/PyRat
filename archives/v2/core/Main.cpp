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
    #include <cstdlib>
    #include <string>
    #include <unordered_map>
    #include <unordered_set>
    #include <vector>
    
    /** INTERNAL **/
    #include <ArgumentsParser.cpp>
    #include <GUI.cpp>
    #include <Player.cpp>
    #include <PyRatGame.cpp>
    #include <CustomMaze.cpp>
    #include <RandomMaze.cpp>
    #include <Shell.cpp>
    #include <TypeConverter.cpp>
    
    /** NAMESPACES **/
    using namespace std;
    
/**********************************************************************************************************************************************************************************************************************************/
/*********************************************************************************************************** ENTRY POINT **********************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/

    /** DOCUMENTATION **/
    // Entry point of the program
    // Parses the command line arguments, initializes the game elements and performs the game
    
    /** CODE **/
    int main (int argc, char** argv)
    {

        // Initialization of the GUI
        Shell::getInstance().start();
        try
        {
        
            // We parse the input
            Shell::getInstance().info("Parsing command line");
            ArgumentsParser parser;
            TypeConverter converter;
            unordered_set<string> compulsoryArguments = {"-ip1", "-port1", "-closeAtEnd"};
            unordered_map<string, string> optionalArguments = {{"-mudProbability", "0.0"}, {"-preprocessingTime", "0.0"}, {"-turnTime", "0.0"}, {"-synchronicity", ""}, {"-outputDirectory", "."}, {"-gameID", ""}, {"-ipGUI", "127.0.0.1"}, {"-portGUI", to_string(converter.getMinPort())}, {"-ip2", "127.0.0.1"}, {"-port2", to_string(converter.getMinPort())}, {"-mazeWidth", "2"}, {"-mazeHeight", "2"}, {"-mazeDensity", "0.0"}, {"-mazeSymmetric", "false"}, {"-mazeFileName", "."}, {"-nbPiecesOfCheese", "1"}};
            unordered_map<string, tuple<bool, string>> arguments = parser.argumentsToMap(argc, argv, compulsoryArguments, optionalArguments);
            
            // We update the shell with the closing information as soon as possible
            Shell::getInstance().info("Checking game configuration");
            bool closeAtEnd = converter.toBool(get<1>(arguments["-closeAtEnd"]));
            if (closeAtEnd)
                Shell::getInstance().forceCloseAtEnd();
            
            // We check that sufficient optional arguments are defined to create a maze
            if (!(get<0>(arguments["-mazeFileName"]) ^ (get<0>(arguments["-mudProbability"]) && get<0>(arguments["-mazeWidth"]) && get<0>(arguments["-mazeHeight"]) && get<0>(arguments["-mazeDensity"]) && get<0>(arguments["-nbPiecesOfCheese"]) && get<0>(arguments["-mazeSymmetric"]))))
                Shell::getInstance().error("You must provide one valid maze description (either using option -mazeFileName or describing it using options -mazeWidth, -mazeHeight, -mazeDensity, -mudProbability, -nbPiecesOfCheese and -mazeSymmetric)");
            
            // If the game has 2 players, all connection information must be provided
            if (get<0>(arguments["-ip2"]) ^ get<0>(arguments["-port2"]))
                Shell::getInstance().error("When asking for a two players game, you must provide a full connection description for player 2 using options -ip2 and -port2");
            
            // If the game has a GUI, all connection information must be provided
            if (get<0>(arguments["-ipGUI"]) ^ get<0>(arguments["-portGUI"]))
                Shell::getInstance().error("When asking for a game with a GUI, you must provide a full connection description for GUI using options -ipGUI and -portGUI");
            
            // We check if the times are provided or if the game is synchronous
            if (get<0>(arguments["-preprocessingTime"]) ^ get<0>(arguments["-turnTime"]))
                Shell::getInstance().error("When asking for an asynchronous game, you must provide a full timing description using options -preprocessingTime and -turnTime");
            
            // The game cannot be both synchronous and asynchronous
            if (get<0>(arguments["-turnTime"]) == get<0>(arguments["-synchronicity"]))
                Shell::getInstance().error("A timing description must be provided using options -preprocessingTime and -turnTime, or a synchronicity mode must be set using option -synchronicity");
            
            // If the game is synchronous, we check which sort of synchronicity
            if (get<0>(arguments["-synchronicity"]) && get<1>(arguments["-synchronicity"]) != string("synchronous") && get<1>(arguments["-synchronicity"]) != string("semi-synchronous"))
                Shell::getInstance().error("When asking for a synchronous game, you must precise if it is fully synchronous or semi-synchonous using option -synchronicity");
                
            // We check if an export is asked
            if (get<0>(arguments["-outputDirectory"]) ^ get<0>(arguments["-gameID"]))
                Shell::getInstance().error("When asking for an export of the game, you must provide a full export description using options -outputDirectory and -gameID");
            
            // We check the types of the remaining arguments
            string ipGUI = converter.toIP(get<1>(arguments["-ipGUI"]));
            int portGUI = converter.toPort(get<1>(arguments["-portGUI"]));
            string ipPlayer1 = converter.toIP(get<1>(arguments["-ip1"]));
            int portPlayer1 = converter.toPort(get<1>(arguments["-port1"]));
            string ipPlayer2 = converter.toIP(get<1>(arguments["-ip1"]));
            int portPlayer2 = converter.toPort(get<1>(arguments["-port2"]));
            int mazeWidth = converter.toIntGreaterThan(get<1>(arguments["-mazeWidth"]), 2);
            int mazeHeight = converter.toIntGreaterThan(get<1>(arguments["-mazeHeight"]), 2);
            double mazeDensity = converter.toDoubleInBounds(get<1>(arguments["-mazeDensity"]), 0.0, 1.0);
            bool mazeSymmetric = converter.toBool(get<1>(arguments["-mazeSymmetric"]));
            string mazeFileName = converter.toPath(get<1>(arguments["-mazeFileName"]));
            string outputDirectory = converter.toPath(get<1>(arguments["-outputDirectory"]));
            string gameID = get<1>(arguments["-gameID"]);
            int nbPiecesOfCheese = converter.toIntGreaterThan(get<1>(arguments["-nbPiecesOfCheese"]), 1);
            double mudProbability = converter.toDoubleInBounds(get<1>(arguments["-mudProbability"]), 0.0, 1.0);
            double preprocessingTime = converter.toDoubleGreaterThan(get<1>(arguments["-preprocessingTime"]), 0.0);
            double turnTime = converter.toDoubleGreaterThan(get<1>(arguments["-turnTime"]), 0.0);
            string synchronicity = get<1>(arguments["-synchronicity"]);

            // We initialize the GUI
            GUI* gui = nullptr;
            if (get<0>(arguments["-ipGUI"]))
                gui = new GUI(ipGUI, portGUI);
            
            // We initialize the players
            vector<Player*> players = {new Player(ipPlayer1, portPlayer1, 1, synchronicity == string("synchronous"))};
            if (get<0>(arguments["-ip2"]))
                players.push_back(new Player(ipPlayer2, portPlayer2, 2, synchronicity == string("synchronous")));
            
            // We initialize the maze
            Maze* maze;
            if (get<0>(arguments["-mazeFileName"]))
                maze = new CustomMaze(mazeFileName, players);
            else
                maze = new RandomMaze(mazeWidth, mazeHeight, mazeDensity, mudProbability, nbPiecesOfCheese, players, mazeSymmetric);

            // We play the game with the given arguments
            PyRatGame game(maze, gui, players, preprocessingTime, turnTime, synchronicity);
            game.start();
            
            // When the game is over, we save its components if asked
            if (get<0>(arguments["-outputDirectory"]))
            {
                Shell::getInstance().info("Saving the game to directory \"" + outputDirectory + "\"");
                maze->save(outputDirectory);
                for (auto player : players)
                    player->save(outputDirectory);
                if (players.size() == 1)
                    remove(Player::getOutputFileName(outputDirectory, 2).c_str());
                game.save(outputDirectory, gameID);
            }
            
            // We close the GUI at the end
            Shell::getInstance().stop(false);
            return EXIT_SUCCESS;
        
        }
        
        // In case of an uncaught exception, we print it to the shell
        catch (const exception& e)
        {
            Shell::getInstance().error(e.what());
        }
        
    }

/**********************************************************************************************************************************************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
