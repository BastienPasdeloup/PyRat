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
    #include <arpa/inet.h>
    #include <fcntl.h>
    #include <ifaddrs.h>
    #include <string>
    
    /** INTERNAL **/
    #include <NetworkObject.cpp>
    #include <Shell.cpp>
    
    /** NAMESPACES **/
    using namespace std;

/**********************************************************************************************************************************************************************************************************************************/
/************************************************************************************************************** CLASS *************************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
    
    #ifndef _NETWORK_SERVER_
    #define _NETWORK_SERVER_
        
        class NetworkServer : public NetworkObject
        {
            
            /********************************************************************************************** CONSTRUCTORS **********************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Constructor with the IP address and port
                
                /** CODE **/
                protected : NetworkServer (string address, int port) : NetworkObject(address, port)
                {}
                
            /**********************************************************************************************************************************************************************************************************/
            /*********************************************************************************************** DESTRUCTOR ***********************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Empty destructor
                
                /** CODE **/
                protected : virtual ~NetworkServer ()
                {}
                
            /**********************************************************************************************************************************************************************************************************/
            /************************************************************************************************* METHODS ************************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Creates a TCP socket server at the given address and port
                
                /** CODE **/
                public : void establishConnection ()
                {
                    
                    // We create a socket in non-blocking mode
                    int tmpSocket = socket(AF_INET, SOCK_STREAM, 0);
                    if (tmpSocket < 0) 
                        Shell::getInstance().error("Could not open socket");
                    
                    // We configure the socket to the given address/port
                    struct sockaddr_in tmpSocketDescription;
                    tmpSocketDescription.sin_family = AF_INET;
                    tmpSocketDescription.sin_addr.s_addr = inet_addr(NetworkObject::_address.c_str());
                    tmpSocketDescription.sin_port = htons(NetworkObject::_port);
                    
                    // Bind in a loop until any previous timeout is finally reached
                    int enable = 1;
                    int error = 0;
                    if (setsockopt(tmpSocket, SOL_SOCKET, SO_REUSEADDR, &enable, sizeof(int)) < 0)
                        Shell::getInstance().error("Could not make socket reusable");
                    do
                        error = bind(tmpSocket, (struct sockaddr*)(&tmpSocketDescription), sizeof(tmpSocketDescription));
                    while (error < 0);
                    
                    // We accept one connection in some period
                    listen(tmpSocket, 1);
                    struct sockaddr_in socketDescription;
                    socklen_t socketDescriptionSize = sizeof(socketDescription);
                    fd_set set;
                    struct timeval timeout;
                    FD_ZERO(&set);
                    FD_SET(tmpSocket, &set);
                    timeout.tv_sec = NetworkObject::START_CONNECTION_TIMEOUT;
                    timeout.tv_usec = 0;
                    int result = select(tmpSocket + 1, &set, NULL, NULL, &timeout);
                    if (result == -1)
                        Shell::getInstance().error("Error in socket select");
                    
                    // Everything went ok
                    else if (result > 0)
                    {
                        NetworkObject::_socket = accept(tmpSocket, (struct sockaddr*)(&socketDescription), &socketDescriptionSize);
                        NetworkObject::_connected = true;
                        close(tmpSocket);
                    }
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
            
        };
        
    #endif

/**********************************************************************************************************************************************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
