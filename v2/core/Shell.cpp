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
    #include <iostream>
    #include <mutex>
    #include <QtCore/QObject>
    #include <QtGui/QApplication>
    #include <QtGui/QGridLayout>
    #include <QtGui/QIcon>
    #include <QtGui/QLabel>
    #include <QtGui/QPixmap>
    #include <QtGui/QTextEdit>
    #include <QtGui/QWidget>
    #include <string>
    #include <thread>
    #include <unistd.h>
    
    /** INTERNAL **/
    #include <ToString.cpp>
    
    /** NAMESPACES **/
    using namespace std;

/**********************************************************************************************************************************************************************************************************************************/
/************************************************************************************************************** CLASS *************************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
    
    #ifndef _SHELL_
    #define _SHELL_
        
        class Shell : public QObject
        {
            
            // Qt macro
            Q_OBJECT
            
            /**********************************************************************************************************************************************************************************************************/
            /************************************************************************************************* SIGNALS ************************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Signal emitted when some text is to be displayed
                
                /** CODE **/
                signals : void newText (QString message);
            
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Signal emitted when the program is over to close the shell
                
                /** CODE **/
                signals : void programStops ();
            
            /**********************************************************************************************************************************************************************************************************/
            /************************************************************************************************ CONSTANTS ***********************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Distance between elements in the shell
                
                /** CODE **/
                private : const int ELEMENTS_SPACING = 10;
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Path to the window icon
                
                /** CODE **/
                private : const string ICON_FILE_NAME = "/resources/various/pyrat.ico";
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Path to the image to show in the shell
                
                /** CODE **/
                private : const string IMAGE_FILE_NAME = "/resources/illustrations/rat_python.png";
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Max number of chars in the path directory
                
                /** CODE **/
                private : const int MAX_PATH = 4096;
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Color of the background of the message area
                
                /** CODE **/
                private : const string TEXT_EDIT_BACKGROUND_COLOR = "#AAAAAA";
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Color of the background of the window
                
                /** CODE **/
                private : const string WINDOW_BACKGROUND_COLOR = "#222222";
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Height of the window
                
                /** CODE **/
                private : const int WINDOW_HEIGHT = 350;
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Name of the window
                
                /** CODE **/
                private : const string WINDOW_TITLE = "PyRat - Core shell";
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Width of the window
                
                /** CODE **/
                private : const int WINDOW_WIDTH = 900;
                
            /**********************************************************************************************************************************************************************************************************/
            /*********************************************************************************************** ATTRIBUTES ***********************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Thread object to have the application run in a different thread
                
                /** CODE **/
                private : class thread* _applicationThread = nullptr;
            
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Boolean indicating if the shell should close when the program is over
                
                /** CODE **/
                private : bool _closeAtEnd = false;
            
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Mutex to synchronize the shell thread and the GUI
                
                /** CODE **/
                private : mutex _mutex;
            
            /**********************************************************************************************************************************************************************************************************/
            /********************************************************************************************** CONSTRUCTORS **********************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Default constructor
                
                /** CODE **/
                private : Shell () : QObject()
                {}
            
            /**********************************************************************************************************************************************************************************************************/
            /*********************************************************************************************** DESTRUCTOR ***********************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
                
                /** DOCUMENTATION **/
                // Empty destructor
                
                /** CODE **/
                private : virtual ~Shell ()
                {}
                
            /**********************************************************************************************************************************************************************************************************/
            /************************************************************************************************* METHODS ************************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Shows a debug message
                
                /** CODE **/
                public : void debug (string message)
                {
                    
                    // We write a message in blue
                    message = "<b><font color=\"blue\">[DEBUG]</font></b> " + message;
                    emit(newText(message.c_str()));
                    
                }
            
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Shows an error message and exits
                
                /** CODE **/
                public : void error (string message)
                {
                    
                    // We write a message in red
                    message = "<b><font color=\"red\">[ERROR]</font></b> " + message;
                    emit(newText(message.c_str()));
                    
                    // We close the GUI before exiting
                    stop(true);
                    exit(EXIT_FAILURE);
                    
                }
            
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Indicates that the shell should close when the program ends
                
                /** CODE **/
                public : void forceCloseAtEnd ()
                {
                    
                    // Setter for the closeAtEnd argument
                    _closeAtEnd = true;
                    
                }
            
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Getter for the unique shell instance
                
                /** CODE **/
                public : static Shell& getInstance ()
                {
                    
                    // We create the instance at first call
                    static Shell instance;
                    return instance;
                    
                }
                
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Shows an information message
                
                /** CODE **/
                public : void info (string message)
                {
                    
                    // We write a message in green
                    message = "<b><font color=\"green\">[INFO]</font></b> " + message;
                    emit(newText(message.c_str()));
                    
                }
            
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Initializes the shell
                // Creates the window, branches the signals to slots and starts the main loop
                // This function is executed in a different thread
                
                /** CODE **/
                private : void initialize ()
                {

                    // We initialize the application
                    int applicationArgc = 0;
                    char** applicationArgv = nullptr;
                    QApplication application(applicationArgc, applicationArgv);
                    
                    // We add a window
                    QWidget window;
                    window.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT);
                    window.setWindowTitle(WINDOW_TITLE.c_str());
                    window.setStyleSheet(("background-color:" + WINDOW_BACKGROUND_COLOR + ";").c_str());
                    char buffer[MAX_PATH + 1];
                    readlink("/proc/self/exe", buffer, MAX_PATH);
                    string currentDirectory = string(buffer).substr(0, string(buffer).find_last_of("/\\"));
                    string iconFileName = currentDirectory + ICON_FILE_NAME;
                    window.setWindowIcon(QIcon(iconFileName.c_str()));
                    
                    // We add a grid layout
                    QGridLayout gridLayout(&window);
                    gridLayout.setContentsMargins(ELEMENTS_SPACING, ELEMENTS_SPACING, ELEMENTS_SPACING, ELEMENTS_SPACING);
                    gridLayout.setHorizontalSpacing(ELEMENTS_SPACING);
                    window.setLayout(&gridLayout);
                    
                    // We add an image
                    QLabel label(&window);
                    string imageFileName = currentDirectory + IMAGE_FILE_NAME;
                    QPixmap image(imageFileName.c_str());
                    label.setPixmap(image.scaledToHeight(WINDOW_HEIGHT - 2 * ELEMENTS_SPACING));
                    gridLayout.addWidget(&label, 0, 0);

                    // We add a text area
                    QTextEdit textEdit(&window);
                    textEdit.setReadOnly(true);
                    textEdit.setLineWrapMode(QTextEdit::WidgetWidth);
                    textEdit.setStyleSheet(("background-color:" + TEXT_EDIT_BACKGROUND_COLOR + ";").c_str());
                    gridLayout.addWidget(&textEdit, 0, 1);
                    
                    // Signal to update the text area when asked
                    connect(this, SIGNAL(newText(QString)), &textEdit, SLOT(append(QString)));
                    
                    // Signal to properly close the GUI at the end of the program
                    connect(this, SIGNAL(programStops()), &application, SLOT(quit()));
                    
                    // Main loop
                    window.show();
                    _mutex.unlock();
                    application.exec();

                }

            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Starts the GUI thread
                
                /** CODE **/
                public : void start ()
                {
                    
                    // We initialize the GUI
                    _mutex.lock();
                    _applicationThread = new class thread(&Shell::initialize, this);
                    _mutex.lock();
                    
                }
            
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Stops the GUI, or waits until it is closed, depending on the user choice
                
                /** CODE **/
                public : void stop (bool error)
                {
                    
                    // We wait for the user to close the window if asked or if an error occurred, otherwise we close it
                    if (_closeAtEnd && !error)
                        emit(programStops());
                    
                    // We wait for the window to close properly
                    _applicationThread->join();
                    
                }
            
            /**********************************************************************************************************************************************************************************************************/
            
                /** DOCUMENTATION **/
                // Shows a warning message
                
                /** CODE **/
                public : void warning (string message)
                {
                    
                    // We write a message in orange
                    message = "<b><font color=\"orange\">[WARNING]</font></b> " + message;
                    emit(newText(message.c_str()));
                    
                }
            
            /**********************************************************************************************************************************************************************************************************/
            /**********************************************************************************************************************************************************************************************************/
            
        };
        
        // To allow header implementation with Qt
        #include "moc_Shell.cpp"
        
    #endif
    
/**********************************************************************************************************************************************************************************************************************************/
/**********************************************************************************************************************************************************************************************************************************/
