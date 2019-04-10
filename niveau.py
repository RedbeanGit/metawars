# -*- coding: utf-8 -*-

import constantes
from entites import Joueur, Ennemi

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"

import os
import pygame
import random


class Niveau(object):
	"""
	Gere l'ensemble des entités du jeu.
	"""

	def __init__(self, affichage):
		self.image = None
		self.joueur = Joueur(self)
		self.affichage = affichage
		self.entites = []

	def charge_image(self):
		
		# on a quelques petits soucis avec le chargement du fond de carte :-p
		"""
		taille_pixel_x = constantes.TAILLE_CARTE[0] * constantes.ZOOM
		taille_pixel_y = constantes.TAILLE_CARTE[1] * constantes.ZOOM
		self.image = affichage.obtenir_image(os.path.join("data", "images", "fond_carte.png"))
		self.image = pygame.transform.scale(self.image, (taille_pixel_x, taille_pixel_y))
		"""

		self.joueur.charge_image(self.affichage)

	def actualise(self, temps):
		self.joueur.actualise(temps)
		
		for entite in self.entites:
			entite.actualise(temps)

		self.fait_apparaitre(temps)

	def fait_apparaitre(self, temps):
		""" Doit aléatoirement faire apparaitre des ennemis et des bonus """
		# on pioche un nombre aléatoire
		nb = random.random()

		# si le nombre pioché est inférieur au temps écoulé divisé 
		# par la fréquence moyenne d'apparition...
		if nb <= temps / constantes.FREQUENCE_APPARITION_ENNEMI:
			# ...on crée un nouvel ennemi
			ennemi = Ennemi(self)
			
			# on choisi aléatoirement la distance entre l'ennemi et le joueur
			dx = (random.random() - 0.5) * 2 * constantes.DIS_MAX_ENNEMI
			dy = (random.random() - 0.5) * 2 * constantes.DIS_MAX_ENNEMI
			# on redéfinit la position de l'ennemi (pour l'instant sur le joueur)
			ennemi.position[0] = self.joueur.position[0] + dx
			ennemi.position[1] = self.joueur.position[1] + dy

			# on lui fait charger ses images
			ennemi.charge_image(self.affichage)
			# on ajoute l'ennemi a la liste des entités
			self.entites.append(ennemi)

	def enleve_entite(self, entite):
		""" Enleve l'entite de self.entites seulement
			si elle fait parti de ce niveau """
		pass