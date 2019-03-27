#!/usr/bin/python3
# -*- coding: utf-8 -*-

import constantes
import utile

from affichage import Affichage
from niveau import Niveau

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"

import time


def main():
	# Fonction principale du jeu
	# Creer une fenetre
	# Creer une boucle infinie pour tenir la fenetre en vie
    
    affichage = Affichage()
    affichage.charge_images()

    niveau = Niveau()
    niveau.charge_image(affichage)

    temps_precedent = time.time()

    while True:
    	temps_ecoule = time.time() - temps_precedent
    	temps_precedent = time.time()

    	affichage.actualise_evenements()
    	niveau.actualise(temps_ecoule)
    	affichage.actualise(niveau)

    	#print("fps={fps}".format(fps=1 / temps_ecoule))


if __name__ == "__main__":
	# Si notre fichier est lancé directement par python et pas
	# importé par un autre script alors on lance le jeu
    print("Démarrage de {nom}...".format(nom=constantes.NOM))
    main()
