#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

sys.stdout = open(os.devnull, "w")

import constantes
import utile

from affichage import Affichage
from jeu import Jeu
from niveau import Niveau

sys.stdout.close()
sys.stdout = sys.__stdout__

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"
__repo__ = "https://github.com/Ptijuju22/metawars.git"

import time


def demarrer():
    jeu = Jeu()
    jeu.charger()
    jeu.initialiser_menu_principal()
    jeu.lancer_boucle()


if __name__ == "__main__":
    # Si notre fichier est lancé directement par python et pas
    # importé par un autre script alors on lance le jeu
    utile.debogguer("Démarrage de " + constantes.General.NOM)
    demarrer()
