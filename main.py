#!/usr/bin/python3
# -*- coding: utf-8 -*-

import constantes
import utile

from affichage import Affichage
from niveau import Niveau

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"
__repo__ = "https://github.com/Ptijuju22/metawars.git"

import time


def main():
    """ Fonction principale du jeu (à ne lancer qu'une seule fois) """
    
    # on creer un nouvel "affichage" (fenetre)
    affichage = Affichage()
    # on charge l'ensemble des images du jeu
    affichage.charge_images()
    # on crée les widgets
    affichage.creer_widgets_niveau()

    # on creer un niveau de jeu
    niveau = Niveau(affichage)
    # le niveau et les entités recupères les images dont elles ont besoin
    niveau.charge_image()

    # cette variable retient le temps (en seconde) du dernier tick de jeu
    temps_precedent = time.time()

    while True:
        # cette variable stocke le temps écoulé depuis le dernier tick de jeu
        temps_ecoule = time.time() - temps_precedent
        temps_precedent = time.time()

        # on gère les evenements utilisateurs (clic, appui sur une touche, etc)
        affichage.actualise_evenements(niveau)
        # on actualise le niveau et les entités qu'il contient
        niveau.actualise(temps_ecoule)
        # on redessine la fenetre pour afficher de nouveau le niveau
        affichage.actualise(niveau, temps_ecoule)


if __name__ == "__main__":
    # Si notre fichier est lancé directement par python et pas
    # importé par un autre script alors on lance le jeu
    print("Démarrage de {nom}...".format(nom=constantes.NOM))
    main()
