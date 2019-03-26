#!/usr/bin/python3
# -*- coding: utf-8 -*-

import constants
import util

from display import Display
from level import Level

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"

import time


def main():
	# Fonction principale du jeu
	# Creer une fenetre
	# Creer une boucle infinie pour tenir la fenetre en vie
    
    display = Display()
    display.load_images()

    level = Level()
    level.load_image(display)
    level.init_player()
    level.player.load_image(display)

    last_time = time.time()

    while True:
    	deltatime = time.time() - last_time
    	last_time = time.time()

    	display.update_events()
    	level.update(deltatime)
    	display.update(level)

    	print("fps={fps}".format(fps=1 / deltatime))


if __name__ == "__main__":
	# Si notre fichier est lancé directement par python et pas
	# importé par un autre script alors on lance le jeu
    print("Démarrage de {name}...".format(name=constants.NAME))
    main()
