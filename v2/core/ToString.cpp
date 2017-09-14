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
    #include <map>
    #include <regex>
    #include <set>
    #include <string>
    #include <unordered_map>
    #include <unordered_set>
    #include <vector>
    
    /** NAMESPACES **/
    using namespace std;

/**********************************************************************************************************************************************************************************************************************************/
/************************************************************************************************************** CODES *************************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
    
    #ifndef _TO_STRING_
    #define _TO_STRING_

        /******************************************************************************************************************************************************************************************************************/
        /***************************************************************************************************** METHODS ****************************************************************************************************/
        /******************************************************************************************************************************************************************************************************************/

            /** DOCUMENTATION **/
            // Returns the string representing the given double
            // Minimzes the representation of the string
            // Not called "to_string" because it uses the classical "to_string"
            
            /** CODE **/
            string double_to_string (double value)
            {
                
                // Nicer to_string for doubles
                if (value == (int)(value))
                    return to_string((int)(value));
                else
                {
                    string croppedDouble = to_string(value).substr(0, to_string(value).find_last_not_of("0") + 1);
                    croppedDouble = regex_replace(croppedDouble, regex(","), ".");
                    return croppedDouble;
                }
                
            }
            
        /******************************************************************************************************************************************************************************************************************/

            /** DOCUMENTATION **/
            // To be able to use to_string for strings
            // Useful for recursive calls
            
            /** CODE **/
            string to_string (string value)
            {
                
                // We return the string
                return value;
                
            }
    
        /******************************************************************************************************************************************************************************************************************/

            /** DOCUMENTATION **/
            // Returns the string representing the given vector
            
            /** CODE **/
            template <typename T> string to_string (vector<T> elements)
            {
                
                // To be able to use to_string for vectors
                string result = "[";
                bool firstElementDone = false;
                for (auto& element : elements)
                {
                    if (firstElementDone)
                        result += "; ";
                    firstElementDone = true;
                    result += to_string(element);
                }
                result += "]";
                return result;
                
            }

        /******************************************************************************************************************************************************************************************************************/

            /** DOCUMENTATION **/
            // Returns the string representing the given unordered set
            
            /** CODE **/
            template <typename T> string to_string (unordered_set<T> elements)
            {
                
                // To be able to use to_string for unordered sets
                string result = "{";
                bool firstElementDone = false;
                for (auto& element : elements)
                {
                    if (firstElementDone)
                        result += "; ";
                    firstElementDone = true;
                    result += to_string(element);
                }
                result += "}";
                return result;
        
            }

        /******************************************************************************************************************************************************************************************************************/

            /** DOCUMENTATION **/
            // Returns the string representing the given set
            
            /** CODE **/
            template <typename T> string to_string (set<T> elements)
            {
                
                // To be able to use to_string for sets
                string result = "{";
                bool firstElementDone = false;
                for (auto& element : elements)
                {
                    if (firstElementDone)
                        result += "; ";
                    firstElementDone = true;
                    result += to_string(element);
                }
                result += "}";
                return result;
        
            }

        /******************************************************************************************************************************************************************************************************************/

            /** DOCUMENTATION **/
            // Returns the string representing the given tuple
            
            /** CODE **/
            template <typename T> string to_string (tuple<T> elements)
            {
                
                // To be able to use to_string for tuples
                string result = "(";
                bool firstElementDone = false;
                for (auto& element : elements)
                {
                    if (firstElementDone)
                        result += "; ";
                    firstElementDone = true;
                    result += to_string(element);
                }
                result += ")";
                return result;
        
            }

        /******************************************************************************************************************************************************************************************************************/

            /** DOCUMENTATION **/
            // Returns the string representing the given unordered map
            
            /** CODE **/
            template <typename T1, typename T2> string to_string (unordered_map<T1, T2> elements)
            {
                
                // To be able to use to_string for unordered maps
                string result = "{";
                bool firstElementDone = false;
                for (auto element : elements)
                {
                    if (firstElementDone)
                        result += "; ";
                    firstElementDone = true;
                    result += to_string(element.first) + ":" + to_string(element.second);
                }
                result += "}";
                return result;
        
            }

        /******************************************************************************************************************************************************************************************************************/

            /** DOCUMENTATION **/
            // Returns the string representing the given map
            
            /** CODE **/
            template <typename T1, typename T2> string to_string (map<T1, T2> elements)
            {
                
                // To be able to use to_string for maps
                string result = "{";
                bool firstElementDone = false;
                for (auto element : elements)
                {
                    if (firstElementDone)
                        result += "; ";
                    firstElementDone = true;
                    result += to_string(element.first) + ":" + to_string(element.second);
                }
                result += "}";
                return result;
        
            }

        /******************************************************************************************************************************************************************************************************************/

            /** DOCUMENTATION **/
            // Returns the string representing the given pair
            
            /** CODE **/
            template <typename T1, typename T2> string to_string (pair<T1, T2> elements)
            {
                
                // To be able to use to_string for pairs
                return "(" + to_string(elements.first) + ", " + to_string(elements.second) + ")";
        
            }

        /******************************************************************************************************************************************************************************************************************/
        /******************************************************************************************************************************************************************************************************************/
        
    #endif

/**********************************************************************************************************************************************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
