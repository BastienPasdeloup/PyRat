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
    // Regularity of the timer to check if a new move is appliable
    // A value of 0 means as fast as possible
    
    /** CODE **/
    const TIMER = 0;

/**********************************************************************************************************************************************************************************************************************************/

    /** DOCUMENTATION **/
    // Duration of the preprocessing phase animation
    
    /** CODE **/
    const PREPROCESSING_DURATION = 2000;

/**********************************************************************************************************************************************************************************************************************************/

    /** DOCUMENTATION **/
    // Duration of apparition of the go message
    
    /** CODE **/
    const GO_DURATION = 400;

/**********************************************************************************************************************************************************************************************************************************/

    /** DOCUMENTATION **/
    // Speed of the animation
    
    /** CODE **/
    const ANIMATION_DURATION = 200;

/**********************************************************************************************************************************************************************************************************************************/

    /** DOCUMENTATION **/
    // Speed of the disappearance of the cheese
    
    /** CODE **/
    const CHEESE_DISAPPEARANCE_DURATION = 200;

/**********************************************************************************************************************************************************************************************************************************/

    /** DOCUMENTATION **/
    // Character used to go up
    
    /** CODE **/
    const MOVE_UP = 'U';

/**********************************************************************************************************************************************************************************************************************************/

    /** DOCUMENTATION **/
    // Character used to go down
    
    /** CODE **/
    const MOVE_DOWN = 'D';

/**********************************************************************************************************************************************************************************************************************************/

    /** DOCUMENTATION **/
    // Character used to go left
    
    /** CODE **/
    const MOVE_LEFT = 'L';

/**********************************************************************************************************************************************************************************************************************************/

    /** DOCUMENTATION **/
    // Character used to go right
    
    /** CODE **/
    const MOVE_RIGHT = 'R';

/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Non-moving token for the first player
    
    /** CODE **/
    const PLAYER_1_TOKEN_IMAGE = "./resources/gameElements/rat.png";

/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Moving token for the first player
    
    /** CODE **/
    const PLAYER_1_MOVING_TOKEN_IMAGE = "./resources/gameElements/movingRat.png";

/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Non-moving token for the second player
    
    /** CODE **/
    const PLAYER_2_TOKEN_IMAGE = "./resources/gameElements/python.png";

/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Moving token for the second player
    
    /** CODE **/
    const PLAYER_2_MOVING_TOKEN_IMAGE = "./resources/gameElements/movingPython.png";

/**********************************************************************************************************************************************************************************************************************************/
/************************************************************************************************************ FUNCTIONS ***********************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Moves the chosen token in the chosen direction
    
    /** CODE **/
    function moveToken (tokenID, direction, duration, scoreID, scoreAfter, cheeseToRemoveAfter, lock, cheese, imageIfMoving, imageIfNotMoving)
    {
        
        // Tile size
        var height = $(".tile").height();
        var width = $(".tile").width();
        
        // Change of image
        if (direction != MOVE_UP && direction != MOVE_DOWN && direction != MOVE_LEFT && direction != MOVE_RIGHT)
        {
            $(tokenID).attr("src", imageIfNotMoving);
            $(tokenID).css({"transform" : "rotate(0deg)"});
        }
        else
        {
            $(tokenID).attr("src", imageIfMoving);
            if (direction == MOVE_UP)
                $(tokenID).css({"transform" : "rotate(0deg)"});
            else if (direction == MOVE_DOWN)
                $(tokenID).css({"transform" : "rotate(180deg)"});
            else if (direction == MOVE_LEFT)
                $(tokenID).css({"transform" : "rotate(270deg)"});
            else if (direction == MOVE_RIGHT)
                $(tokenID).css({"transform" : "rotate(90deg)"});
        }
        
        // Animation
        var animation = {top : "+=0"};
        if (direction == MOVE_UP)
            animation = {top : "-=" + (height / duration)};
        else if (direction == MOVE_DOWN)
            animation = {top : "+=" + (height / duration)};
        else if (direction == MOVE_LEFT)
            animation = {left : "-=" + (width / duration)};
        else if (direction == MOVE_RIGHT)
            animation = {left : "+=" + (width / duration)};
        
        // We update the score and the cheese after the animation
        $(tokenID).animate(animation, ANIMATION_DURATION, function ()
        {
            $(scoreID).html(scoreAfter);
            if (cheeseToRemoveAfter != "")
            {
                cheeseToRemoveAfter = cheeseToRemoveAfter.replace("(", "");
                cheeseToRemoveAfter = cheeseToRemoveAfter.replace(")", "");
                cheeseToRemoveAfter = cheeseToRemoveAfter.replace(", ", "_");
                $("#cheese_" + cheeseToRemoveAfter).fadeOut(CHEESE_DISAPPEARANCE_DURATION);
                cheese.count--;
            }
            lock.count--;
        });
        
    }
    
/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Changes the message in the message area
    
    /** CODE **/
    function showMessage (message)
    {
        
        // We show the message
        $("#messagesArea").html(message);
        
    }
    
/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Asks the PHP page for the moves to apply and animates the tokens
    
    /** CODE **/
    window.setTimeout(function ()
    {
        
        // Initialization
        var nextMove = 1;
        var gameID = $("#gameID").text();
        var lock = {count : 0};
        var gameIsOver = false;
        var cheese = {count: parseInt($("#cheeseCount").text())};
        
        // Starting message
        showMessage("Go!");
        
        // Function called regularly
        setTimeout(function ()
        {

            // We ask the server for the next move and do something if some data is available
            $.post("index.php", {game: gameID, move: nextMove}, function (result)
            {
                if (result != "{}" && lock.count == 0)
                {
                
                    // If we have an error, we replace the page contents
                    if (result[0] != '{')
                    {
                        document.write(result);
                        document.close();
                        gameIsOver = true;
                    }
                    
                    // If no error, we do something
                    else
                    {
                    
                        // We update the message
                        var objResult = jQuery.parseJSON(result);
                        var message = "[" + objResult.moves[0] + "]";
                        if (objResult.moves.length > 1)
                            message += "<div class=\"movesMessageSeparator\"></div>[" + objResult.moves[1] + "]";
                        showMessage(message);
                        
                        // We move the players accordingly
                        var playerTags = ["#player1Token", "#player2Token"];
                        var scoreTags = ["#player1Score", "#player2Score"];
                        var movingTokenImages = [PLAYER_1_MOVING_TOKEN_IMAGE, PLAYER_2_MOVING_TOKEN_IMAGE];
                        var notMovingTokenImages = [PLAYER_1_TOKEN_IMAGE, PLAYER_2_TOKEN_IMAGE];
                        for (var i = 0 ; i < objResult.moves.length ; i++)
                        {
                            lock.count++;
                            moveToken(playerTags[i], objResult.moves[i], objResult.durations[i], scoreTags[i], objResult.scoresAfter[i], objResult.cheeseToRemoveAfter[i], lock, cheese, movingTokenImages[i], notMovingTokenImages[i]);
                        }
                        
                        // Move is performed
                        nextMove++;
                        
                    }

                }
                else if (cheese.count == 0)
                {
                    
                    // If it is the end of the game, we update the message
                    if (!$("#player2Name").length)
                        showMessage("Congratulations! You got all the cheese!");
                    else if (parseInt($("#player1Score").text()) > parseInt($("#player2Score").text()))
                        showMessage($("#player1Name").text() + " wins!");
                    else if (parseInt($("#player1Score").text()) < parseInt($("#player2Score").text()))
                        showMessage($("#player2Name").text() + " wins!");
                    else
                        showMessage("The game is a tie!");
                    gameIsOver = true;
                    
                }
            });
            
            // Regular call
            if (!gameIsOver)
                setTimeout(arguments.callee, TIMER);
            
        }, GO_DURATION);
    }, PREPROCESSING_DURATION);
    
/**********************************************************************************************************************************************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/