<?php
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
/************************************************************************************************************ INCLUDES ************************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/

    /** INTERNAL **/
    include "database.php";
    include "htmlElements.php";
    include "networkServer.php";
    
/**********************************************************************************************************************************************************************************************************************************/
/************************************************************************************************************ FUNCTIONS ***********************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Creates a new game viewer using the given address and port to establish a server
    
    /** CODE **/
    function createNewGame ($addressArgument, $portArgument)
    {
        
        // We reserve a game ID in the database
        $gameID = reserveNewGame();
        if (is_string($gameID))
            showErrorPage($gameID);
        
        // We start a script to fill the database when messages are received from the core program
        exec("./php game.php ".escapeshellarg($addressArgument)." ".escapeshellarg($portArgument)." ".escapeshellarg($gameID)." > /dev/null 2>/dev/null &");
        
        // We wait until the game is created
        while (true)
        {
            
            // Game info
            $gameStatus = getNewGameStatus($gameID);
            if (is_string($gameStatus))
                showErrorPage($gameStatus);
            
            // -1 in the status indicates an error occurred
            $row = nextEntry($gameStatus);
            if ($row["status"] < 0)
                showErrorPage($row["message"]);
            else if ($row["status"] > 0)
                break;
            
        }

        // We join the game when it is created
        joinGame($gameID);
        
    }

/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Connects the viewer to the game asked by the user
    
    /** CODE **/
    function joinGame ($gameArgument)
    {
        
        // We get the game description
        $game = intval($gameArgument);
        $gameInfo = getGameInfo($game);
        if (is_string($gameInfo))
            showErrorPage($gameInfo);
        
        // We extract the useful information
        $row = nextEntry($gameInfo);
        $mazeMap = fieldToStruct($row["map"]);
        $piecesOfCheese = fieldToStruct($row["piecesOfCheese"]);
        $width = $row["width"];
        $height = $row["height"];
        $player1Name = $row["name"];
        $player1StartingLocation = $row["startingLocation"];
        $row = nextEntry($gameInfo);
        $player2Name = (is_null($row) ? "" : $row["name"]);
        $player2StartingLocation = (is_null($row) ? "" : $row["startingLocation"]);
        
        // We initialize the page
        $player1Area = playerToHTML($player1Name, 1, is_null($row));
        $player2Area = (is_null($row) ? "" : playerToHTML($player2Name, 2, false));
        $mazeArea = mazeToHTML($game, $mazeMap, $piecesOfCheese, $width, $height, $player1StartingLocation, $player2StartingLocation);
        $messagesArea = "Preprocessing step\n";
        if (is_null($row))
            showPage($mazeArea, $player1Area["description"], $player1Area["score"], $messagesArea, true);
        else
            showPage($mazeArea, $player1Area, $player2Area, $messagesArea, true);
        
    }

/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Sents the moves associated to the players for the given game and time to the GUI
    
    /** CODE **/
    function returnMove ($gameArgument, $moveArgument)
    {
        
        // We get the required move for the required game
        $game = intval($gameArgument);
        $move = intval($moveArgument);
        $moveInfo = getMove($game, $move);
        if (is_string($moveInfo))
            showErrorPage($moveInfo);
        
        // If the information does not exist, we do nothing
        $row = nextEntry($moveInfo);
        if (is_null($row))
        {
            echo "{}";
            return;
        }
        
        // We extract the useful information
        $player1Direction = $row["direction"];
        $player1Duration = $row["duration"];
        $player1ScoreAfter = $row["scoreAfter"];
        $player1CheeseToRemoveAfter = $row["cheeseToRemoveAfter"];
        $row = nextEntry($moveInfo);
        $player2Direction = (is_null($row) ? "" : $row["direction"]);
        $player2Duration = (is_null($row) ? "" : $row["duration"]);
        $player2ScoreAfter = (is_null($row) ? "" : $row["scoreAfter"]);
        $player2CheeseToRemoveAfter = (is_null($row) ? "" : $row["cheeseToRemoveAfter"]);
        
        // String to return
        echo "{\"moves\" : [\"".$player1Direction.(is_null($row) ? "" : "\", \"".$player2Direction)."\"],".
             "\"durations\" : [\"".$player1Duration.(is_null($row) ? "" : "\", \"".$player2Duration)."\"], ".
             "\"scoresAfter\" : [\"".$player1ScoreAfter.(is_null($row) ? "" : "\", \"".$player2ScoreAfter)."\"], ".
             "\"cheeseToRemoveAfter\" : [\"".$player1CheeseToRemoveAfter.(is_null($row) ? "" : "\", \"".$player2CheeseToRemoveAfter)."\"]}";
        
    }

/**********************************************************************************************************************************************************************************************************************************/
/*********************************************************************************************************** ENTRY POINT **********************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Main entry point
    // Checks the URL arguments to determine the execution mode of the page
    // If no argument is set, we show a page to select a game to start
    
    /** CODE **/
    function main ()
    {
        
        // If a game is running and we are asking for a move, we return it
        if (isset($_POST["move"]))
        {
            if (!isset($_POST["game"]))
                showErrorPage("Game ID is not provided");
            else
                returnMove($_POST["game"], $_POST["move"]);
        }
        
        // If a game ID is provided, we join it
        elseif (isset($_GET["game"]))
            joinGame($_GET["game"]);
        
        // If an address/port is provided, it means we try to start a new game
        elseif (isset($_GET["address"]) && isset($_GET["port"]))
            createNewGame($_GET["address"], $_GET["port"]);
        
        // If nothing is provided, we try to watch a game
        else
            showGameSelectionPage();
        
    }
    main();

/**********************************************************************************************************************************************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
?>