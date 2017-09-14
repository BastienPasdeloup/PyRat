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
    #include <arpa/inet.h>
    #include <regex>
    #include <sstream>
    #include <string>
    #include <sys/stat.h>
    
    /** INTERNAL **/
    #include <Shell.cpp>
    #include <ToString.cpp>
    
    /** NAMESPACES **/
    using namespace std;

/**********************************************************************************************************************************************************************************************************************************/
/************************************************************************************************************** CLASS *************************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
    
    #ifndef _TYPE_CONVERTER_
    #define _TYPE_CONVERTER_
        
        class TypeConverter
        {
            
            /**********************************************************************************************************************************************************************************************************/
            /************************************************************************************************ CONSTANTS ***********************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Max value allowed for ports
                
                /** CODE **/
                private : const int MAX_PORT = 65535;

            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Min value allowed for ports
                
                /** CODE **/
                private : const int MIN_PORT = 1024;

            /**********************************************************************************************************************************************************************************************************/
            /********************************************************************************************** CONSTRUCTORS **********************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Default constructor
                
                /** CODE **/
                public : TypeConverter ()
                {}
            
            /**********************************************************************************************************************************************************************************************************/
            /*********************************************************************************************** DESTRUCTOR ***********************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Empty destructor
                
                /** CODE **/
                public : virtual ~TypeConverter ()
                {}
                
            /**********************************************************************************************************************************************************************************************************/
            /************************************************************************************************* METHODS ************************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Getter for the min port value
                // Useful for setting default value in case of optional arguments
                
                /** CODE **/
                public : int getMinPort ()
                {
                    
                    // Getter for the MIN_PORT constant
                    return MIN_PORT;
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/

                /** DOCUMENTATION **/
                // Checks if the string is a double
                
                /** CODE **/
                public : bool isDouble (string stringToCheck)
                {
                    
                    // We check if the string is a valid double
                    istringstream iss(stringToCheck);
                    double result;
                    return !!(iss >> result);
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/

                /** DOCUMENTATION **/
                // Transforms "true" or "false" (any case) into the corresponding boolean
                
                /** CODE **/
                public : double toBool (string stringToConvert)
                {
                    
                    // Must be "true" or "false" in any case
                    transform(stringToConvert.begin(), stringToConvert.end(), stringToConvert.begin(), ::tolower);
                    bool result = false;
                    if (stringToConvert == "true")
                        result = true;
                    else if (stringToConvert != "false")
                        Shell::getInstance().error(stringToConvert + " is not a valid boolean");
                    
                    // Done
                    return result;
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/

                /** DOCUMENTATION **/
                // Transforms the string into a double
                
                /** CODE **/
                public : double toDouble (string stringToConvert)
                {
                    
                    // We check if the string is a valid double
                    istringstream iss(stringToConvert);
                    double result;
                    if (!(iss >> result))
                        Shell::getInstance().error(stringToConvert + " is not a valid double");
                    
                    // Done
                    return result;
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/

                /** DOCUMENTATION **/
                // Transforms the string into a double with min bound check
                
                /** CODE **/
                public : double toDoubleGreaterThan (string stringToConvert, double minBound)
                {
                    
                    // Must be a double greater than a bound
                    double value = toDouble(stringToConvert);
                    if (value < minBound)
                        Shell::getInstance().error(stringToConvert + " is not a valid double greater than " + double_to_string(minBound));
                    
                    // Done
                    return value;
                    
                }

            /**********************************************************************************************************************************************************************************************************/

                /** DOCUMENTATION **/
                // Transforms the string into a double with bounds check
                
                /** CODE **/
                public : double toDoubleInBounds (string stringToConvert, double minBound, double maxBound)
                {
                    
                    // Must be a double within some bounds
                    double value = toDouble(stringToConvert);
                    if (value < minBound || value > maxBound)
                        Shell::getInstance().error(stringToConvert + " is not a valid double in [" + double_to_string(minBound) + ", " + double_to_string(maxBound) + "]");
                    
                    // Done
                    return value;
                    
                }

            /**********************************************************************************************************************************************************************************************************/

                /** DOCUMENTATION **/
                // Transforms the string into an int
                
                /** CODE **/
                public : int toInt (string stringToConvert)
                {
                    
                    // We check if the string is a valid integer
                    istringstream iss(stringToConvert);
                    int result;
                    if (!(iss >> result))
                        Shell::getInstance().error(stringToConvert + " is not a valid integer");
                    
                    // Done
                    return result;
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/

                /** DOCUMENTATION **/
                // Transforms the string into an int with min bound check
                
                /** CODE **/
                public : int toIntGreaterThan (string stringToConvert, int minBound)
                {
                    
                    // Must be an integer greater than a bound
                    int value = toInt(stringToConvert);
                    if (value < minBound)
                        Shell::getInstance().error(stringToConvert + " is not a valid integer greater than " + to_string(minBound));
                    
                    // Done
                    return value;
                    
                }

            /**********************************************************************************************************************************************************************************************************/

                /** DOCUMENTATION **/
                // Transforms the string into an int with bounds check
                
                /** CODE **/
                public : int toIntInBounds (string stringToConvert, int minBound, int maxBound)
                {
                    
                    // Must be an integer within some bounds
                    int value = toInt(stringToConvert);
                    if (value < minBound || value > maxBound)
                        Shell::getInstance().error(stringToConvert + " is not a valid integer in [" + to_string(minBound) + ", " + to_string(maxBound) + "]");
                    
                    // Done
                    return value;
                    
                }

            /**********************************************************************************************************************************************************************************************************/

                /** DOCUMENTATION **/
                // Checks that the string corresponds to a valid IP address
                
                /** CODE **/
                public : string toIP (string stringToConvert)
                {
                    
                    // We check if the string is a valid IP address
                    struct sockaddr_in socketDescription;
                    int result = inet_pton(AF_INET, stringToConvert.c_str(), &(socketDescription.sin_addr));
                    if (result != 1)
                        Shell::getInstance().error("Invalid IP " + stringToConvert);
                    
                    // Done
                    return stringToConvert;
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/

                /** DOCUMENTATION **/
                // Sanitizes the given string to make it JSON compatible
                
                /** CODE **/
                public : string toJSON (string stringToConvert)
                {
                    
                    // We add backslashes to the backslashes and the double quotes
                    stringToConvert = regex_replace(stringToConvert, regex("\\\\"), "\\\\");
                    stringToConvert = regex_replace(stringToConvert, regex("\""), "\\\"");
                    
                    // Done
                    return stringToConvert;
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/

                /** DOCUMENTATION **/
                // Checks that the string corresponds to an existing path
                
                /** CODE **/
                public : string toPath (string stringToConvert)
                {
                    
                    // We check if the string corresponds to an existing directory
                    struct stat buffer;
                    if (stat(stringToConvert.c_str(), &buffer) != 0)
                        Shell::getInstance().error("Invalid path " + stringToConvert);
                    
                    // Done
                    return stringToConvert;
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/

                /** DOCUMENTATION **/
                // Checks that the string corresponds to a valid port value
                
                /** CODE **/
                public : int toPort (string stringToConvert)
                {
                    
                    // Integer in correct bounds
                    return toIntInBounds(stringToConvert, MIN_PORT, MAX_PORT);
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
            
        };
        
    #endif

/**********************************************************************************************************************************************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
