# -*- coding: utf-8 -*-

#	This file is part of Metawars.
#
#	Metawars is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	Metawars is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with Metawars. If not, see <https://www.gnu.org/licenses/>

"""
	Ce fichier contient toutes les constantes nécessaires au bon
	fonctionnement du jeu.
"""

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"

from os import path as op


class Chemin:
	""" Regroupe tous les chemins de fichiers du jeu. """

	RESSOURCES = op.join("..", "ressources")
	IMAGES = op.join(RESSOURCES, "images")
	SONS = op.join(RESSOURCES, "sons")


class General:
	""" Regroupe les constantes générales du jeu. """

	NOM = "MetaWars"
	ZOOM = 110
	POLICE = "police.ttf"
	DEBUG = True
	VERSION = "3 (Réseau) (sous GNU GPL v3)"
	TAILLE_ECRAN = (800, 450)
	IMAGE_ICONE = op.join(Chemin.IMAGES, "icone.png")
	IMAGE_TITRE = op.join(Chemin.IMAGES, "titre.png")
	IMAGE_FOND = op.join(Chemin.IMAGES, "fond_carte.png")
	ERREURS = ("INFO", "ATTENTION", "ERREUR")


class Joueur:
	""" Regroupe les constantes liées au joueur. """

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
	""" Regroupe les constantes liées aux ennemis. """

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
	""" Regroupe les constantes liées aux bonus. """

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
	""" Regroupe les constantes liées aux tirs. """

	VITESSE = 8
	TAILLE = (0.05, 0.05)
	DUREE = 2.5
	IMAGE = op.join(Chemin.IMAGES, "tir", "tir.png")


class Ressources:
	""" Regroupe les noms des sons et images du jeu sous la forme:
		(nomDossier, nomSousDossier, ..., nomFichier). """

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