# LICENSE 

    Copyright © 2016 Bastien Pasdeloup (name.surname@gmail.com) and Télécom Bretagne

    This file is part of PyRat.

    PyRat is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    PyRat is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with PyRat.  If not, see <http://www.gnu.org/licenses/>.

# PRESENTATION

    Welcome to PyRat software!
    
    PyRat is an educative software in which users are asked to write AIs to control tokens in a maze, in order to collect pieces of cheese.
    It was developed at Télécom Bretagne, Brest (France) to teach programming to students.
    
    This software consists of multiple parts:
    * The PyRat core, that creates the maze, and centralizes the game information.
    * One PyRat player handler per AI, that hides the communication mechanisms between pieces of software and allows AIs to be written as simple Python files.
    * The PyRat GUI, that runs on a web server, along with a database to store the running games and visualize them from a distant browser.
    
    Additionally, PyRat launchers are provided to start pre-customized games.
    They take AIs as arguments, and are located in the "launchers" directory.
    As an example, the launcher "launchers/programVsProgram/Match.py" takes two AI files as arguments, and starts a two players game on a random maze.
    Once the game is over, it is saved to the "savedGames/previousGame" directory, and can be played again with the launcher "launchers/Replay.py".
    Feel free to write your own launchers, by studying the existing ones.
    
    Finally, the AIs must be derived from the "programs/Template.py" file.
    More details are available there, and an example AI "Random.py" is provided to illustrate how things work.
    
    For more precise usage information, please consult this page: "http://formations.telecom-bretagne.eu/pyrat/".
    This website also contains the lessons associated to this software.
    In case of a problem, please contact Bastien Pasdeloup (name.surname@gmail.com).
    
    All images located in the "resources" directory were kindly made by Lauren Lefumeur-Pasdeloup for PyRat.
    They are published under Creative Commons CC-BY license.

# INSTALLATION

    This installation guide contains information that were tested on a fresh Ubuntu 16.04.
    Follow the following instructions in order to install all PyRat components on either your physical machine or a virtual one.
    
    First, we need to install some dependencies.
    During installation of MySQL, a password will be asked.
    Choose the one you want and remember it for later.
    To install all the required packages, run the following command in a shell:
    
    sudo apt-get install qt4-qmake libqt4-dev clang apache2 mysql-server php libapache2-mod-php php-mysql chromium-chromedriver python3-pyqt4 python3-selenium python3-matplotlib python3-numpy python3-evdev
    
    Then, we will install PyRat on the file system.
    From the directory containing this README file, run the following commands.
    Your session password may be asked at the beginning of the installation.
    At some point during installation, another password will be asked.
    Enter the one you set when installing the dependencies before:
    
    make
    make install

    At this point, PyRat is successfully installed on your computer.
    A directory called "pyrat" has been created in your home directory.
    It should contain everything that you need to use the software.
    Open a new shell in that directory and run the following command to start a match against a randomly-playing opponent:
    
    ./launchers/humanVsProgram/KeyboardGame.py ./programs/Random.py
