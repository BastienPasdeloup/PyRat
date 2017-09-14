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
    // Name of the webpage
    
    /** CODE **/
    define("PAGE_TITLE", "PyRat");

/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Path to the image for the first player
    
    /** CODE **/
    define("PLAYER_1_IMAGE", "./resources/illustrations/rat.png");

/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Path to the image for the second player
    
    /** CODE **/
    define("PLAYER_2_IMAGE", "./resources/illustrations/python_left.png");

/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Path to the token for the first player
    
    /** CODE **/
    define("PLAYER_1_TOKEN", "./resources/gameElements/rat.png");

/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Path to the token for the second player
    
    /** CODE **/
    define("PLAYER_2_TOKEN", "./resources/gameElements/python.png");

/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Path to the game logo image
    
    /** CODE **/
    define("PYRAT_IMAGE", "./resources/illustrations/rat_python.png");

/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Path to the images of walls
    
    /** CODE **/
    define("WALL_IMAGE", "./resources/gameElements/wall.png");

/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Path to the images of mud
    
    /** CODE **/
    define("MUD_IMAGE", "./resources/gameElements/mud.png");

/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Path to the images of tiles
    // This is only the beginning of the path to allow multiple images of tiles
    
    /** CODE **/
    define("TILE_IMAGES", "./resources/gameElements/tile");

/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Path to the images of pieces of cheese
    
    /** CODE **/
    define("CHEESE_IMAGE", "./resources/gameElements/cheese.png");

/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Path to the images of corners
    
    /** CODE **/
    define("CORNER_IMAGE", "./resources/gameElements/corner.png");

/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Path to the icon of the page
    
    /** CODE **/
    define("ICON_FILE_NAME", "./resources/various/pyrat.ico");

/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Max number of characters displayed for the players' names
    
    /** CODE **/
    define("MAX_NAME_SIZE", 50);

/**********************************************************************************************************************************************************************************************************************************/
/************************************************************************************************************ FUNCTIONS ***********************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/

    /** DOCUMENTATION **/
    // Returns the HTML img tag with the logo
    
    /** CODE **/
    function logoToHTML ()
    {
        
        // Logo in an img tag
        return "<img class=\"defaultImage\" src=\"".PYRAT_IMAGE."\" />";
        
    }
    
/**********************************************************************************************************************************************************************************************************************************/

    /** DOCUMENTATION **/
    // Crops a name that is too long
    
    /** CODE **/
    function cropName ($name)
    {
        
        // We crop the name if needed
        if (strlen($name) > MAX_NAME_SIZE)
            $name = substr($name, 0, MAX_NAME_SIZE)."...";
        return $name;
        
    }

/**********************************************************************************************************************************************************************************************************************************/

    /** DOCUMENTATION **/
    // Returns the string representing the HTML tags of the maze, cheese, walls...
    
    /** CODE **/
    function mazeToHTML ($game, $mazeMap, $piecesOfCheese, $mazeWidth, $mazeHeight, $player1StartingLocation, $player2StartingLocation)
    {
        
        // We generate the tiles, cheese, mud and walls
        $mazeHTML = "";
        for ($line = 0 ; $line < $mazeHeight ; $line++)
        {
            $mazeHTML .= "<div class=\"tilesLine\">\n";
            $mazeHTML .= "    <div class=\"tilesLineWrapper\">\n";
            for ($column = 0 ; $column < $mazeWidth ; $column++)
            {
                
                // Some useful information
                $key = "(".$line.", ".$column.")";
                $topKey = "(".($line - 1).", ".$column.")";
                $bottomKey = "(".($line + 1).", ".$column.")";
                $leftKey = "(".$line.", ".($column - 1).")";
                $rightKey = "(".$line.", ".($column + 1).")";
                $topLeftKey = "(".($line - 1).", ".($column - 1).")";
                $topRightKey = "(".($line - 1).", ".($column + 1).")";
                $bottomLeftKey = "(".($line + 1).", ".($column - 1).")";
                $bottomRightKey = "(".($line + 1).", ".($column + 1).")";
                $isLeftMostKey = !array_key_exists($leftKey, $mazeMap);
                $isRightMostKey = !array_key_exists($rightKey, $mazeMap);
                $isTopMostKey = !array_key_exists($topKey, $mazeMap);
                $isBottomMostKey = !array_key_exists($bottomKey, $mazeMap);
                $isCheeseLocation = in_array($key, $piecesOfCheese);
                $canGoLeft = !$isLeftMostKey && array_key_exists($leftKey, $mazeMap[$key]);
                $canGoRight = !$isRightMostKey && array_key_exists($rightKey, $mazeMap[$key]);
                $canGoTop = !$isTopMostKey && array_key_exists($topKey, $mazeMap[$key]);
                $canGoDown = !$isBottomMostKey && array_key_exists($bottomKey, $mazeMap[$key]);
                $topKeyCanGoLeft = $isTopMostKey || array_key_exists($topLeftKey, $mazeMap[$topKey]);
                $topKeyCanGoRight = $isTopMostKey || array_key_exists($topRightKey, $mazeMap[$topKey]);
                $bottomKeyCanGoLeft = $isBottomMostKey || array_key_exists($bottomLeftKey, $mazeMap[$bottomKey]);
                $bottomKeyCanGoRight = $isBottomMostKey || array_key_exists($bottomRightKey, $mazeMap[$bottomKey]);
                $leftKeyCanGoTop = $isLeftMostKey || array_key_exists($topLeftKey, $mazeMap[$leftKey]);
                $leftKeyCanGoDown = $isLeftMostKey || array_key_exists($bottomLeftKey, $mazeMap[$leftKey]);
                $rightKeyCanGoTop = $isRightMostKey || array_key_exists($topRightKey, $mazeMap[$rightKey]);
                $rightKeyCanGoDown = $isRightMostKey || array_key_exists($bottomRightKey, $mazeMap[$rightKey]);
                
                // Tile
                $allTiles = glob(TILE_IMAGES."*.png");
                switch (rand(0, 3))
                {
                    case 0 : $rotation = " rotate90"; break;
                    case 1 : $rotation = " rotate180"; break;
                    case 2 : $rotation = " rotate270"; break;
                    default : $rotation = "";
                }
                $mazeHTML .= "        <div class=\"tile\">\n";
                $mazeHTML .= "            <img class=\"gameElement tileImage".$rotation."\" src=\"".$allTiles[rand(0, count($allTiles) - 1)]."\" />\n";
                
                // Side element (wall or mud)
                $keys = array($topKey, $bottomKey, $leftKey, $rightKey);
                $locations = array("top", "bottom", "left", "right");
                for ($i = 0 ; $i < 4 ; $i++)
                    if (!array_key_exists($keys[$i], $mazeMap[$key]))
                        $mazeHTML .= "            <img class=\"gameElement ".$locations[$i]."Separation wall\" src=\"".WALL_IMAGE."\" />\n";
                    elseif ($mazeMap[$key][$keys[$i]] > 1)
                    {
                        $mazeHTML .= "            <img class=\"gameElement ".$locations[$i]."Separation mud\" src=\"".MUD_IMAGE."\" />\n";
                        if ($locations[$i] == "right" || $locations[$i] == "bottom")
                            $mazeHTML .= "            <p class=\"mudLabel ".$locations[$i]."MudLabel\">".$mazeMap[$key][$keys[$i]]."</p>\n";
                    }

                // Corners
                $cornerNotNecessary = [($canGoTop && $rightKeyCanGoTop && !$canGoRight && !$topKeyCanGoRight) || ($canGoRight && $topKeyCanGoRight && !$canGoTop && !$rightKeyCanGoTop),
                                       ($canGoDown && $leftKeyCanGoDown && !$canGoLeft && !$bottomKeyCanGoLeft) || ($canGoLeft && $bottomKeyCanGoLeft && !$canGoDown && !$leftKeyCanGoDown),
                                       ($canGoTop && $leftKeyCanGoTop && !$canGoLeft && !$topKeyCanGoLeft) || ($canGoLeft && $topKeyCanGoLeft && !$canGoTop && !$leftKeyCanGoTop),
                                       ($canGoDown && $rightKeyCanGoDown && !$canGoRight && !$bottomKeyCanGoRight) || ($canGoRight && $bottomKeyCanGoRight && !$canGoDown && !$rightKeyCanGoDown)];
                $locations = array("topRight", "bottomLeft", "topLeft", "bottomRight");
                for ($i = 0 ; $i < 4 ; $i++)
                    if (!$cornerNotNecessary[$i])
                        $mazeHTML .= "            <img class=\"gameElement ".$locations[$i]."Corner corner\" src=\"".CORNER_IMAGE."\" />\n";
                
                // Cheese
                if ($isCheeseLocation)
                    $mazeHTML .= "            <img id=\"cheese_".$line."_".$column."\" class=\"gameElement cheese\" src=\"".CHEESE_IMAGE."\" />\n";
                
                // Player token
                if ($key == $player1StartingLocation)
                    $mazeHTML .= "            <img id=\"player1Token\" class=\"gameElement playerToken\" src=\"".PLAYER_1_TOKEN."\" />\n";
                if ($key == $player2StartingLocation)
                    $mazeHTML .= "            <img id=\"player2Token\" class=\"gameElement playerToken\" src=\"".PLAYER_2_TOKEN."\" />\n";
                
                // End of the tile
                $mazeHTML .= "        </div>\n";
                
            }
            $mazeHTML .= "    </div>\n";
            $mazeHTML .= "</div>\n";
            
            // We add hidden fields with the game ID and the cheese count
            $mazeHTML .= "<div id=\"gameID\" class=\"hidden\">".$game."</div>\n";
            $mazeHTML .= "<div id=\"cheeseCount\" class=\"hidden\">".count($piecesOfCheese)."</div>\n";
            
        }
        
        // Done
        return $mazeHTML;
        
    }

/**********************************************************************************************************************************************************************************************************************************/

    /** DOCUMENTATION **/
    // Returns the HTML tags for the players scores, images and names
    
    /** CODE **/
    function playerToHTML ($name, $number, $singlePlayer)
    {
        
        // Image
        $image = PLAYER_1_IMAGE;
        if ($number == 2)
            $image = PLAYER_2_IMAGE;
        
        // Player's description
        $description = "<p id=\"player".$number."Name\" class=\"playerName\">".cropName($name)."</p>\n";
        $description .= "<img class=\"playerImage\" src=\"".$image."\" />\n";
        $score = "<p id=\"player".$number."Score\" class=\"playerScore\">0</p>\n";
        
        // We return different things depending on the number of players
        if ($singlePlayer)
            return array("description"=>$description, "score"=>$score);
        else
            return $description.$score;
        
    }

/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Displays the error page
    
    /** CODE **/
    function showErrorPage ($message)
    {
        
        // Various areas
        $mazeArea = logoToHTML()."\n";
        $messagesArea = $message."\n";
        $player1Area = "";
        $player2Area = "";
        
        // We show the page and exit
        showPage($mazeArea, $player1Area, $player2Area, $messagesArea, false);
        die();
        
    }

/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Displays the game selection page
    
    /** CODE **/
    function showGameSelectionPage ()
    {
        
        // We get the list of games sorted by date
        $games = getGamesList();
        if (is_string($games))
            showErrorPage($games);
        
        // Maze area
        $mazeArea = logoToHTML()."\n";
        
        // Players areas
        $player1Area = "";
        $player2Area = "";
        
        // Messages area
        $messagesArea = "<form action=\"#\" method=\"get\">\n";
        $messagesArea .= "    <select name=\"game\">\n";
        $messagesArea .= "        <option disabled selected value>Select a game</option>\n";
        while ($row = nextEntry($games))
        {
            $messagesArea .= "        <option value=\"".$row["id"]."\">[".date("d/m/Y H:i:s", strtotime($row["start"]))."] ".cropName($row["name"]);
            if ($row["nbPlayers"] == 2)
            {
                $row = nextEntry($games);
                $messagesArea .= " Vs. ".cropName($row["name"]);
            }
            $messagesArea .= "</option>\n";
        }
        $messagesArea .= "    </select>\n";
        $messagesArea .= "    <input type=\"submit\" value=\"Go !\" />\n";
        $messagesArea .= "</form>\n";
        
        // We show the page
        showPage($mazeArea, $player1Area, $player2Area, $messagesArea, false);
        
    }

/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Displays a page with the given area contents
    
    /** CODE **/
    function showPage ($mazeArea, $player1Area, $player2Area, $messagesArea, $gameIsStarted)
    {
        
        // Page contents
        echo "<!DOCTYPE html>\n";
        echo "<html>\n";
        echo "    <head>\n";
        echo "        <meta charset=\"UTF-8\">\n";
        echo "        <link rel=\"stylesheet\" href=\"pyrat.css\" />\n";
        echo "        <link rel=\"icon\" href=\"".ICON_FILE_NAME."\" />\n";
        echo "        <script src=\"jquery.js\"></script>\n";
        if ($gameIsStarted)
        {
            echo "        <script src=\"mouseDrag.js\"></script>\n";
            echo "        <script src=\"animation.js\"></script>\n";
        }
        echo "        <title>".PAGE_TITLE."</title>\n";
        echo "    </head>\n";
        echo "    <body id=\"pyrat\">\n";
        echo "        <div class=\"gameArea\">\n";
        echo "            <div class=\"playerArea\">\n";
        foreach (preg_split("/((\r?\n)|(\r\n?))/", $player1Area) as $line)
            if ($line != "")
                echo "                ".$line."\n";
        echo "            </div>\n";
        echo "            <div id=\"mouseDraggable\" class=\"mazeArea\">\n";
        foreach (preg_split("/((\r?\n)|(\r\n?))/", $mazeArea) as $line)
            if ($line != "")
                echo "                ".$line."\n";
        echo "            </div>\n";
        echo "            <div class=\"playerArea\">\n";
        foreach (preg_split("/((\r?\n)|(\r\n?))/", $player2Area) as $line)
            if ($line != "")
                echo "                ".$line."\n";
        echo "            </div>\n";
        echo "        </div>\n";
        echo "        <div id=\"messagesArea\" class=\"messagesArea\">\n";
        foreach (preg_split("/((\r?\n)|(\r\n?))/", $messagesArea) as $line)
            if ($line != "")
                echo "            ".$line."\n";
        echo "        </div>\n";
        echo "    </body>\n";
        echo "</html>\n";
        
    }
    
/**********************************************************************************************************************************************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
?>