# -*- coding: utf-8 -*-

import constantes

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"

import os
import math
import pygame
import pygame.freetype

pygame.freetype.init()


class Widget(object):
	""" Classe de base pour tous les widgets (éléments graphiques indépendants). """

	def __init__(self, affichage, position=(0, 0), taille=(1, 1), ancrage=(-1, -1)):
		""" Initialise un widget. 

			<affichage> (affichage.Affichage): La fenêtre sur laquelle dessiner le widget.
			[position] (tuple): La position (x, y) du widget en pixels.
			[taille] (tuple): La taille (largeur, hauteur) du widget en pixels.
			[ancrage] (tuple): Le point (x, y) d'ancrage du widget en pixels. """

		# la fenêtre sur lequel ce widget devra s'afficher
		self.affichage = affichage
		# la position du widget
		self.position = position
		# sa taille
		self.taille = taille

		# son point d'ancrage, définit comment placer le widget par rapport à sa position:
		# (-1, -1) signifie "en haut à gauche" et (1, 1) "en bas à droite"
		# (0, 0) signifie donc "centré"
		self.ancrage = ancrage

	def actualiser(self):
		""" Cette méthode est appelée à chaque frame de jeu pour 
			redessiner le widget sur 'self.affichage'
			Ne fait rien par défaut """
		pass

	def actualiser_evenement(self, evenement):
		""" Cette méthode est appelée pour chaque nouvel évenement (clic, appui sur une touche, ...).
			Ne fait rien par défaut """
		pass

	def obtenir_position_reelle(self):
		""" Renvoie la position du coin supérieur gauche du widget
			en fonction de ses attributs 'position' et 'ancrage' """

		x, y = self.position
		w, h = self.taille
		ax, ay = self.ancrage

		vrai_x = int(x - w*(ax + 1)/2)
		vrai_y = int(y - h*(ay + 1)/2)

		return (vrai_x, vrai_y)

	def est_dans_widget(self, position):
		""" Renvoie True si la position est dans le widget sinon False.

			<position> (tuple): La position (x, y) à tester. """

		x, y = self.obtenir_position_reelle()
		largeur, hauteur = self.taille

		if position[0] >= x and position[0] <= x + largeur:
			if position[1] >= y and position[1] <= y + hauteur:
				return True
		return False


class Texte(Widget):
	""" Permet d'afficher un texte à une position définie. """

	def __init__(self, affichage, texte, position=(0, 0), ancrage=(-1, -1), taille_police=20, couleur=(255, 255, 255)):
		""" Initialise un texte. 

			<affichage> (affichage.Affichage): La fenêtre sur laquelle dessiner le texte.
			<text> (str): Le texte à afficher.
			[position] (tuple): La position (x, y) du texte en pixels.
			[ancrage] (tuple): Le point (x, y) d'ancrage du texte en pixels.
			[taille_police] (int): La hauteur de la police en pixels.
			[couleur] (tuple): La couleur (R, V, B) du texte. """

		super().__init__(affichage, position, (1, 1), ancrage)

		self.texte = texte
		self.taille_police = taille_police
		self.couleur = couleur

		chemin_fichier_police = os.path.join(constantes.Chemin.RESSOURCES, constantes.General.POLICE)

		if os.path.exists(chemin_fichier_police):
			# si la police est présente dans le data du jeu, on l'utilise
			self.police = pygame.freetype.Font(chemin_fichier_police)
		else:
			# sinon on utilise la police par défaut du système
			nom_police = pygame.freetype.get_default_font()
			self.police = pygame.freetype.SysFont(nom_police, self.taille_police)

	def actualiser(self):
		""" Crée une surface à partir du texte défini puis la dessine sur l'affichage. """

		# on créer une surface à partir du texte donné, en utilisant la police définie
		surface, rect = self.police.render(self.texte, self.couleur, size=self.taille_police)
		
		# on redéfini la taille du widget, car sa taille dépend du texte donné
		# elle a donc peut être changé
		self.taille = (rect.width, rect.height)

		# on dessine la surface représentant le texte sur la fenêtre, 
		# à sa position réelle (coin supérieur gauche)
		self.affichage.fenetre.blit(surface, self.obtenir_position_reelle())


class Bouton(Widget):
	""" Permet de créer un bouton qui change de texture en fonction
		de la position et de l'état de la souris. Lance une fonction
		donnée lors du clic.	"""

	def __init__(self, affichage, action, texte="", arguments_action=(), position=(0, 0), taille=(1, 1), ancrage=(-1, -1), \
			taille_police=20, couleur_texte=(255, 255, 255)):
		""" Initialise un bouton. 

			<affichage> (affichage.Affichage): La fenêtre sur laquelle dessiner le bouton.
			<action> (function ou method): La fonction ou méthode à exécuter lors du clic sur ce bouton.
			[text] (str): Le texte à afficher.
			[position] (tuple): La position (x, y) du bouton en pixels.
			[taille] (tuple): La taille (largeur, hauteur) du bouton en pixels.
			[ancrage] (tuple): Le point (x, y) d'ancrage du bouton en pixels.
			[taille_police] (int): La hauteur de la police en pixels.
			[couleur_texte] (tuple): La couleur (R, V, B) du texte. """

		super().__init__(affichage, position, taille, ancrage)
		# on crée un widget Texte qui sera affiché sur le bouton (centré sur le bouton)
		self.texte = Texte(affichage, texte, position=self.obtenir_position_texte(), ancrage=(0, 0), \
			taille_police=taille_police, couleur=couleur_texte)
		# tuple contenant tous les arguments à passer à la fonction 'action'
		self.arguments_action = arguments_action
		# action est une fonction que l'on lancera lors du clic sur le bouton
		self.action = action
		# toutes les textures du boutons seront stockées dans cet attribut
		self.images = {}
		# l'état du bouton (entre 'normal', 'survol', 'clic_droit', 'clic_gauche', 'clic_central' et 'desactive')
		self.etat = "normal"
		# on charge toutes les images du bouton (normal, cliqué, désactivé, ...)
		self.charger_images()

	def charger_images(self):
		""" Charge les images de fond du bouton. """

		etats = ("clic_central", "clic_droit", "clic_gauche", "desactive", "normal", "survol")

		# pour chaque état que peut avoir le bouton, on charge une image
		# que l'on 'stocke' dans 'self.images'
		for etat in etats:
			chemin_image = os.path.join(constantes.Chemin.IMAGES, "bouton", "{etat}.png".format(etat=etat))
			image = self.affichage.obtenir_image(chemin_image)

			# il faut redimensionner l'image pour qu'elle fasse la taille du bouton
			self.images[etat] = pygame.transform.scale(image, self.taille)

	def actualiser(self):
		""" Redessine l'image de fond et le texte du bouton sur l'affichage. """

		# on dessine la texture correspondante à l'état actuelle du bouton sur la fenêtre
		# à la position du coin supérieur gauche
		self.affichage.fenetre.blit(self.images[self.etat], self.obtenir_position_reelle())
		# on actualise le texte sur le bouton
		self.texte.actualiser()

	def actualiser_evenement(self, evenement):
		""" Détecte le survol et le clic de la souris pour changer l'état du bouton et
			exécuter l'action définie.

			<evenement> (pygame.event.Event): L'évènement à tester. """

		x, y = self.obtenir_position_reelle()
		w, h = self.taille

		# si on repère le clic de la souris
		if evenement.type == pygame.MOUSEBUTTONDOWN:
			# si le clic de la souris est faite sur le widget (et pas en dehors)
			if self.est_dans_widget(evenement.pos):
				# en fonction du bouton cliqué, on change l'état du bouton
				if evenement.button == 1:
					self.etat = "clic_gauche"
				elif evenement.button == 2:
					self.etat = "clic_central"
				elif evenement.button == 3:
					self.etat = "clic_droit"

		# si le bouton de la souris se relève
		elif evenement.type == pygame.MOUSEBUTTONUP:
			# si la souris se trouve sur le bouton, on le met en état de 'survol'
			if self.est_dans_widget(evenement.pos):
				# si le bouton relaché est le clic gauche, on execute l'action associée au bouton
				if evenement.button == 1:
					self.action(*self.arguments_action)
				
				self.etat = "survol"
			else:
				# sinon, on le remet dans l'état 'normal'
				self.etat = "normal"

		# si la souris se déplace, on regarde si elle survole le bouton
		elif evenement.type == pygame.MOUSEMOTION:
			# si la souris se trouve sur le bouton, on le met en état de 'survol'
			if self.est_dans_widget(evenement.pos):
				self.etat = "survol"
			else:
				# sinon, on le remet dans l'état 'normal'
				self.etat = "normal"

	def obtenir_position_texte(self):
		""" Renvoie la position du texte en fonction de celle du bouton. """

		x, y = self.obtenir_position_reelle()
		w, h = self.taille

		return (x + w//2, y + h//2)


class Image(Widget):
	""" Permet de créer une image qui se redéssine seule à une position définie lors de sa création.
		L'image est chargée automatiquement par le widget lors de sa création. """

	def __init__(self, affichage, chemin_image, position=(0, 0), taille=(0, 0), ancrage=(-1, -1)):
		""" Initialise une image. 

			<affichage> (affichage.Affichage): La fenêtre sur laquelle dessiner l'image.
			<chemin_image> (str): Le chemin de l'image à afficher.
			[position] (tuple): La position (x, y) de l'image en pixels.
			[taille] (tuple): La taille (largeur, hauteur) de l'image en pixels.
			[ancrage] (tuple): Le point (x, y) d'ancrage de l'image en pixels. """

		super().__init__(affichage, position, taille, ancrage)

		self.chemin_image = chemin_image
		self.charger_image()

	def charger_image(self):
		""" Charge l'image à afficher. """

		# on charge l'image demandée
		self.image = self.affichage.obtenir_image(self.chemin_image)

		# si la taille définie est différente de 0x0 pixels:
		if self.taille != (0, 0):
			# on la redimensionne à la taille voulue
			self.image = pygame.transform.scale(self.image, self.taille)
		else:
			# sinon on change l'attribut taille pour qu'il corresponde à la taille de l'image chargée
			self.taille = self.image.get_size()

	def actualiser(self):
		""" Redessine l'image sur l'affichage. """

		# on colle l'image sur la fenêtre à la position du coin supérieur gauche
		self.affichage.fenetre.blit(self.image, self.obtenir_position_reelle())