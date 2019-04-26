# -*- coding: utf-8 -*-

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"


NOM = "MetaWars"
ZOOM = 150
POLICE = "police.ttf"

FREQUENCE_APPARITION_ENNEMI = 3
FREQUENCE_APPARITION_BONUS = 3
FREQUENCE_TIR = 1

VITESSE_JOUEUR = 1.2
VITESSE_ENNEMI = 1
VITESSE_TIR = 6

VIE_JOUEUR = 20
VIE_ENNEMI = 5

TAILLE_ECRAN = (1600, 900)
TAILLE_CARTE = (100, 100)
TAILLE_BONUS = (0.4, 0.4)


DEGAT_JOUEUR = 1
DEGAT_ENNEMI = 0.5

DIS_MIN_ENNEMI = 1.2
DIS_MAX_ENNEMI = 5
DIS_MAX_BONUS = 4
ZONE_AUTOUR_JOUEUR = 1.5
ZONE_AUTOUR_ENNEMI = 0.5
HIT_BOX = (0.2, 0.2)


PIECE_ENNEMI = 10

BONUS_SOIN = 10
BONUS_VITESSE = 0.2
BONUS_FREQUENCE_TIR = 2
BONUS_DEGAT = 0.5

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

TYPE_BONUS = [
	"soin",
	"frequence_tir_acceleree",
	"vitesse_augmentee",
	"arme_amelioree"
]