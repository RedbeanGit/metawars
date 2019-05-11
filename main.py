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
import pygame

def lancer_jeu():
    """ Fonction principale du jeu (à ne lancer qu'une seule fois) """
    
    # on creer un nouvel "affichage" (fenetre)
    affichage = Affichage()
    # on charge l'ensemble des images du jeu
    affichage.charge_images()
    # on crée les widgets du niveau
    affichage.creer_widgets_menu(lancer_partie)

    # on creer un niveau de jeu
    niveau_menu = Niveau(affichage)
    # le niveau et les entités recupères les images dont elles ont besoin
    niveau_menu.charge_image()

    # cette variable retient le temps (en seconde) du dernier tick de jeu
    temps_precedent = time.time()

    while True:
        # cette variable stocke le temps écoulé depuis le dernier tick de jeu
        temps_ecoule = time.time() - temps_precedent
        temps_precedent = time.time()

        # on gère les evenements utilisateurs (clic, appui sur une touche, etc)
        affichage.actualise_evenements(niveau_menu, False)
        # on actualise le niveau et les entités qu'il contient
        niveau_menu.actualise(temps_ecoule)
        # on redessine la fenetre pour afficher de nouveau le niveau
        affichage.actualise(niveau_menu, False)


    
def lancer_partie(affichage):
    # on supprime tous les widgets de la fenêtre
    affichage.supprimer_widgets()
    # on crée les widgets du niveau
    affichage.creer_widgets_niveau()

    # on creer un niveau de jeu
    niveau_jeu = Niveau(affichage)
    # le niveau et les entités recupères les images dont elles ont besoin
    niveau_jeu.charge_image()

    # cette variable retient le temps (en seconde) du dernier tick de jeu
    temps_precedent = time.time()

    while True:
        # cette variable stocke le temps écoulé depuis le dernier tick de jeu
        temps_ecoule = time.time() - temps_precedent
        temps_precedent = time.time()

        # on gère les evenements utilisateurs (clic, appui sur une touche, etc)
        affichage.actualise_evenements(niveau_jeu, True)
        # on actualise le niveau et les entités qu'il contient
        niveau_jeu.actualise(temps_ecoule)
        # on redessine la fenetre pour afficher de nouveau le niveau
        affichage.actualise(niveau_jeu, True)

    # une fois sortie de la boucle, on re-supprime tous les widgets
    affichage.supprimer_widgets()
    # puis on recrée les widgets du menu
    affichage.creer_widgets_menu(lancer_partie)


if __name__ == "__main__":
    # Si notre fichier est lancé directement par python et pas
    # importé par un autre script alors on lance le jeu
    print("Démarrage de {nom}...".format(nom=constantes.NOM))
    lancer_jeu()
