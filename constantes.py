# -*- coding: utf-8 -*-

"""
	Ce fichier contient toutes les constantes nécessaires au bon fonctionnement du jeu.
"""

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"


NOM = "MetaWars"
ZOOM = 110
POLICE = "police.ttf"

FREQUENCE_APPARITION_ENNEMI = 2.5
FREQUENCE_APPARITION_BONUS = 3
FREQUENCE_TIR_JOUEUR = 1
FREQUENCE_TIR_ENNEMI = 1

VITESSE_JOUEUR = 4
VITESSE_ENNEMI = 1
VITESSE_TIR = 8

VIE_JOUEUR = 20
VIE_ENNEMI = 5

TAILLE_ECRAN = (800, 450)
TAILLE_BONUS = (0.6, 0.6)
TAILLE_TIR = (0.05, 0.05)

DEGAT_JOUEUR = 1
DEGAT_ENNEMI = 0.5

DIS_MIN_ENNEMI = 1.2
DIS_MAX_ENNEMI = 5
DIS_MAX_BONUS = 4
ZONE_AUTOUR_JOUEUR = 1.5
ZONE_AUTOUR_ENNEMI = 0.5

DUREE_BONUS = 5
DUREE_TIR = 2.5
DUREE_ANIMATION_DEGAT = 0.1

PIECE_ENNEMI = 10

BONUS_SOIN = 2
BONUS_VITESSE = 0.15
BONUS_FREQUENCE_TIR = 2
BONUS_DEGAT = 0.25

# Chemin de fichier vers l'ensemble des images du jeu
# chaque nom de dossier et fichier est une chaine de caractère
# le chemin est inscrit dans une liste
# ainsi, "bonus/life_restore.png" donnera ("bonus", "life_restore.png")
IMAGES = (
	("bonus", "soin.png"),
	("bonus", "bouclier_solidifie.png"),
	("bonus", "vitesse_augmentee.png"),
	("bonus", "arme_amelioree.png"),
	("bouton", "clic_gauche.png"),
	("bouton", "desactive.png"),
	("bouton", "survol.png"),
	("bouton", "clic_central.png"),
	("bouton", "normal.png"),
	("bouton", "clic_droit.png"),
	("ennemi", "ennemi.png"),
	("ennemi", "ennemi_touche.png"),
	("joueur", "joueur.png"),
	("joueur", "joueur_touche.png"),
	("joueur", "joueur_bouclier.png"),
	("tir", "gros_tir.png"),
	("tir", "tir.png"),
	("companie.png",),
	("image_demarrage.png",),
	("titre.png",),
	("fond_carte.png",)
)

SONS = (
	("gros_tir.wav",),
	("bonus.wav",),
	("clic_bouton.wav",),
	("touche.wav",),
	("mort_joueur.wav",),
	("musique_partie.wav",),
	("musique_menu.wav",),
	("tir.wav",),
	("musique_demarrage.wav",)
)

TYPE_BONUS = (
	"soin",
	"vitesse_augmentee",
	"arme_amelioree"
)