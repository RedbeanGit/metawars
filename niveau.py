# -*- coding: utf-8 -*-

import constantes
from entites import Joueur

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"

import os
import pygame


class Niveau(object):
	"""
	Gere l'ensemble des entités du jeu.
	"""

	def __init__(self):
		self.texture = None
		self.joueur = Joueur(self)
		self.entites = []

	def charge_image(self, affichage):
		# Cette methode ne fonctionne pas sur Windows
		# a vous de regler le probleme ehe :-p
		
		#taille_pixel_x = constantes.TAILLE_CARTE[0] * constantes.ZOOM
		#taille_pixel_y = constantes.TAILLE_CARTE[1] * constantes.ZOOM
		#self.texture = affichage.obtenir_image(os.path.join("data", "images", "fond_carte.png"))
		#self.texture = pygame.transform.scale(self.texture, (taille_pixel_x, taille_pixel_y))

		self.joueur.charge_image(affichage)

	def actualise(self, temps):
		self.joueur.actualise(temps)
		
		for entite in self.entites:
			entite.actualise(temps)