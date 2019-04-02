# -*- coding: utf-8 -*-

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"


NOM = "MetaWars"
TAILLE_ECRAN = (800, 800)
TAILLE_CARTE = (100, 100)
ZOOM = 300

VITESSE_JOUEUR = 40
VITESSE_ENNEMI = 30

DEGAT_TIR = 1

# Chemin de fichier vers l'ensemble des images du jeu
# chaque nom de dossier et fichier est une chaine de caractère
# le chemin est inscrit dans une liste
# ainsi, "bonus/life_restore.png" donnera ["bonus", "life_restore.png"]
IMAGES = [
	["bonus", "soin.png"],
	["bonus", "frequence_de_tir_acceleree.png"],
	["bonus", "bouclier_solidifie.png"],
	["bonus", "vitesse_augmentee.png"],
	["bonus", "arme_amelioree.png"],
	["bouton", "clic_gauche.png"],
	["bouton", "desactive.png"],
	["bouton", "survol.png"],
	["bouton", "clic_central.png"],
	["bouton", "normal.png"],
	["bouton", "clic_droit.png"],
	["ennemi", "ennemi.png"],
	["ennemi", "ennemi_touche.png"],
	["joueur", "joueur_0.png"],
	["joueur", "joueur_1.png"],
	["joueur", "joueur_2.png"],
	["joueur", "joueur_3.png"],
	["joueur", "joueur_4.png"],
	["joueur", "joueur_5.png"],
	["joueur", "joueur_6.png"],
	["joueur", "joueur_7.png"],
	["joueur", "joueur_8.png"],
	["joueur", "joueur_9.png"],
	["joueur", "joueur_coeur.png"],
	["joueur", "joueur_coeur_touche.png"],
	["tir", "gros_tir.png"],
	["tir", "tir.png"],
	["companie.png"],
	["image_demarrage.png"],
	["titre.png"],
	["fond_carte.png"]
]

SONS = [
	["gros_tir.wav"],
	["bonus.wav"],
	["clic_bouton.wav"],
	["touche.wav"],
	["mort_joueur.wav"],
	["musique_partie.wav"],
	["musique_menu.wav"],
	["tir.wav"],
	["musique_demarrage.wav"]
]

TYPE_DE_BONUS = ["soin", "frequence_de_tir_acceleree", "bouclier_solidifie", "vitesse_augmentee", "arme_amelioree"]