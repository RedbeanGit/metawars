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
		self.image = None
		self.joueur = Joueur(self)
		self.entites = []

	def charge_image(self, affichage):
		
		# on a quelques petits soucis avec le chargement du fond de carte :-p
		"""
		taille_pixel_x = constantes.TAILLE_CARTE[0] * constantes.ZOOM
		taille_pixel_y = constantes.TAILLE_CARTE[1] * constantes.ZOOM
		self.image = affichage.obtenir_image(os.path.join("data", "images", "fond_carte.png"))
		self.image = pygame.transform.scale(self.image, (taille_pixel_x, taille_pixel_y))
		"""

		self.joueur.charge_image(affichage)

	def actualise(self, temps):
		self.joueur.actualise(temps)
		
		for entite in self.entites:
			entite.actualise(temps)

	def fait_apparaitre(self, temps):
		""" Doit aléatoirement faire apparaitre des ennemis et des bonus """
		nb = random.random(0, constantes.FREQUENCE_APPARITION_ENNEMI / temps)

		if nb == 0:
			# ajouter un ennemi

	def enleve_entite(self, entite):
		""" Enleve l'entite de self.entites seulement
			si elle fait parti de ce niveau """
		pass