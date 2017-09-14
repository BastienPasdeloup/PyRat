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
    // Max allowed value for ports
    
    /** CODE **/
    define("MAX_PORT", 65535);
    
/**********************************************************************************************************************************************************************************************************************************/

    /** DOCUMENTATION **/
    // Char used to indicate the end of a message
    
    /** CODE **/
    define("MESSAGE_DELIMITER", "\n");
    
/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Min allowed value for ports
    
    /** CODE **/
    define("MIN_PORT", 1024);

/**********************************************************************************************************************************************************************************************************************************/

    /** DOCUMENTATION **/
    // Size of the buffer when reading from the socket
    
    /** CODE **/
    define("READ_MAX_SIZE", 2048);

/**********************************************************************************************************************************************************************************************************************************/
    
    /** DOCUMENTATION **/
    // Timeout for the connection in seconds
    
    /** CODE **/
    define("TIMEOUT", 10.0);

/**********************************************************************************************************************************************************************************************************************************/
/************************************************************************************************************ FUNCTIONS ***********************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/

    /** DOCUMENTATION **/
    // Start a TCP socket server
    
    /** CODE **/
    function startServer ($addressArgument, $portArgument)
    {
        
        // We check the port value
        $port = intval($portArgument);
        if ($port < MIN_PORT || $port > MAX_PORT)
            showErrorPage("Invalid port value: ".$portArgument);

        // Socket creation
        $tmpSocket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
        if (!$tmpSocket)
            return "Error creating socket";

        // Bind in a loop until any previous timeout is finally reached
        if (!socket_set_option($tmpSocket, SOL_SOCKET, SO_REUSEADDR, 1))
            return "Could not make socket reusable";
        do
            $error = socket_bind($tmpSocket, $addressArgument, $port);
        while ($error);

        // We wait for one connection
        if (!socket_listen($tmpSocket, 1))
            return "Error listening on socket";

        // we accept a connection in a certain time
        if (!socket_set_option($tmpSocket, SOL_SOCKET, SO_RCVTIMEO, array("sec"=>intval(TIMEOUT), "usec"=>(TIMEOUT-intval(TIMEOUT))*100000)))
            return "Error setting socket timeout";
        $socket = socket_accept($tmpSocket);
        if (!$socket)
            return "No connection received before timeout";

        // Everything was ok
        return $socket;
        
    }

/**********************************************************************************************************************************************************************************************************************************/

    /** DOCUMENTATION **/
    // Transforms a JSON string to a structure
    
    /** CODE **/
    function fieldToStruct ($messageField)
    {
        
        // We transform the field into a structure
        $messageField = str_replace("(", "\"(", $messageField);
        $messageField = str_replace(")", ")\"", $messageField);
        return json_decode($messageField, true);
        
    }
    
/**********************************************************************************************************************************************************************************************************************************/

    /** DOCUMENTATION **/
    // Reads a message from the socket
    
    /** CODE **/
    function readMessage ($socket)
    {

        // We read until we find a delimiter or the client has disconnected
        $message = "";
        while (strlen($message) == 0 || substr($message, -1) != MESSAGE_DELIMITER)
        {
            $result = socket_read($socket, READ_MAX_SIZE, PHP_NORMAL_READ);
            if (!$result)
                return "Client has disconnected";
            $message .= $result;
        }

        // Conversion into a structure
        $message = preg_replace("/[^[:print:]]/", "", $message);
        $decodedMessage = json_decode($message, true);
        if ($decodedMessage == NULL)
            return "Invalid message received";
        return $decodedMessage;
        
    }

/**********************************************************************************************************************************************************************************************************************************/

    /** DOCUMENTATION **/
    // Stops the server
    
    /** CODE **/
    function stopServer ($socket)
    {
        
        // We close the socket
        socket_close($socket);
        
    }

/**********************************************************************************************************************************************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
?>