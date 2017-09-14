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
/************************************************************************************************************ CONSTANTS ***********************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Address of the database
    
    /** CODE **/
    define("DB_ADDRESS", "localhost");
    
/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Name of the database
    
    /** CODE **/
    define("DB_NAME", "pyrat");
    
/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Password of the user for the database
    
    /** CODE **/
    define("DB_PASSWORD", "pyrat");
    
/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Name of the user for the database
    
    /** CODE **/
    define("DB_USER", "pyrat");
    
/**********************************************************************************************************************************************************************************************************************************/
/************************************************************************************************************ FUNCTIONS ***********************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/

    /** DOCUMENTATION **/
    // Connects to the database
    
    /** CODE **/
    function connectToDatabase ()
    {
        
        // We connect to the database and return the link to the database
        $dbLink = new mysqli(DB_ADDRESS, DB_USER, DB_PASSWORD, DB_NAME);
        if ($dbLink->connect_error)
            return "Connection failed: ".$dbLink->connect_error;
        return $dbLink;
        
    }
    
/**********************************************************************************************************************************************************************************************************************************/

    /** DOCUMENTATION **/
    // Gets the game description from the database
    
    /** CODE **/
    function getGameInfo ($gameID)
    {
        
        // Connection
        $dbLink = connectToDatabase();
        if (is_string($dbLink))
            return $dbLink;
        
        // We get the game description and the players, sorted by creation date
        $request = "SELECT *
                    FROM game, player
                    WHERE game.id = player.game_id
                    AND game.id = ".mysqli_real_escape_string($dbLink, $gameID)."
                    ORDER BY player.number ASC";
        
        // Request
        $result = $dbLink->query($request);
        
        // Disconnection
        $dbLink->close();
        
        // Verification
        if (!$result)
            return "Invalid request: ".$request;
        if (mysqli_num_rows($result) == 0)
            return "Required game does not exist";
        return $result;
        
    }

/**********************************************************************************************************************************************************************************************************************************/

    /** DOCUMENTATION **/
    // Gets a move per player from the database
    
    /** CODE **/
    function getMove ($gameID, $moveID)
    {
        
        // Connection
        $dbLink = connectToDatabase();
        if (is_string($dbLink))
            return $dbLink;
        
        // We get the moves, sorted by player
        $request = "SELECT *
                    FROM move
                    WHERE move.game_id = ".mysqli_real_escape_string($dbLink, $gameID)."
                    AND move.time = ".mysqli_real_escape_string($dbLink, $moveID)."
                    ORDER BY player_number ASC";
        
        // Request
        $result = $dbLink->query($request);
        
        // Disconnection
        $dbLink->close();
        
        // Verification
        if (!$result)
            return "Invalid request: ".$request;
        return $result;
        
    }

/**********************************************************************************************************************************************************************************************************************************/

    /** DOCUMENTATION **/
    // Gets the list of games from the database
    
    /** CODE **/
    function getGamesList ()
    {
        
        // Connection
        $dbLink = connectToDatabase();
        if (is_string($dbLink))
            return $dbLink;
        
        // We get the list of games, sorted by date
        $request = "SELECT t1.id, t1.start, t1.name, t1.number, t2.nbPlayers
                    FROM
                    (
                        SELECT game.id, game.start, player.name, player.number
                        FROM game, player
                        WHERE game.id = player.game_id
                        ORDER BY game.start, player.number ASC
                    ) t1
                    INNER JOIN
                    (
                        SELECT player.game_id, COUNT(*) AS 'nbPlayers'
                        FROM player
                        GROUP BY player.game_id
                    ) t2
                    ON t1.id = t2.game_id";
        
        // Request
        $result = $dbLink->query($request);
        
        // Disconnection
        $dbLink->close();
        
        // Verification
        if (!$result)
            return "Invalid request: ".$request;
        return $result;
        
    }

/**********************************************************************************************************************************************************************************************************************************/

    /** DOCUMENTATION **/
    // Iterates over the result of a query
    
    /** CODE **/
    function nextEntry ($result)
    {
        
        // Encapsulation of the MySQLi function
        return mysqli_fetch_array($result, MYSQLI_ASSOC);
        
    }

/**********************************************************************************************************************************************************************************************************************************/

    /** DOCUMENTATION **/
    // Checks if the information for a game are available or if it has crashed
    
    /** CODE **/
    function getNewGameStatus ($gameID)
    {
        
        // Connection
        $dbLink = connectToDatabase();
        if (is_string($dbLink))
            return $dbLink;
        
        // We get the game description and use the width as status indicator
        $request = "SELECT map AS message, width AS status
                    FROM game
                    WHERE game.id = ".mysqli_real_escape_string($dbLink, $gameID);
        
        // Request
        $result = $dbLink->query($request);
        
        // Disconnection
        $dbLink->close();
        
        // Verification
        if (!$result)
            return "Invalid request: ".$request;
        if (mysqli_num_rows($result) == 0)
            return "Required game does not exist";
        return $result;
        
    }

/**********************************************************************************************************************************************************************************************************************************/

    /** DOCUMENTATION **/
    // Inserts a placeholder in the database to reserve a game
    // Useful for synchronization with the socket thread
    
    /** CODE **/
    function reserveNewGame ()
    {
        
        // Connection
        $dbLink = connectToDatabase();
        if (is_string($dbLink))
            return $dbLink;
        
        // We create a new game with the minimum information
        $request = "INSERT INTO game
                    VALUES
                    (
                        NULL,
                        CURRENT_TIMESTAMP,
                        \"\",
                        \"\",
                        0,
                        0
                    )";
        
        // Request
        $result = $dbLink->query($request);
        
        // Verification
        if (!$result)
            return "Invalid request: ".$request;
        $gameID = $dbLink->insert_id;
        
        // Disconnection
        $dbLink->close();
        
        // We return the newly created game ID
        return $gameID;
        
    }

/**********************************************************************************************************************************************************************************************************************************/

    /** DOCUMENTATION **/
    // Saves the game description and players to the database
    
    /** CODE **/
    function saveNewGame ($gameID, $mazeMap, $piecesOfCheese, $mazeWidth, $mazeHeight, $player1Name, $player2Name, $player1StartingLocation, $player2StartingLocation)
    {
        
        // Connection
        $dbLink = connectToDatabase();
        if (is_string($dbLink))
            return $dbLink;
        
        // We insert the players
        $request = "INSERT INTO player
                    VALUES
                    (
                        ".mysqli_real_escape_string($dbLink, $gameID).",
                        1,
                        \"".mysqli_real_escape_string($dbLink, $player1Name)."\",
                        \"".mysqli_real_escape_string($dbLink, $player1StartingLocation)."\"
                    )";
        if ($player2Name != "")
            $request .= ", (
                                ".mysqli_real_escape_string($dbLink, $gameID).",
                                2,
                                \"".mysqli_real_escape_string($dbLink, $player2Name)."\",
                                \"".mysqli_real_escape_string($dbLink, $player2StartingLocation)."\"
                            )";
        
        // Request
        $result = $dbLink->query($request);
        
        // Verification
        if (!$result)
            return "Invalid request: ".$request;
        
        // We save the game description where the ID was reserved
        $request = "UPDATE game
                    SET map = \"".mysqli_real_escape_string($dbLink, $mazeMap)."\",
                        piecesOfCheese = \"".mysqli_real_escape_string($dbLink, $piecesOfCheese)."\",
                        width = ".mysqli_real_escape_string($dbLink, $mazeWidth).",
                        height = ".mysqli_real_escape_string($dbLink, $mazeHeight)."
                    WHERE id = ".mysqli_real_escape_string($dbLink, $gameID);
        
        // Request
        $result = $dbLink->query($request);
        
        // Verification
        if (!$result)
            return "Invalid request: ".$request;
        
        // Disconnection
        $dbLink->close();
        
    }

/**********************************************************************************************************************************************************************************************************************************/

    /** DOCUMENTATION **/
    // Saves the turn information to the database
    
    /** CODE **/
    function saveTurn ($gameID, $turnID, $player1Move, $player2Move, $player1MoveDuration, $player2MoveDuration, $player1Score, $player2Score, $player1CheeseEaten, $player2CheeseEaten)
    {
        
        // Connection
        $dbLink = connectToDatabase();
        if (is_string($dbLink))
            return $dbLink;
        
        // We insert the moves
        $request = "INSERT INTO move
                    VALUES
                    (
                        ".mysqli_real_escape_string($dbLink, $gameID).",
                        1,
                        ".mysqli_real_escape_string($dbLink, $turnID).",
                        ".mysqli_real_escape_string($dbLink, $player1MoveDuration).",
                        '".mysqli_real_escape_string($dbLink, $player1Move)."',
                        ".mysqli_real_escape_string($dbLink, $player1Score).",
                        \"".mysqli_real_escape_string($dbLink, $player1CheeseEaten)."\"
                    )";
        if ($player2Move != "")
            $request .= ", (
                                ".mysqli_real_escape_string($dbLink, $gameID).",
                                2,
                                ".mysqli_real_escape_string($dbLink, $turnID).",
                                ".mysqli_real_escape_string($dbLink, $player2MoveDuration).",
                                '".mysqli_real_escape_string($dbLink, $player2Move)."',
                                ".mysqli_real_escape_string($dbLink, $player2Score).",
                                \"".mysqli_real_escape_string($dbLink, $player2CheeseEaten)."\"
                            )";
        
        // Request
        $result = $dbLink->query($request);
        
        // Disconnection
        $dbLink->close();
        
        // Verification
        if (!$result)
            return "Invalid request: ".$request;
        
    }

/**********************************************************************************************************************************************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
?>