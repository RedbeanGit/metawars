# -*- coding: utf-8 -*-

import constantes
import utile
from entites import Joueur
import niveau

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"

import os
import pygame


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
			return pygame.Surface((50, 50))

	def actualise(self, niveau):
		# On rend tous les pixels de la fenetre blanc
		self.fenetre.fill((255, 255, 255))

		# si le niveau a une image de fond, on l'affiche
		if niveau.image:
			self.fenetre.blit(niveau.image, (0, 0))

		# on affiche les entités (dont le joueur)
		self.affiche_entite(niveau.joueur)

		for entite in niveau.entites:
			self.affiche_entite(entite)

		# On actualise l'écran
		pygame.display.update()

	def actualise_evenements(self, niveau):
		# on parcourt l'ensemble des evenements utilisateurs (clic, appui sur une touche, etc)
		for evenement in pygame.event.get():

			# si l'utilisateur appui sur une touche du clavier...
			if evenement.type == pygame.KEYDOWN:
				# si cette touche est W (ou Z sur les claviers français)
				if evenement.key == pygame.K_w:
					niveau.joueur.haut()
					print("Le joueur va en haut")
				if evenement.key == pygame.K_s:
					niveau.joueur.bas()
					print("Le joueur va en bas")
				if evenement.key == pygame.K_a:
					niveau.joueur.gauche()
					print("Le joueur va à gauche")
				if evenement.key == pygame.K_d:
					niveau.joueur.droite()
					print("Le joueur va à droite")
				if evenement.key == pygame.K_LSHIFT:
					niveau.joueur.stop()
					print("Le joueur s'arrete")

			# si il clique avec la souris
			elif evenement.type == pygame.MOUSEBUTTONDOWN:
				# si le bouton cliqué est le bouton droit de la souris (3)
				if evenement.button == 1:
					niveau.joueur.tir()
					print("Le joueur tir")

			# si l'utilisateur a cliqué sur la croix rouge de la fenêtre
			# on arrete le jeu
			if evenement.type == pygame.QUIT:
				utile.arreter()

	def affiche_entite(self, entite):
		# on recuper le milieu de l'ecran
		milieu_ecran_x = constantes.TAILLE_ECRAN[0] // 2
		milieu_ecran_y = constantes.TAILLE_ECRAN[1] // 2

		# on recupere le milieu de l'entite
		milieu_entite_x = entite.taille[0] * constantes.ZOOM / 2
		milieu_entite_y = entite.taille[1] * constantes.ZOOM / 2

		# on calcul la position de l'entité par rapport au joueur
		# car celui-ci doit être centré en plein milieu de l'écran
		entite_x = (entite.position[0] - entite.niveau.joueur.position[0]) * constantes.ZOOM + milieu_ecran_x
		entite_y = (entite.position[1] - entite.niveau.joueur.position[1]) * constantes.ZOOM + milieu_ecran_y

		# on applique une rotation sur l'image en fonction de l'angle de l'entite
		# mais il faut d'abord convertir l'angle de l'entite en degrés (pygame travaille avec des degrés)
		angle_degres = utile.radian_en_degres(entite.angle)
		image_tournee = pygame.transform.rotate(entite.image, angle_degres)

		# on colle l'image de l'entité
		self.fenetre.blit(image_tournee, (entite_x - milieu_entite_x, entite_y - milieu_entite_y))