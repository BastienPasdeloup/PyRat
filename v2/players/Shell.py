#!/usr/bin/env python3
# -*- coding: utf-8 -*-
####################################################################################################################################################################################################################################
############################################################################################################## LICENSE #############################################################################################################
####################################################################################################################################################################################################################################
#
#    Copyright © 2016 Bastien Pasdeloup (name.surname@gmail.com) and Télécom Bretagne
#
#    This file is part of PyRat.
#
#    PyRat is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    PyRat is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with PyRat.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################################################################################################################################################
############################################################################################################## IMPORTS #############################################################################################################
####################################################################################################################################################################################################################################

### EXTERNAL ###
import os
import sys
import threading
import time
import PyQt4.QtCore
import PyQt4.QtGui

####################################################################################################################################################################################################################################
############################################################################################################### CLASS ##############################################################################################################
####################################################################################################################################################################################################################################

class Shell (PyQt4.QtCore.QObject) :
    
    ############################################################################################################################################################################################################################
    ######################################################################################################### CONSTANTS ########################################################################################################
    ############################################################################################################################################################################################################################

        ### DOCUMENTATION ###
        # Spacing between the elements, and distance to the window border

        ### CODE ###
        ELEMENTS_SPACING = 10
        
    ############################################################################################################################################################################################################################
        
        ### DOCUMENTATION ###
        # Image file to use for the icon

        ### CODE ###
        ICON_FILE_NAME = "/resources/various/pyrat.ico"
        
    ############################################################################################################################################################################################################################
        
        ### DOCUMENTATION ###
        # Image files to use for the first player

        ### CODE ###
        IMAGE_FILE_NAME_PLAYER_1 = "/resources/illustrations/rat.png"
        
    ############################################################################################################################################################################################################################
        
        ### DOCUMENTATION ###
        # Image files to use for the second player

        ### CODE ###
        IMAGE_FILE_NAME_PLAYER_2 = "/resources/illustrations/python_right.png"
        
    ############################################################################################################################################################################################################################
        
        ### DOCUMENTATION ###
        # Background color of the text edit

        ### CODE ###
        TEXT_EDIT_BACKGROUND_COLOR = "#AAAAAA"
        
    ############################################################################################################################################################################################################################
        
        ### DOCUMENTATION ###
        # Background color of the shell

        ### CODE ###
        WINDOW_BACKGROUND_COLOR = "#222222"
        
    ############################################################################################################################################################################################################################
        
        ### DOCUMENTATION ###
        # Height of the shell

        ### CODE ###
        WINDOW_HEIGHT = 350
        
    ############################################################################################################################################################################################################################
        
        ### DOCUMENTATION ###
        # Title of the shell

        ### CODE ###
        WINDOW_TITLE = "PyRat - Shell for script [FILE_NAME]"
        
    ############################################################################################################################################################################################################################
        
        ### DOCUMENTATION ###
        # Width of the shell

        ### CODE ###
        WINDOW_WIDTH = 900
        
    ############################################################################################################################################################################################################################
    ####################################################################################################### CONSTRUCTORS #######################################################################################################
    ############################################################################################################################################################################################################################
        
        ### DOCUMENTATION ###
        # Extends QObject to allow sending custom signals from the object
        # Initializes the mutual exclusion tools that will be used to make the GUI work properly in a different thread
        
        ### CODE ###
        def __init__ (self) :
            
            # Parent constructor
            super().__init__()
            
            # Attributes
            self.applicationThread = None
            self.mutex = threading.Lock()
            self.closeAtEnd = False
        
    ############################################################################################################################################################################################################################
    ######################################################################################################## DESTRUCTOR ########################################################################################################
    ############################################################################################################################################################################################################################
        
        ### DOCUMENTATION ###
        # Default constructor
        
        ### CODE ###
        def __del__ (self) :
            
            pass
        
    ############################################################################################################################################################################################################################
    ########################################################################################################## METHODS #########################################################################################################
    ############################################################################################################################################################################################################################
        
        ### DOCUMENTATION ###
        # This method is required not to crash when the print function is called
        # In practice, we do not need to flush anything here
        
        ### CODE ###
        def flush (self) :
            
            pass
        
    ############################################################################################################################################################################################################################
    
        ### DOCUMENTATION ###
        # Customizes the shell with the player's name and the correct picture
        
        ### CODE ###
        def customize (self, playerFileName, playerNumber) :
            
            # Title of the window
            windowTitle = Shell.WINDOW_TITLE.replace("[FILE_NAME]", str(playerFileName))
            self.emit(PyQt4.QtCore.SIGNAL("windowTitleAvailable(QString)"), windowTitle)
            
            # Image
            if playerNumber == 1 :
                self.emit(PyQt4.QtCore.SIGNAL("playerIsNumber1()"))
            else :
                self.emit(PyQt4.QtCore.SIGNAL("playerIsNumber2()"))
        
    ############################################################################################################################################################################################################################
    
        ### DOCUMENTATION ###
        # Forces the shell to close at the end of the program
        
        ### CODE ###
        def forceCloseAtEnd (self) :
            
            # Setter
            self.closeAtEnd = True
        
    ############################################################################################################################################################################################################################
    
        ### DOCUMENTATION ###
        # Sets up the window in critical session so that no message is printed during initialization
        
        ### CODE ###
        def initialize (self) :
            
            # We initialize the application
            application = PyQt4.QtGui.QApplication(sys.argv)
            
            # We add a window
            window = PyQt4.QtGui.QWidget()
            window.resize(Shell.WINDOW_WIDTH, Shell.WINDOW_HEIGHT)
            window.setStyleSheet("background-color:" + Shell.WINDOW_BACKGROUND_COLOR + ";")
            currentDirectory = os.path.dirname(os.path.realpath(__file__))
            window.setWindowIcon(PyQt4.QtGui.QIcon(currentDirectory + Shell.ICON_FILE_NAME))
            
            # We add a grid layout
            gridLayout = PyQt4.QtGui.QGridLayout()
            gridLayout.setContentsMargins(Shell.ELEMENTS_SPACING, Shell.ELEMENTS_SPACING, Shell.ELEMENTS_SPACING, Shell.ELEMENTS_SPACING)
            gridLayout.setHorizontalSpacing(Shell.ELEMENTS_SPACING)
            window.setLayout(gridLayout)
            
            # We create labels for both images, but only one will be used
            labels = []
            for i in range(2) :
                labels.append(PyQt4.QtGui.QLabel())
                image = PyQt4.QtGui.QPixmap(currentDirectory + Shell.IMAGE_FILE_NAME_PLAYER_1 if i == 0 else currentDirectory + Shell.IMAGE_FILE_NAME_PLAYER_2).scaledToHeight(Shell.WINDOW_HEIGHT - 2 * Shell.ELEMENTS_SPACING)
                labels[i].setPixmap(image)
                gridLayout.addWidget(labels[i], 0, 0)
                labels[i].hide()

            # We add a text area
            textEdit = PyQt4.QtGui.QTextEdit()
            textEdit.setReadOnly(True)
            textEdit.setLineWrapMode(PyQt4.QtGui.QTextEdit.WidgetWidth)
            textEdit.setStyleSheet("background-color:" + Shell.TEXT_EDIT_BACKGROUND_COLOR + ";")
            gridLayout.addWidget(textEdit, 0, 1)
            
            # Signal to update the text area when asked
            self.connect(self, PyQt4.QtCore.SIGNAL("newText(QString)"), textEdit, PyQt4.QtCore.SLOT("append(QString)"));
            
            # Signal to properly close the GUI at the end of the program
            self.connect(self, PyQt4.QtCore.SIGNAL("programStops()"), application, PyQt4.QtCore.SLOT("quit()"));
            
            # Signal to update the window when new information is available
            self.connect(self, PyQt4.QtCore.SIGNAL("windowTitleAvailable(QString)"), window, PyQt4.QtCore.SLOT("setWindowTitle(QString)"));
            self.connect(self, PyQt4.QtCore.SIGNAL("playerIsNumber1()"), labels[0], PyQt4.QtCore.SLOT("show()"));
            self.connect(self, PyQt4.QtCore.SIGNAL("playerIsNumber2()"), labels[1], PyQt4.QtCore.SLOT("show()"));
            
            # Main loop
            window.show()
            self.mutex.release()
            application.exec_()
        
    ############################################################################################################################################################################################################################
    
        ### DOCUMENTATION ###
        # Initializes the shell and routes the calls to print on stdout and stderr
        # This method must be called in a single-thread context
        
        ### CODE ###
        def start (self) :
            
            # Redirection of all writes to stdout and stderr
            sys.stdout = self
            sys.stderr = self
            
            # We initialize the GUI
            self.mutex.acquire()
            self.applicationThread = threading.Thread(target=self.initialize)
            self.applicationThread.start()
            self.mutex.acquire()
        
    ############################################################################################################################################################################################################################
    
        ### DOCUMENTATION ###
        # Waits for the user to close the GUI at the end of the program if asked
        # Otherwise, closes the window directly
        
        ### CODE ###
        def stop (self, error) :
            
            # We indicate the time to wait before the window closes
            if (self.closeAtEnd and not error) :
                self.emit(PyQt4.QtCore.SIGNAL("programStops()"))
            
            # We wait for the window to close properly
            self.applicationThread.join()
        
    ############################################################################################################################################################################################################################
    
        ### DOCUMENTATION ###
        # This method is where writes on stdout or stderr are redirected
        
        ### CODE ###
        def write (self, message) :
            
            # We write the message to the shell
            message = message.strip()
            if len(message) > 0 and message != "\n" :
                self.emit(PyQt4.QtCore.SIGNAL("newText(QString)"), str(message))
        
    ############################################################################################################################################################################################################################
    ############################################################################################################################################################################################################################

####################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################