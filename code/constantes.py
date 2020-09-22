# -*- coding: utf-8 -*-

"""
	Ce fichier contient toutes les constantes nécessaires au bon fonctionnement du jeu.
"""

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"

from os import path as op


class Chemin:
	RESSOURCES = op.join("..", "data")
	IMAGES = op.join(RESSOURCES, "images")
	SONS = op.join(RESSOURCES, "sons")


class General:
	NOM = "MetaWars"
	ZOOM = 110
	POLICE = "police.ttf"
	DEBUG = True
	TAILLE_ECRAN = (800, 450)
	IMAGE_ICONE = op.join(Chemin.IMAGES, "icone.png")
	IMAGE_TITRE = op.join(Chemin.IMAGES, "titre.png")
	IMAGE_FOND = op.join(Chemin.IMAGES, "fond_carte.png")
	ERREURS = ("INFO", "ATTENTION", "ERREUR")


class Joueur:
	FREQUENCE_TIR = 1
	VITESSE = 4
	VIE = 20
	DEGAT = 1
	ZONE = 1.5
	DUREE_ANIMATION_DEGAT = 0.1
	IMAGE = op.join(Chemin.IMAGES, "joueur", "joueur.png")
	IMAGE_TOUCHE = op.join(Chemin.IMAGES, "joueur", "joueur_touche.png")
	IMAGE_BOUCLIER = op.join(Chemin.IMAGES, "joueur", "joueur_bouclier.png")

class Ennemi:
	FREQUENCE_APPARITION = 2.5
	FREQUENCE_TIR = 1
	VITESSE = 1
	VIE = 5
	DEGAT = 0.5
	DIS_MIN = 1.2
	DIS_MAX = 5
	ZONE = 0.5
	PIECE = 10
	DUREE_ANIMATION_DEGAT = 0.1
	IMAGE = op.join(Chemin.IMAGES, "ennemi", "ennemi.png")
	IMAGE_TOUCHE = op.join(Chemin.IMAGES, "ennemi", "ennemi_touche.png")

class Bonus:
	FREQUENCE_APPARITION = 3
	TAILLE = (0.6, 0.6)
	DIS_MAX = 4
	DUREE = 5
	SOIN = 2
	VITESSE = 0.15
	FREQUENCE_TIR = 2
	DEGAT = 0.25
	IMAGE = lambda t: op.join(Chemin.IMAGES, "bonus", t + ".png")
	TYPES = (
		"soin",
		"vitesse_augmentee",
		"arme_amelioree"
	)

class Tir:
	VITESSE = 8
	TAILLE = (0.05, 0.05)
	DUREE = 2.5
	IMAGE = op.join(Chemin.IMAGES, "tir", "tir.png")


class Ressources:
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