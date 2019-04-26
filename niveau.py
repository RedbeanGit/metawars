# -*- coding: utf-8 -*-

import constantes
from entites import Joueur, Ennemi, Bonus

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
		self.affichage = affichage
		self.joueur = Joueur(self)
		self.entites = []
		self.piece = 0

	def charge_image(self):
		
		# on a quelques petits soucis avec le chargement du fond de carte :-p
		"""
		taille_pixel_x = constantes.TAILLE_CARTE[0] * constantes.ZOOM
		taille_pixel_y = constantes.TAILLE_CARTE[1] * constantes.ZOOM
		self.image = affichage.obtenir_image(os.path.join("data", "images", "fond_carte.png"))
		self.image = pygame.transform.scale(self.image, (taille_pixel_x, taille_pixel_y))
		"""

		self.joueur.charge_image()

	def actualise(self, temps):
		self.joueur.actualise(temps)
		
		for entite in self.entites:
			entite.actualise(temps)

		self.fait_apparaitre(temps)

	def fait_apparaitre(self, temps):
		""" Doit aléatoirement faire apparaitre des ennemis et des bonus """
		# on pioche un nombre aléatoire
		nb = random.random()

		if nb <= temps / constantes.FREQUENCE_APPARITION_BONUS:
			# ...on crée un nouveau bonus
			bonus = Bonus(self)

			# on choisi aléatoirement la distance entre le joueur et le bonus
			dx = (random.random() - 0.5) * 2 * constantes.DIS_MAX_BONUS
			dy = (random.random() - 0.5) * 2 * constantes.DIS_MAX_BONUS

			# on redéfinit la position du Bonus (pour l'instant sur le joueur)
			bonus.position[0] = self.joueur.position[0] + dx + 4
			bonus.position[1] = self.joueur.position[1] + dy + 8

			# on lui fait charger ses images
			bonus.charge_image()

			# on ajoute le bonus a la liste des entités
			self.entites.append(bonus)

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
			ennemi.charge_image()
			# on ajoute l'ennemi a la liste des entités
			self.entites.append(ennemi)

	def enleve_entite(self, entite):
		""" Enleve l'entite de self.entites seulement
			si elle fait parti de ce niveau """

		# si l'entité fait bien parti de la liste des entités de ce niveau
		if entite in self.entites:
			# on la retire de la liste (elle ne fait donc plus parti du niveau)
			self.entites.remove(entite)