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
		# on cree une fenetre
		self.fenetre = pygame.display.set_mode(constantes.TAILLE_ECRAN)
		self.images = {}

		# on defini un titre a notre fenetre (ici: MetaWars)
		pygame.display.set_caption(constantes.NOM)

	def charge_images(self):
		print("Chargement des images...")

		# Pour chaque image dans constantes.IMAGES
		for chemin_image in constantes.IMAGES:
			chemin_image = os.path.join("data", "images", *chemin_image)

			try:
				self.images[chemin_image] = pygame.image.load(chemin_image)
				print("L'image {image} a été chargé !".format(image=chemin_image))
			except pygame.error:
				print("[ERREUR] L'image {image} n'existe pas !".format(image=chemin_image))
		print("Fin du chargement des images !")

	def obtenir_image(self, chemin_image):
		if chemin_image in self.images:
			# si l'image existe, on la renvoie
			return self.images[chemin_image].convert_alpha()
		else:
			# sinon, on renvoie une surface noire de 50x50 pixels
			print("[ERREUR] L'image demandée ({image}) n'a pas été chargée ! Création d'une surface noire".format(image=chemin_image))
			return pygame.Surface((50, 50))

	def actualise(self, niveau):
		# On rend tous les pixels de la fenetre blanc
		self.fenetre.fill((255, 255, 255))

		# si le niveau a une image de fond, on l'affiche
		if niveau.image:
			self.fenetre.blit(niveau.image, (0, 0))

		# On affiche la texture du joueur au milieu de la fenetre:
		# on recuper le milieu de l'ecran
		milieu_x = constantes.TAILLE_ECRAN[0] // 2
		milieu_y = constantes.TAILLE_ECRAN[1] // 2

		# on recupere le milieu du joueur
		milieu_joueur_x = niveau.joueur.taille[0] * constantes.ZOOM / 2
		milieu_joueur_y = niveau.joueur.taille[1] * constantes.ZOOM / 2

		# on colle l'image du joueur
		self.fenetre.blit(niveau.joueur.image, (milieu_x - milieu_joueur_x, milieu_y - milieu_joueur_y))

		# On actualise l'écran
		pygame.display.update()

	def actualise_evenements(self):
		# on parcourt l'ensemble des evenements utilisateurs (clic, appui sur une touche, etc)
		for evenement in pygame.event.get():
			# si l'utilisateur a cliqué sur la croix rouge
			# on arrete le jeu
			if evenement.type == QUIT:
				utile.arreter()