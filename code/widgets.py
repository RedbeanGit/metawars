# -*- coding: utf-8 -*-

import constantes

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"

import os
import math
import pygame
import pygame.freetype
import time

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
		# si expire vaut True, alors le widget sera supprimé de l'affichage
		self.expire = False

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

	def __init__(self, affichage, texte, taille_police=20, couleur=(255, 255, 255), **kwargs):
		""" Initialise un texte. 

			<affichage> (affichage.Affichage): La fenêtre sur laquelle dessiner le texte.
			<text> (str): Le texte à afficher.
			[taille_police] (int): La hauteur de la police en pixels.
			[couleur] (tuple): La couleur (R, V, B) du texte.
			[**kwargs] (object): Les attributs hérités de Widget. """

		kwargs["taille"] = (1, 1)
		super().__init__(affichage, **kwargs)

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
		
		rect = self.obtenir_surface()[1]
		self.taille = (rect.width, rect.height)

	def obtenir_surface(self):
		""" Crée une surface à partir du texte défini puis la retourne avec un pygame.Rect associé. """

		return self.police.render(self.texte, self.couleur, size=self.taille_police)

	def actualiser(self):
		""" Redessine sur l'affichage une surface à partir du texte défini. """

		# on créer une surface à partir du texte donné, en utilisant la police définie
		surface, rect = self.obtenir_surface()
		
		# on redéfini la taille du widget, car sa taille dépend du texte donné
		# elle a donc peut être changé
		self.taille = (rect.width, rect.height)

		# on dessine la surface représentant le texte sur la fenêtre, 
		# à sa position réelle (coin supérieur gauche)
		self.affichage.fenetre.blit(surface, self.obtenir_position_reelle())


class Bouton(Widget):
	""" Permet de créer un bouton qui change de texture en fonction
		de la position et de l'état de la souris. Lance une fonction
		donnée lors du clic. """

	def __init__(self, affichage, action, texte="", arguments_action=(), taille_police=20, couleur_texte=(255, 255, 255), **kwargs):
		""" Initialise un bouton. 

			<affichage> (affichage.Affichage): La fenêtre sur laquelle dessiner le bouton.
			<action> (function ou method): La fonction ou méthode à exécuter lors du clic sur ce bouton.
			[text] (str): Le texte à afficher.
			[taille_police] (int): La hauteur de la police en pixels.
			[couleur_texte] (tuple): La couleur (R, V, B) du texte.
			[**kwargs] (object): Les attributs hérités de Widget. """

		super().__init__(affichage, **kwargs)
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

	def __init__(self, affichage, chemin_image, **kwargs):
		""" Initialise une image. 

			<affichage> (affichage.Affichage): La fenêtre sur laquelle dessiner l'image.
			<chemin_image> (str): Le chemin de l'image à afficher.
			[**kwargs] (object): Les attributs hérités de Widget. """

		super().__init__(affichage, **kwargs)

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


class TexteEditable(Texte):
	""" Cette classe définit un texte éditable avec le clavier et la souris. """

	def __init__(self, affichage, texte, couleur_curseur=(0, 0, 0), **kwargs):
		""" Initialise un texte éditable.
		
			<affichage> (affichage.Affichage): La fenêtre sur laquelle dessiner l'image.
			<text> (str): Le texte à afficher.
			[**kwargs] (object): Les attributs hérités de Texte. """

		super().__init__(affichage, texte, **kwargs)

		self.couleur_curseur = couleur_curseur
		self.en_edition = False
		self.couleurs = {}
		self.etat = "normal"
		self.position_curseur = len(self.texte)

		self.charger_couleurs()

	def charger_couleurs(self):
		""" Charge les différentes couleurs du texte. """

		if isinstance(self.couleur, str):
			r, v, b = pygame.color.THECOLORS.get(self.color, (0, 0, 0))
		elif len(self.couleur) == 3:
			r, v, b = self.couleur
		elif len(self.couleur) == 4:
			r, v, b, a = self.couleur

		self.couleurs = {
			"clic_central": (max(r-5, 0), max(v-5, 0), max(b-5, 0)),
			"clic_droit": (min(r+5, 255), min(v+5, 255), min(b+5, 255)),
			"clic_gauche": (max(r-10, 0), max(v-10, 0), max(b-10, 0)),
			"desactive": (max(r-20, 0), max(v-20, 0), max(b-20, 0)),
			"normal": (r, v, b),
			"survol": (min(r+10, 255), min(v+10, 255), min(b+10, 255))
		}

	def obtenir_surface(self):
		""" Crée une surface à partir du texte défini puis la retourne avec un pygame.Rect associé. """

		return self.police.render(self.texte, self.couleurs[self.etat], size=self.taille_police)

	def actualiser(self):
		""" Redessine le texte sur l'affichage et un curseur en mode édition. """

		super().actualiser()

		if self.en_edition:
			x, y = self.obtenir_position_reelle()
			w, h = self.taille

			cx = int(x + self.position_curseur * w / len(self.texte))
			cy = y
			pygame.draw.line(self.affichage.fenetre, self.couleur_curseur, (cx, cy), (cx, cy + h), width=2)

	def actualiser_evenement(self, evenement):
		""" Détecte le survol et le clic de la souris pour changer l'état du texte et
			active ou désactive le mode édition lors du clic.

			<evenement> (pygame.event.Event): L'évènement à tester. """

		x, y = self.obtenir_position_reelle()
		w, h = self.taille

		# si on repère le clic de la souris
		if evenement.type == pygame.MOUSEBUTTONDOWN:
			# si le clic de la souris est faite sur le widget (et pas en dehors)
			if self.est_dans_widget(evenement.pos):
				# en fonction du bouton cliqué, on change l'état du texte
				if evenement.button == 1:
					self.etat = "clic_gauche"
					self.en_edition = True
					self.position_curseur = int((evenement.pos[0] - x) / w * len(self.texte))
				elif evenement.button == 2:
					self.etat = "clic_central"
				elif evenement.button == 3:
					self.etat = "clic_droit"
			# si on clique en dehors du texte, on arrête le mode édition
			elif evenement.button == 1:
				self.en_edition = False

		# si la souris se déplace, on regarde si elle survole le texte
		elif evenement.type == pygame.MOUSEMOTION:
			# si la souris se trouve sur le texte, on le met en état de 'survol'
			if self.est_dans_widget(evenement.pos):
				self.etat = "survol"
			else:
				# sinon, on le remet dans l'état 'normal'
				self.etat = "normal"

		elif evenement.type == pygame.KEYDOWN:
			if self.en_edition:
				if evenement.key == pygame.K_RETURN:
					self.en_edition = False
				elif evenement.key == pygame.K_BACKSPACE:
					self.texte = self.texte[:self.position_curseur] + self.texte[self.position_curseur:]
				elif evenement.key == pygame.K_DELETE:
					self.texte = self.texte[:self.position_curseur+1] + self.texte[self.position_curseur+1:]
				else:
					self.texte += evenement.unicode


class TexteTemporaire(Texte):
	""" Cette classe définit un texte qui disparait progressivement. Au bout d'une certaine durée, il expire
		et est alors supprimé de l'affichage. """

	def __init__(self, affichage, texte, duree, **kwargs):
		""" Initialise un TexteTemporaire avec une durée de vie donnée.

			<affichage> (affichage.Affichage): La fenêtre sur laquelle dessiner l'image.
			<text> (str): Le texte à afficher.
			<duree> (float): La durée de vie du texte.
			[**kwargs] (object): Les attributs hérités de Texte. """

		self.duree = duree
		self.depart = time.time()

		super().__init__(affichage, texte, **kwargs)

	def redemarrer(self):
		""" Remet à zéro le widget. """

		self.expire = False
		self.depart = time.time()

	def obtenir_surface(self):
		""" Crée une surface à partir du texte défini puis la retourne avec un pygame.Rect associé. """

		if isinstance(self.couleur, str):
			r, g, b = pygame.color.THECOLORS
		elif len(self.couleur) == 3:
			r, g, b = self.couleur
		elif len(self.couleur) == 4:
			r, g, b, a = self.couleur

		a = 255 - int((time.time() - self.depart) / self.duree * 255)

		if a > 255:
			a = 255
		elif a < 0:
			a = 0

		return self.police.render(self.texte, (r, g, b, a), size=self.taille_police)
	
	def actualiser(self):
		""" Redessine le texte sur l'affichage et met à jour son état en fonction du temps écoulé. """
		
		temps_actuel = time.time()

		if temps_actuel - self.depart >= self.duree:
			self.expire = True

		super().actualiser()