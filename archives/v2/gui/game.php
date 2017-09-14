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
    // Saves an error message to the database so that it can be displayed in the GUI
    
    /** CODE **/
    function saveError ($gameID, $server, $message)
    {
        
        // Since the errors here are not shown in the browser, we save them so that they can be shown anyway
        saveNewGame($gameID, $message, "", -1, -1, "", "", "", "");
        if (!is_string($server))
            stopServer($server);
        exit();
        
    }
    
/**********************************************************************************************************************************************************************************************************************************/
/*********************************************************************************************************** ENTRY POINT **********************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Entry point of this script
    // This script is executed in a different process to have asynchronous sockets
    // The communication is made through the database (this script fills it, the other reads it)
    
    /** CODE **/
    function main ()
    {
        
        // We get the arguments
        $addressArgument = $_SERVER["argv"][1];
        $portArgument = $_SERVER["argv"][2];
        $gameID = $_SERVER["argv"][3];
        
        // We start a server
        $server = startServer($addressArgument, $portArgument);
        if (is_string($server))
            saveError($gameID, $server, $server);
        
        // We read the initial message
        $message = readMessage($server);
        if (is_string($message))
            saveError($gameID, $server, $message);
        $mazeMapString = $message["mazeMap"];
        $mazeMap = fieldToStruct($mazeMapString);
        $piecesOfCheeseString = $message["piecesOfCheese"];
        $piecesOfCheese = fieldToStruct($piecesOfCheeseString);
        $width = $message["mazeWidth"];
        $height = $message["mazeHeight"];
        $player1Name = $message["player1Name"];
        $player1Location = $message["player1Location"];
        $player2Name = (array_key_exists("player2Name", $message) ? $message["player2Name"] : "");
        $player2Location = (array_key_exists("player2Location", $message) ? $message["player2Location"] : "");
        
        // We save the game to the database
        $result = saveNewGame($gameID, $mazeMapString, $piecesOfCheeseString, $width, $height, $player1Name, $player2Name, $player1Location, $player2Location);
        if (is_string($result))
            saveError($gameID, $server, $result);
        
        // We play turns until the game is over
        $turn = 1;
        $piecesOfCheeseBefore = $piecesOfCheese;
        do
        {
            
            // We read the turn message until nothing more is received
            $message = readMessage($server);
            if (is_string($message))
            {
                if ($message == "Client has disconnected")
                    break;
                else
                    saveError($gameID, $server, $message);
            }
            $piecesOfCheeseString = $message["piecesOfCheese"];
            $piecesOfCheese = fieldToStruct($piecesOfCheeseString);
            $player1Move = $message["player1Move"];
            $player1MoveDuration = $message["player1MoveDuration"];
            $player1Score = $message["player1Score"];
            $player2Move = (array_key_exists("player2Move", $message) ? $message["player2Move"] : "");
            $player2MoveDuration = (array_key_exists("player2MoveDuration", $message) ? $message["player2MoveDuration"] : "");
            $player2Score = (array_key_exists("player2Score", $message) ? $message["player2Score"] : "");
            
            // We determine the disappeared pieces of cheese
            $cheeseEaten = [];
            foreach ($piecesOfCheeseBefore as $cheese)
                if (!in_array($cheese, $piecesOfCheese))
                    array_push($cheeseEaten, $cheese);
            for ($i = count($cheeseEaten) ; $i < 2 ; $i++)
                array_push($cheeseEaten, "");
            $piecesOfCheeseBefore = $piecesOfCheese;
            
            // We save the turn to the database
            $result = saveTurn($gameID, $turn, $player1Move, $player2Move, $player1MoveDuration, $player2MoveDuration, $player1Score, $player2Score, $cheeseEaten[0], $cheeseEaten[1]);
            if (is_string($result))
                saveError($gameID, $server, $result);
            
            // If there are no pieces of cheese, we stop
            if (count($piecesOfCheese) == 0)
                break;
            $turn++;
            
        }
        while (true);

        // Once the game is over, we stop the server
        stopServer($server);
        
    }
    main();

/**********************************************************************************************************************************************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
?>