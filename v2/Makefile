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
############################################################################################################# CONSTANTS ############################################################################################################
####################################################################################################################################################################################################################################

PATH_TO_PYRAT = /usr/share/pyrat
PATH_TO_APACHE = /var/www/html/pyrat
PATH_TO_STUDENT = /home/$$USER/pyrat
PATH_TO_BASHRC = /home/$$USER/.bashrc
PATH_TO_CHROMEDRIVER = /usr/lib/chromium-browser
PATH_TO_PHP = /usr/bin/php

####################################################################################################################################################################################################################################
############################################################################################################# COMMANDS #############################################################################################################
####################################################################################################################################################################################################################################

build:
	cd ./core && qmake-qt4 -project -o pyrat_core.pro && qmake-qt4 pyrat_core.pro && sed -i -- 's#CXX           = g++#CXX           = clang++ -std=c++11 -pthread -O3#g' Makefile && make
	rm ./core/*.o ./core/pyrat_core.pro ./core/Makefile ./core/moc_*

####################################################################################################################################################################################################################################

install:
	sudo mkdir -p $(PATH_TO_PYRAT)/resources $(PATH_TO_PYRAT)/players $(PATH_TO_PYRAT)/core $(PATH_TO_PYRAT)/launchers $(PATH_TO_APACHE)
	sudo cp -r ./resources/* $(PATH_TO_PYRAT)/resources
	sudo cp ./players/* $(PATH_TO_PYRAT)/players
	sudo cp ./launchers/* $(PATH_TO_PYRAT)/launchers
	sudo cp ./gui/* $(PATH_TO_APACHE)
	sudo mv ./core/pyrat_core $(PATH_TO_PYRAT)/core
	sudo ln -sfn $(PATH_TO_PYRAT)/resources $(PATH_TO_PYRAT)/core/resources
	sudo ln -sfn $(PATH_TO_PYRAT)/resources $(PATH_TO_PYRAT)/players/resources
	sudo ln -sfn $(PATH_TO_PYRAT)/resources $(PATH_TO_APACHE)/resources
	sudo ln -sfn $(PATH_TO_PHP) $(PATH_TO_APACHE)/php
	sudo ln -sfn $(PATH_TO_PYRAT)/players/Main.py $(PATH_TO_PYRAT)/players/pyrat_player
	sudo chmod -R 755 $(PATH_TO_PYRAT) $(PATH_TO_APACHE)
	sudo cat ./gui/pyrat.sql | mysql -u root -h 127.0.0.1 -p
	sudo service apache2 restart
	mkdir -p $(PATH_TO_STUDENT)/programs $(PATH_TO_STUDENT)/launchers $(PATH_TO_STUDENT)/savedGames
	cp ./students/programs/* $(PATH_TO_STUDENT)/programs
	cp -r ./students/savedGames/* $(PATH_TO_STUDENT)/savedGames
	cp -r ./students/launchers/* $(PATH_TO_STUDENT)/launchers
	cp ./README.md $(PATH_TO_STUDENT)/
	echo 'export PATH="$(PATH_TO_PYRAT)/core":$$PATH' >> $(PATH_TO_BASHRC)
	echo 'export PATH="$(PATH_TO_PYRAT)/players":$$PATH' >> $(PATH_TO_BASHRC)
	echo 'export PATH="$(PATH_TO_CHROMEDRIVER)":$$PATH' >> $(PATH_TO_BASHRC)
	echo 'export PYTHONPATH="$(PATH_TO_PYRAT)/launchers":$$PYTHONPATH' >> $(PATH_TO_BASHRC)
	echo 'export PYTHONPATH="$(PATH_TO_STUDENT)/programs":$$PYTHONPATH' >> $(PATH_TO_BASHRC)
	
####################################################################################################################################################################################################################################
	
clean:
	sudo rm -rf $(PATH_TO_PYRAT) $(PATH_TO_APACHE)

####################################################################################################################################################################################################################################

cleanAll:
	sudo rm -rf $(PATH_TO_PYRAT) $(PATH_TO_APACHE) $(PATH_TO_STUDENT)

####################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################