# -*- coding: utf-8 -*-

import constantes
import utile
import niveau
from widgets import Texte, Bouton

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"

import math
import os
import pygame


class Affichage(object):
	def __init__(self):
		# on cree une fenetre
		self.fenetre = pygame.display.set_mode(constantes.TAILLE_ECRAN)
		self.images = {}
		self.widgets = []

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

	def creer_widgets_niveau(self):
		""" Doit créer un Text pour le temps passé sur le niveau, un pour les pièces
			et un pour indiquer la vie du joueur """

		texte_temps = Texte(self, "Temps: 0", (10, 10))
		texte_pieces = Texte(self, "Pièces: 0", (10, 40))
		texte_vie = Texte(self, "Vie: 0", (10, 70))

		self.widgets.append(texte_temps)
		self.widgets.append(texte_pieces)
		self.widgets.append(texte_vie)

	def creer_widgets_menu(self):
		""" Doit créer un """
		milieu_ecran_x = constantes.TAILLE_ECRAN[0] // 2
		milieu_ecran_y = constantes.TAILLE_ECRAN[1] // 2

		# On verra un peu plus tard pour cette partie là
		#bouton_jouer_menu = Bouton(self, "Jouer", self.commencer_partie, (milieu_ecran_x, milieu_ecran_y))

		#self.widgets.append(bouton_jouer_menu)

	def actualise(self, niveau):
		# On rend tous les pixels de la fenetre blanc
		self.fenetre.fill((255, 255, 255))

		# on affiche le fond du niveau
		self.affiche_carte(niveau)

		# on affiche les entités (dont le joueur)
		self.affiche_entite(niveau.joueur)

		for entite in niveau.entites:
			self.affiche_entite(entite)

		# on actualise le score en fonction de celui du niveau
		self.actualise_scores(niveau)
		# on redessine les widgets
		self.affiche_widgets()

		# On actualise l'écran
		pygame.display.update()

	def actualise_evenements(self, niveau):
		# on parcourt l'ensemble des evenements utilisateurs (clic, appui sur une touche, etc)
		for evenement in pygame.event.get():

			# si l'utilisateur appui sur une touche du clavier...
			if evenement.type == pygame.KEYDOWN:
				# en fonction de la touche appuyée, on appelle la fonction
				# commandant le déplacement correspondant
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

				if evenement.key == pygame.K_ESCAPE:
					utile.arreter()

			# si l'utilisateur relache une touche du clavier...
			elif evenement.type == pygame.KEYUP:
				# en fonction de la touche appuyée, on appelle la fonction
				# commandant le déplacement inverse
				if evenement.key == pygame.K_w:
					niveau.joueur.bas()
					print("Le joueur va en haut")

				if evenement.key == pygame.K_s:
					niveau.joueur.haut()
					print("Le joueur va en bas")

				if evenement.key == pygame.K_a:
					niveau.joueur.droite()
					print("Le joueur va à gauche")

				if evenement.key == pygame.K_d:
					niveau.joueur.gauche()
					print("Le joueur va à droite")

			# si il clique avec la souris
			elif evenement.type == pygame.MOUSEBUTTONDOWN:
				# si le bouton cliqué est le bouton droit de la souris (3)
				if evenement.button == 1:
					niveau.joueur.tir()
					print("Le joueur tir")

			# si la souris bouge
			elif evenement.type == pygame.MOUSEMOTION:
				x, y = evenement.pos

				# on calcul l'écart entre la position de la souris et le milieu de la fenêtre
				dx = x - constantes.TAILLE_ECRAN[0] / 2
				dy = y - constantes.TAILLE_ECRAN[1] / 2

				# on enlève le zoom pour convertir cet écart dans l'échelle du niveau
				dx_niveau = dx / constantes.ZOOM
				dy_niveau = dy / constantes.ZOOM

				# on fait en sorte que le joueur regarde la position de la souris
				niveau.joueur.regarde_position(dx_niveau, dy_niveau)

			# si l'utilisateur a cliqué sur la croix rouge de la fenêtre
			# on arrete le jeu
			if evenement.type == pygame.QUIT:
				utile.arreter()

			# on actualise les évenements pour chaque widget
			for widget in self.widgets:
				widget.actualise_evenement(evenement)

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

		# la taille de l'image a peut-être changé en la tournant
		# il faut donc calculer la différence de taille entre les 2 images
		d_taille_x = image_tournee.get_size()[0] - entite.image.get_size()[0]
		d_taille_y = image_tournee.get_size()[1] - entite.image.get_size()[1]

		# on peut maintenant déterminer la position de l'image
		x = int(entite_x - milieu_entite_x - d_taille_x / 2)
		y = int(entite_y - milieu_entite_y - d_taille_y / 2)

		# on colle l'image de l'entité
		self.fenetre.blit(image_tournee, (x, y))

	def affiche_carte(self, niveau):
		largeur, hauteur = niveau.image.get_size()
		joueur_x, joueur_y = niveau.joueur.position

		distance_joueur_x = (joueur_x * constantes.ZOOM) % largeur
		distance_joueur_y = (joueur_y * constantes.ZOOM) % hauteur

		# on calcule le nombre de texture qu'il va falloir afficher à l'écran
		# en largeur (x) et en hauteur (y)
		# math.ceil renvoie la valeur arrondi supérieure ou égale
		# car il vaut mieux afficher des textures en trop que pas assez
		# sinon il va rester du vide
		nb_texture_x = math.ceil(constantes.TAILLE_ECRAN[0] / largeur)
		nb_texture_y = math.ceil(constantes.TAILLE_ECRAN[1] / hauteur)

		if distance_joueur_x != 0:
			nb_texture_x += 1
		if distance_joueur_y != 0:
			nb_texture_y += 1

		for x in range(nb_texture_x):
			for y in range(nb_texture_y):
				self.fenetre.blit(niveau.image, (x * largeur - distance_joueur_x, y * hauteur - distance_joueur_y))

	def affiche_widgets(self):
		for widget in self.widgets:
			widget.actualise()

	def actualise_scores(self, niveau):
		texte_temps = self.widgets[0]
		texte_pieces = self.widgets[1]
		texte_vie = self.widgets[2]

		texte_temps.texte = "Temps: {temps}".format(temps=int(niveau.temps_total))
		texte_pieces.texte = "Pièces: {pieces}".format(pieces=niveau.piece)
		texte_vie.texte = "Vie: {vie}".format(vie=int(niveau.joueur.vie))
