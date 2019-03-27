# -*- coding: utf-8 -*-

import constantes
import utile

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"

import os
import pygame
from pygame.locals import QUIT


class Affichage(object):
	def __init__(self):
		self.fenetre = pygame.display.set_mode(constantes.TAILLE_ECRAN)
		self.images = {}

	def charge_images(self):
		print("Chargement des images !")

		# Pour chaque image dans constantes.IMAGES
		for chemin_image in constantes.IMAGES:
			chemin_image = os.path.join("data", "images", *chemin_image)

			try:
				self.images[chemin_image] = pygame.image.load(chemin_image)
				print("L'image {image} a été chargé !".format(image=chemin_image))
			except pygame.error:
				print("L'image {image} n'existe pas !".format(image=chemin_image))

	def obtenir_image(self, chemin_image):
		if chemin_image in self.images:
			# si l'image existe, on la renvoie
			return self.images[chemin_image].convert_alpha()
		else:
			# sinon, on renvoie une surface noire de 50x50 pixels
			return pygame.Surface((50, 50))

	def actualise(self, niveau):
		# On rend tous les pixels de la fenetre noir
		self.fenetre.fill((0, 0, 0))

		# si le niveau a une texture, on affiche cette texture
		if niveau.texture:
			self.fenetre.blit(niveau.texture, (0, 0))

		# On affiche la texture du joueur au milieu de la fenetre
		# les "//" permettent d'obtenir un nombre entier
		# même si la division ne tombe pas juste
		milieu_x = constantes.TAILLE_ECRAN[0] // 2
		milieu_y = constantes.TAILLE_ECRAN[1] // 2
		self.fenetre.blit(niveau.joueur.texture, (milieu_x, milieu_y))

		# On actualise l'écran
		pygame.display.update()

	def actualise_evenements(self):
		for evenement in pygame.event.get():
			# si l'utilisateur a cliqué sur la croix rouge
			# on arrete le jeu
			if evenement.type == QUIT:
				utile.arret()