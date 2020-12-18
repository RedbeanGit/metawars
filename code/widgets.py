# -*- coding: utf-8 -*-

#	This file is part of Metawars.
#
#	Metawars is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	Metawars is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with Metawars. If not, see <https://www.gnu.org/licenses/>

"""
	Propose des classes permettant la création de widgets.
	Un widget est un élément graphique indépendant et autonome tel qu'un
	bouton, une zone de texte ou une image.
"""

import constantes

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"

import math
import pygame
import pygame.freetype
import time

from os import path as op

pygame.freetype.init()


class Widget(object):
	""" Classe de base pour tous les widgets (éléments graphiques
		indépendants). """

	def __init__(self, affichage, position=(0, 0), taille=(1, 1), \
		ancrage=(-1, -1)):
		""" Initialise un widget. 

			<affichage> (affichage.Affichage): La fenêtre sur laquelle
				dessiner le widget.
			[position] (tuple): La position (x, y) du widget en pixel.
			[taille] (tuple): La taille (largeur, hauteur) du widget en 
				pixel.
			[ancrage] (tuple): Le point (x, y) d'ancrage du widget en pixel. """

		self.affichage = affichage
		self.position = position
		self.taille = taille
		# son point d'ancrage, définit comment placer le widget par rapport à
		# sa position:
		# (-1, -1) signifie "en haut à gauche" et (1, 1) "en bas à droite"
		# (0, 0) signifie donc "centré"
		self.ancrage = ancrage
		self.expire = False

	def actualiser(self):
		""" Cette méthode est appelée à chaque frame de jeu pour redessiner le
			widget sur l'affichage. Ne fait rien par défaut. """

		pass

	def actualiser_evenement(self, evenement):
		""" Cette méthode est appelée pour chaque nouvel évenement (clic,
			appui sur une touche, ...). Ne fait rien par défaut.

			<evenement> (pygame.event.Event): L'évènement déclencheur. """

		pass

	def obtenir_position_reelle(self):
		""" Renvoie la position du coin supérieur gauche du widget
			en fonction de ses attributs 'position' et 'ancrage'. """

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

	def __init__(self, affichage, texte, taille_police=20, \
		couleur=(255, 255, 255), **kwargs):
		""" Initialise un texte. 

			<affichage> (affichage.Affichage): La fenêtre sur laquelle
				dessiner le texte.
			<text> (str): Le texte à afficher.
			[taille_police] (int): La hauteur de la police en pixel.
			[couleur] (tuple): La couleur (R, V, B) du texte.
			[**kwargs] (object): Les attributs hérités de Widget. """

		kwargs["taille"] = (1, 1)
		super().__init__(affichage, **kwargs)

		self.texte = texte
		self.taille_police = taille_police
		self.couleur = couleur

		dossier_police = constantes.Chemin.RESSOURCES
		nom_police = constantes.General.POLICE
		chemin_fichier_police = op.join(dossier_police, nom_police)

		if op.exists(chemin_fichier_police):
			self.police = pygame.freetype.Font(chemin_fichier_police)
		else:
			nom_police = pygame.freetype.get_default_font()
			self.police = pygame.freetype.SysFont(nom_police, \
				self.taille_police)

	def obtenir_surface(self):
		""" Crée une surface à partir du texte défini puis la retourne avec un
			pygame.Rect associé. """

		return self.police.render(self.texte, self.couleur, \
			size=self.taille_police)

	def actualiser(self):
		""" Redessine sur l'affichage une surface à partir du texte défini. """

		surface, rect = self.obtenir_surface()
		self.taille = (rect.width, rect.height)
		self.affichage.fenetre.blit(surface, self.obtenir_position_reelle())


class Bouton(Widget):
	""" Permet de créer un bouton qui change de texture en fonction
		de la position et de l'état de la souris. Lance une fonction
		donnée lors du clic. """

	def __init__(self, affichage, action, texte="", arguments_action=(), \
		taille_police=20, couleur_texte=(255, 255, 255), **kwargs):
		""" Initialise un bouton. 

			<affichage> (affichage.Affichage): La fenêtre sur laquelle
				dessiner le bouton.
			<action> (function ou method): La fonction ou méthode à	exécuter
				lors du clic sur ce bouton.
			[text] (str): Le texte à afficher.
			[taille_police] (int): La hauteur de la police en pixel.
			[couleur_texte] (tuple): La couleur (R, V, B) du texte.
			[**kwargs] (object): Les attributs hérités de Widget. """

		super().__init__(affichage, **kwargs)
		
		position_text = self.obtenir_position_texte()
		self.texte = Texte(affichage, texte, position=position_text, \
			ancrage=(0, 0), taille_police=taille_police, \
			couleur=couleur_texte)

		self.arguments_action = arguments_action
		self.action = action
		self.images = {}
		self.etat = "normal"

		self.charger_images()

	def charger_images(self):
		""" Charge les images de fond du bouton. """

		etats = ("clic_central", "clic_droit", "clic_gauche", "desactive", \
			"normal", "survol")

		for etat in etats:
			chemin_image = op.join(constantes.Chemin.IMAGES, "bouton", \
				"{etat}.png".format(etat=etat))
			image = self.affichage.obtenir_image(chemin_image)
			self.images[etat] = pygame.transform.scale(image, self.taille)

	def actualiser(self):
		""" Redessine l'image de fond et le texte du bouton sur l'affichage. """

		self.affichage.fenetre.blit(self.images[self.etat], \
			self.obtenir_position_reelle())
		self.texte.actualiser()

	def actualiser_evenement(self, evenement):
		""" Détecte le survol et le clic de la souris pour changer l'état du
			bouton et exécuter l'action définie.

			<evenement> (pygame.event.Event): L'évènement à tester. """

		if evenement.type == pygame.MOUSEBUTTONDOWN:
			if self.est_dans_widget(evenement.pos):
				if evenement.button == 1:
					self.etat = "clic_gauche"
				elif evenement.button == 2:
					self.etat = "clic_central"
				elif evenement.button == 3:
					self.etat = "clic_droit"

		elif evenement.type == pygame.MOUSEBUTTONUP:
			if self.est_dans_widget(evenement.pos):
				if evenement.button == 1:
					self.action(*self.arguments_action)
				
				self.etat = "survol"
			else:
				self.etat = "normal"

		elif evenement.type == pygame.MOUSEMOTION:
			if self.est_dans_widget(evenement.pos):
				self.etat = "survol"
			else:
				self.etat = "normal"

	def obtenir_position_texte(self):
		""" Renvoie la position du texte en fonction de celle du bouton. """

		x, y = self.obtenir_position_reelle()
		w, h = self.taille

		return (x + w//2, y + h//2)


class Image(Widget):
	""" Permet de créer une image qui se redéssine seule à une position
		définie lors de sa création. L'image est chargée automatiquement par
		le widget lors de sa création. """

	def __init__(self, affichage, chemin_image, **kwargs):
		""" Initialise une image. 

			<affichage> (affichage.Affichage): La fenêtre sur laquelle
				dessiner l'image.
			<chemin_image> (str): Le chemin de l'image à afficher.
			[**kwargs] (object): Les attributs hérités de Widget. """

		super().__init__(affichage, **kwargs)

		self.chemin_image = chemin_image
		self.charger_image()

	def charger_image(self):
		""" Charge l'image à afficher. """

		self.image = self.affichage.obtenir_image(self.chemin_image)

		if self.taille != (0, 0):
			self.image = pygame.transform.scale(self.image, self.taille)
		else:
			self.taille = self.image.get_size()

	def actualiser(self):
		""" Redessine l'image sur l'affichage. """

		self.affichage.fenetre.blit(self.image, \
			self.obtenir_position_reelle())


class TexteEditable(Texte):
	""" Cette classe définit un texte éditable avec le clavier et la souris. """

	def __init__(self, affichage, texte, couleur_curseur=(0, 0, 0), \
		largeur_min=0, **kwargs):
		""" Initialise un texte éditable.
		
			<affichage> (affichage.Affichage): La fenêtre sur laquelle 
				dessiner l'image.
			<text> (str): Le texte à afficher
			[couleur_curseur] (tuple): La couleur (R, V, B) du curseur en mode
				édition. (0, 0, 0) par défaut.
			[largeur_min] (int): La largeur minimale en pixel de la zone
				cliquable du widget. 0 par défaut.
			[**kwargs] (object): Les attributs hérités de Texte. """

		super().__init__(affichage, texte, **kwargs)

		self.couleur_curseur = couleur_curseur
		self.largeur_min = largeur_min
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
		""" Crée une surface à partir du texte défini puis la retourne avec un
			pygame.Rect associé. """

		return self.police.render(self.texte, self.couleurs[self.etat], \
			size=self.taille_police)

	def actualiser(self):
		""" Redessine le texte sur l'affichage et un curseur en mode édition. """

		super().actualiser()

		if self.en_edition:
			l, h = self.taille
			x, y = self.obtenir_position_reelle()

			if self.texte:
				cx = int(x + self.position_curseur * l / len(self.texte))
			else:
				cx = x
			cy = y

			l = max(l, self.largeur_min)
			self.taille = (l, h)

			pygame.draw.line(self.affichage.fenetre, self.couleur_curseur, \
				(cx, cy), (cx, cy + h), 2)
			pygame.draw.line(self.affichage.fenetre, self.couleur_curseur, \
				(x, cy + h + 2), (x + l, cy + h + 2), 2)

	def actualiser_evenement(self, evenement):
		""" Détecte le survol et le clic de la souris pour changer l'état du 
			texte et active ou désactive le mode édition lors du clic.

			<evenement> (pygame.event.Event): L'évènement à tester. """

		x, y = self.obtenir_position_reelle()
		w, h = self.taille

		if evenement.type == pygame.MOUSEBUTTONDOWN:
			if self.est_dans_widget(evenement.pos):
				if evenement.button == 1:
					self.etat = "clic_gauche"
					self.en_edition = True
					self.position_curseur = int((evenement.pos[0] - x) / w * len(self.texte))
				elif evenement.button == 2:
					self.etat = "clic_central"
				elif evenement.button == 3:
					self.etat = "clic_droit"
			elif evenement.button == 1:
				self.en_edition = False

		elif evenement.type == pygame.MOUSEMOTION:
			if self.est_dans_widget(evenement.pos):
				self.etat = "survol"
			else:
				self.etat = "normal"

		elif evenement.type == pygame.KEYDOWN:
			if self.en_edition:
				if evenement.key == pygame.K_RETURN:
					self.en_edition = False
				
				elif evenement.key == pygame.K_BACKSPACE:
					if self.position_curseur:
						self.texte = self.texte[:self.position_curseur-1] \
							+ self.texte[self.position_curseur:]
						self.position_curseur -= 1
				
				elif evenement.key == pygame.K_DELETE:
					self.texte = self.texte[:self.position_curseur] \
					+ self.texte[self.position_curseur+1:]
				
				elif evenement.key == pygame.K_UP:
					self.position_curseur = 0
				
				elif evenement.key == pygame.K_DOWN:
					self.position_curseur = len(self.texte)
				
				elif evenement.key == pygame.K_LEFT:
					if self.position_curseur:
						self.position_curseur -= 1
				
				elif evenement.key == pygame.K_RIGHT:
					if self.position_curseur < len(self.texte):
						self.position_curseur += 1
				
				else:
					self.texte = self.texte[:self.position_curseur] \
						+ evenement.unicode \
						+ self.texte[self.position_curseur:]
					self.position_curseur += 1


class TexteTemporaire(Texte):
	""" Cette classe définit un texte qui disparait progressivement. Au bout
		d'une certaine durée, il expire et est alors supprimé de l'affichage. """

	def __init__(self, affichage, texte, duree, **kwargs):
		""" Initialise un TexteTemporaire avec une durée de vie donnée.

			<affichage> (affichage.Affichage): La fenêtre sur laquelle
				dessiner l'image.
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
		""" Crée une surface à partir du texte défini puis la retourne avec un
			pygame.Rect associé. """

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

		return self.police.render(self.texte, (r, g, b, a), \
			size=self.taille_police)
	
	def actualiser(self):
		""" Redessine le texte sur l'affichage et met à jour son état en
			fonction du temps écoulé. """
		
		temps_actuel = time.time()

		if temps_actuel - self.depart >= self.duree:
			self.expire = True

		super().actualiser()