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
	Contient une classe permettant de créer une fenêtre et de gérer les
	images.
"""

import math
import os
import sys
import pygame

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"

import constantes
import utile
import niveau
from widgets import Texte, Bouton, Image, TexteTemporaire, TexteEditable


class Affichage(object):
	""" Permet de créer une fenêtre, charger des images et gérer des 
		Widgets. """

	def __init__(self):
		""" Initialise un nouvel affichage. """

		taille_ecran = constantes.General.TAILLE_ECRAN
		self.fenetre = pygame.display.set_mode(taille_ecran)
		self.images = {}
		self.widgets = []

		pygame.display.set_caption(constantes.General.NOM)
		icone = pygame.image.load(constantes.General.IMAGE_ICONE)
		pygame.display.set_icon(icone)

	def charger_images(self):
		""" Charge les images du disque dur en mémoire vive. Il est
			préférable de n'appeler cette méthode qu'une seule fois
			pour éviter de ralentir le jeu. """

		utile.debogguer("Chargement des images...")

		# Pour chaque image dans constantes.IMAGES
		for chemin_image in constantes.Ressources.IMAGES:
			chemin_image = os.path.join(constantes.Chemin.IMAGES, 
				*chemin_image)

			try:
				self.images[chemin_image] = pygame.image.load(chemin_image)
				utile.debogguer("L'image '" + chemin_image \
					+ "' a été chargé !")
			except pygame.error:
				utile.debogguer("L'image '" + chemin_image \
					+ "' n'existe pas !", 1)
		
		utile.debogguer("Fin du chargement des images !")

	def obtenir_image(self, chemin_image):
		""" Renvoie une surface pygame à un emplacement défini. Si
			l'image n'a pas été chargée, crée une nouvelle surface
			noire.

			<chemin_image> (str): L'emplacement de l'image. """

		if chemin_image in self.images:
			# si l'image existe, on la renvoie
			return self.images[chemin_image].convert_alpha()
		else:
			# sinon, on renvoie une surface noire de 50x50 pixels
			return pygame.Surface((50, 50))

	def afficher_message(self, message, couleur=(255, 255, 255)):
		""" Affiche un message temporaire en bas de l'écran.

			<message> (str): Le message à afficher.
			[couleur] (tuple): La couleur du texte sour la forme (R, V,
			B). (0, 0, 0) par défaut. """

		l, h = self.obtenir_taille()
		self.widgets.append(TexteTemporaire(self, message, 2, \
			position=(l // 2, int(h * 0.77)), ancrage=(0, 0), \
			couleur=couleur))

	def supprimer_widgets(self):
		""" Supprime tous les widgets de cet affichage en vidant la 
			liste des widgets. """

		self.widgets.clear()

	def creer_widgets_partie(self):
		""" Crée les textes à afficher pendant la partie renseignant 
			sur le temps écoulé, les pièces amassées, la vie restante, 
			les dégats et vitesse bonus. """

		coord_droite = self.obtenir_taille()[0] - 10

		texte_temps = Texte(self, "Temps: 0s", position=(10, 10))
		texte_pieces = Texte(self, "Pièces: 0", position=(10, 40))
		texte_vie = Texte(self, "Vie: 0", position=(10, 70))

		texte_arme = Texte(self, "Bonus dégats: 0", \
			position=(coord_droite,	10), ancrage=(1, -1))
		texte_vitesse = Texte(self, "Bonus vitesse: x1", \
			position=(coord_droite, 40), ancrage=(1, -1))
		
		self.widgets.append(texte_temps)
		self.widgets.append(texte_pieces)
		self.widgets.append(texte_vie)

		self.widgets.append(texte_arme)
		self.widgets.append(texte_vitesse)

	def creer_widgets_menu(self, jeu):
		""" Crée un bouton 'Jouer', un bouton 'Quitter', une image de 
			titre et des textes informatifs.

			<jeu> (jeu.Jeu): Le jeu à appeler lors du clic sur un bouton. """

		def jouer():
			jeu.initialiser_partie()
			jeu.lancer_boucle()

		def multijoueur():
			jeu.initialiser_menu_multijoueur()
			jeu.lancer_boucle()

		def quitter():
			jeu.arreter()

		l, h = self.obtenir_taille()
		milieu_ecran_x = l // 2
		milieu_ecran_y = h // 2
		milieu_du_milieu_ecran_y = milieu_ecran_y // 2

		bouton_jouer = Bouton(self, jouer, texte="Jouer en solo", \
			position=(milieu_ecran_x, milieu_ecran_y), taille=(300, 50), \
			ancrage=(0, 0), taille_police=20)
		bouton_multi = Bouton(self, multijoueur, texte="Multijoueur", \
			position=(milieu_ecran_x, milieu_ecran_y+80), taille=(300, 50), \
			ancrage=(0, 0), taille_police=20)
		bouton_quitter = Bouton(self, quitter, texte="Quitter", \
			position=(milieu_ecran_x, milieu_ecran_y+160), taille=(300, 50), \
			ancrage=(0, 0), taille_police=20)
		logo = Image(self, constantes.General.IMAGE_TITRE, \
			position=(milieu_ecran_x, milieu_du_milieu_ecran_y), \
			taille=(400, 80), ancrage=(0, 0))
		texte_version = Texte(self, "v" + constantes.General.VERSION, \
			position=(10, h - 10), ancrage=(-1, 1), taille_police=16)
		texte_dev = Texte(self, __author__, position=(l - 10, h - 10), \
			ancrage=(1, 1), taille_police=16)

		self.widgets.append(bouton_jouer)
		self.widgets.append(bouton_multi)
		self.widgets.append(bouton_quitter)
		self.widgets.append(logo)
		self.widgets.append(texte_version)
		self.widgets.append(texte_dev)

	def creer_widgets_multijoueur(self, jeu):
		""" Crée un bouton 'Héberger', 'Rejoindre' et 'Retour' ainsi qu'un
			titre pour afficher un menu multijoueur.

			<jeu> (jeu.Jeu): Le jeu à appeler lors du clic sur un bouton. """

		def heberger():
			jeu.initialiser_menu_heberger()
			jeu.lancer_boucle()

		def rejoindre():
			jeu.initialiser_menu_rejoindre()
			jeu.lancer_boucle()

		def retour():
			jeu.arreter_boucle()
			jeu.initialiser_menu_principal()

		l, h = self.obtenir_taille()
		milieu_ecran_x = l // 2
		milieu_ecran_y = h // 2
		milieu_du_milieu_ecran_y = milieu_ecran_y // 2

		logo = Image(self, constantes.General.IMAGE_TITRE, \
			position=(milieu_ecran_x, milieu_du_milieu_ecran_y), \
			taille=(400, 80), ancrage=(0, 0))
		texte_titre = Texte(self, "Multijoueur", \
			position=(milieu_ecran_x, int(h * 0.4)), ancrage=(0, 0), \
			taille_police=22)
		bouton_heberger = Bouton(self, heberger, texte="Héberger", \
			position=(milieu_ecran_x, milieu_ecran_y), taille=(300, 50), \
			ancrage=(0, 0), taille_police=20)
		bouton_rejoindre = Bouton(self, rejoindre, texte="Rejoindre", \
			position=(milieu_ecran_x, milieu_ecran_y+80), taille=(300, 50), \
			ancrage=(0, 0), taille_police=20)
		bouton_retour = Bouton(self, retour, texte="Retour", \
			position=(milieu_ecran_x, milieu_ecran_y+160), taille=(300, 50), \
			ancrage=(0, 0), taille_police=20)

		self.widgets.append(logo)
		self.widgets.append(texte_titre)
		self.widgets.append(bouton_heberger)
		self.widgets.append(bouton_rejoindre)
		self.widgets.append(bouton_retour)

	def creer_widgets_heberger(self, jeu):
		""" Crée une entrée 'Port' ainsi qu'un titre pour afficher un menu de 
			configuration d'une partie hébergée (serveur).

			<jeu> (jeu.Jeu): Le jeu à appeler lors du clic sur un bouton. """

		def confirmer():
			if edittexte_port.texte.isdigit() \
			and "." not in edittexte_port.texte:
				jeu.initialiser_partie_serveur(int(edittexte_port.texte))
				jeu.lancer_boucle()
			else:
				self.afficher_message("Port invalide")

		def retour():
			jeu.arreter_boucle()
			jeu.initialiser_menu_multijoueur()

		l, h = self.obtenir_taille()
		milieu_ecran_x = l // 2
		milieu_ecran_y = h // 2
		milieu_du_milieu_ecran_y = milieu_ecran_y // 2

		logo = Image(self, constantes.General.IMAGE_TITRE, \
			position=(milieu_ecran_x, milieu_du_milieu_ecran_y), \
			taille=(400, 80), ancrage=(0, 0))
		texte_titre = Texte(self, "Héberger", \
			position=(milieu_ecran_x, int(h * 0.4)), ancrage=(0, 0), \
			taille_police=22)
		texte_port = Texte(self, "Port", \
			position=(milieu_ecran_x - 20, milieu_ecran_y), ancrage=(1, 0), \
			taille_police=20)
		edittexte_port = TexteEditable(self, "20092", \
			position=(milieu_ecran_x + 20, milieu_ecran_y), ancrage=(-1, 0), \
			taille_police=20, couleur_curseur=(255, 255, 255), largeur_min=50)
		bouton_retour = Bouton(self, retour, texte="Retour", \
			position=(milieu_ecran_x-10, milieu_ecran_y+160), \
			taille=(140, 50), ancrage=(1, 0), taille_police=20)
		bouton_confirmer = Bouton(self, confirmer, texte="Se connecter", \
			position=(milieu_ecran_x+10, milieu_ecran_y+160), \
			taille=(140, 50), ancrage=(-1, 0), taille_police=20)

		self.widgets.append(logo)
		self.widgets.append(texte_titre)
		self.widgets.append(texte_port)
		self.widgets.append(edittexte_port)
		self.widgets.append(bouton_retour)
		self.widgets.append(bouton_confirmer)

	def creer_widgets_rejoindre(self, jeu):
		""" Crée une entrée 'Adresse' et 'Port' ainsi qu'un titre pour
			afficher un menu de configuration d'une partie en tant que client.

			<jeu> (jeu.Jeu): Le jeu à appeler lors du clic sur un bouton. """

		def confirmer():
			if edittexte_port.texte.isdigit() \
			and "." not in edittexte_port.texte:
				jeu.initialiser_partie_client(edittexte_adresse.texte, \
					int(edittexte_port.texte))
				jeu.lancer_boucle()
			else:
				self.afficher_message("Port invalide")

		def retour():
			jeu.arreter_boucle()
			jeu.initialiser_menu_multijoueur()

		l, h = self.obtenir_taille()
		milieu_ecran_x = l // 2
		milieu_ecran_y = h // 2
		milieu_du_milieu_ecran_y = milieu_ecran_y // 2

		logo = Image(self, constantes.General.IMAGE_TITRE, \
			position=(milieu_ecran_x, milieu_du_milieu_ecran_y), \
			taille=(400, 80), ancrage=(0, 0))
		texte_titre = Texte(self, "Rejoindre", \
			position=(milieu_ecran_x, int(h * 0.4)), ancrage=(0, 0), \
			taille_police=22)
		texte_adresse = Texte(self, "Adresse", \
			position=(milieu_ecran_x-20, milieu_ecran_y), ancrage=(1, 0), \
			taille_police=20)
		edittexte_adresse = TexteEditable(self, "localhost", \
			position=(milieu_ecran_x+20, milieu_ecran_y), \
			ancrage=(-1, 0), taille_police=20, \
			couleur_curseur=(255, 255, 255), largeur_min=50)
		texte_port = Texte(self, "Port", \
			position=(milieu_ecran_x-20, milieu_ecran_y+40), ancrage=(1, 0), \
			taille_police=20)
		edittexte_port = TexteEditable(self, "20092", \
			position=(milieu_ecran_x + 20, milieu_ecran_y+40), \
			ancrage=(-1, 0), taille_police=20, \
			couleur_curseur=(255, 255, 255), largeur_min=50)
		bouton_retour = Bouton(self, retour, texte="Retour", \
			position=(milieu_ecran_x-10, milieu_ecran_y+160), \
			taille=(140, 50), ancrage=(1, 0), taille_police=20)
		bouton_confirmer = Bouton(self, confirmer, texte="Se connecter", \
			position=(milieu_ecran_x+10, milieu_ecran_y+160), \
			taille=(140, 50), ancrage=(-1, 0), taille_police=20)

		self.widgets.append(logo)
		self.widgets.append(texte_titre)
		self.widgets.append(texte_adresse)
		self.widgets.append(edittexte_adresse)
		self.widgets.append(texte_port)
		self.widgets.append(edittexte_port)
		self.widgets.append(bouton_retour)
		self.widgets.append(bouton_confirmer)

	def creer_widgets_pause(self, jeu):
		""" Crée un bouton 'Continuer' et 'Retour au menu principal' ainsi
			qu'un titre pour afficher un menu de pause.

			<jeu> (jeu.Jeu): Le jeu à appeler lors du clic sur un bouton. """

		def continuer():
			jeu.geler_partie(False)

		def retour():
			jeu.arreter_partie()
			jeu.arreter_boucle()
			jeu.initialiser_menu_principal()

		l, h = self.obtenir_taille()
		milieu_ecran_x = l // 2
		milieu_ecran_y = h // 2
		milieu_du_milieu_ecran_y = milieu_ecran_y // 2

		logo_pause = Image(self, constantes.General.IMAGE_TITRE, \
			position=(milieu_ecran_x, milieu_du_milieu_ecran_y), \
			taille=(400, 80), ancrage=(0, 0))
		texte_pause = Texte(self, "Pause", \
			position=(milieu_ecran_x, int(h * 0.4)), ancrage=(0, 0), \
			taille_police=22)
		bouton_continuer = Bouton(self, continuer, texte="Continuer", \
			position=(milieu_ecran_x, milieu_ecran_y), \
			taille=(300, 50), ancrage=(0, 0), taille_police=20)
		bouton_menu = Bouton(self, retour, texte="Retour au menu principal", \
			position=(milieu_ecran_x, milieu_ecran_y+80), \
			taille=(300, 50), ancrage=(0, 0), taille_police=20)

		self.widgets.append(bouton_continuer)
		self.widgets.append(bouton_menu)
		self.widgets.append(logo_pause)
		self.widgets.append(texte_pause)

	def creer_widgets_fin(self, jeu):
		""" Crée un texte de résumé des scores, un bouton 'Retour au menu
			principal' et un titre pour afficher un menu de fin (Game Over).

			<jeu> (jeu.Jeu): Le jeu à appeler lors du clic sur un bouton. """

		def retour():
			jeu.arreter_partie()
			jeu.arreter_boucle()
			jeu.initialiser_menu_principal()

		l, h = self.obtenir_taille()
		milieu_ecran_x = l // 2
		milieu_ecran_y = h // 2
		milieu_du_milieu_ecran_y = milieu_ecran_y // 2

		logo_fin = Image(self, constantes.General.IMAGE_TITRE, \
			position=(milieu_ecran_x, milieu_du_milieu_ecran_y), \
			taille=(400, 80), ancrage=(0, 0))
		titre_fin = Texte(self, "Partie terminée", \
			position=(milieu_ecran_x, int(h * 0.4)), ancrage=(0, 0), \
			taille_police=22)
		texte_fin = Texte(self, "Pièces: {} | Temps: {}s" \
			.format(jeu.niveau.pieces, round(jeu.niveau.temps_total)), \
			position=(milieu_ecran_x, milieu_ecran_y), ancrage=(0, 0), \
			taille_police=18)
		bouton_menu = Bouton(self, retour, texte="Retour au menu principal", \
			position=(milieu_ecran_x, milieu_ecran_y + 80), taille=(300, 50), \
			ancrage=(0, 0), taille_police=20)

		self.widgets.append(logo_fin)
		self.widgets.append(titre_fin)
		self.widgets.append(texte_fin)
		self.widgets.append(bouton_menu)

	def supprimer_widgets_pause(self):
		""" Supprimer les 4 derniers widgets crées. Cette méthode ne doit pas
			être appelée pour supprimer un autre menu que celui de pause. """

		self.widgets[-4:] = []

	def actualiser(self, niveau, jeu):
		""" Efface la fenêtre, redessine le terrain, les entités, puis les
			widgets en les actualisant. 

			<niveau> (niveau.Niveau): Le niveau à afficher.
			<jeu> (jeu.Jeu): Le jeu auquel appartient cet affichage. """

		self.afficher_carte(niveau)
		
		for entite in niveau.entites:
			self.afficher_entite(entite)
		
		if jeu.en_partie:
			self.actualiser_scores(niveau)
		
		self.actualiser_widgets()
		pygame.display.update()

	def actualiser_evenements(self, jeu):
		""" Lit les évenements du clavier et de la souris et exécute les
			fonctions associées	à certaines touches (ex: Appui sur la touche Z
			-> le joueur monte).

			<jeu> (jeu.Jeu): Le jeu auquel appartient cet affichage. """

		for evenement in pygame.event.get():
			if evenement.type == pygame.QUIT:
				jeu.arreter()
			elif jeu.en_partie:
				jeu.niveau.actualiser_evenement(evenement)
			for widget in self.widgets:
				widget.actualiser_evenement(evenement)

	def afficher_entite(self, entite):
		""" Affiche une entité en fonction de ses attributs de position,
			taille et rotation.

			<entite> (entites.Entite): L'entité à afficher. """

		joueur = entite.niveau.obtenir_joueur_local()
		
		l, h = self.obtenir_taille()
		milieu_ecran_x = l // 2
		milieu_ecran_y = h // 2

		milieu_entite_x = entite.taille[0] * constantes.General.ZOOM / 2
		milieu_entite_y = entite.taille[1] * constantes.General.ZOOM / 2

		entite_x = (entite.position[0] - joueur.position[0]) \
			* constantes.General.ZOOM + milieu_ecran_x
		entite_y = (entite.position[1] - joueur.position[1]) \
			* constantes.General.ZOOM + milieu_ecran_y

		angle_degres = utile.radian_en_degres(entite.angle)
		image_tournee = pygame.transform.rotate(entite.image, angle_degres)

		d_taille_x = image_tournee.get_size()[0] - entite.image.get_size()[0]
		d_taille_y = image_tournee.get_size()[1] - entite.image.get_size()[1]

		x = int(entite_x - milieu_entite_x - d_taille_x / 2)
		y = int(entite_y - milieu_entite_y - d_taille_y / 2)

		self.fenetre.blit(image_tournee, (x, y))

	def afficher_carte(self, niveau):
		""" Dessine le fond du niveau en fonction de la position du joueur
			pour donner l'impression que celui-ci bouge alors qu'il reste
			constament centré en plein milieu de l'écran.

			<niveau> (niveau.Niveau): Le niveau à afficher. """

		largeur, hauteur = niveau.image.get_size()
		joueur_x, joueur_y = niveau.obtenir_joueur_local().position

		distance_joueur_x = (joueur_x * constantes.General.ZOOM) % largeur
		distance_joueur_y = (joueur_y * constantes.General.ZOOM) % hauteur

		l, h = self.obtenir_taille()
		nb_texture_x = math.ceil(l / largeur)
		nb_texture_y = math.ceil(h / hauteur)

		if distance_joueur_x != 0:
			nb_texture_x += 1
		if distance_joueur_y != 0:
			nb_texture_y += 1

		for x in range(nb_texture_x):
			for y in range(nb_texture_y):
				self.fenetre.blit(niveau.image, (x * largeur \
					- distance_joueur_x, y * hauteur - distance_joueur_y))

	def actualiser_widgets(self):
		""" Redessine tous les widgets de cet affichage. """

		for widget in self.widgets:
			if widget.expire:
				self.widgets.remove(widget)
			else:
				widget.actualiser()

	def actualiser_scores(self, niveau):
		""" Change le texte des Widgets affichant les stats du joueur.

			<niveau> (niveau.Niveau): Le niveau dont il faut afficher
				les stats. """

		texte_temps = self.widgets[0]
		texte_pieces = self.widgets[1]
		texte_vie = self.widgets[2]
		texte_arme = self.widgets[3]
		texte_vitesse = self.widgets[4]

		joueur = niveau.obtenir_joueur_local()

		texte_temps.texte = "Temps: {temps}s".format(temps=int(niveau \
			.temps_total))
		texte_pieces.texte = "Pièces: {pieces}".format(pieces=niveau.pieces)
		texte_vie.texte = "Vie: {vie}".format(vie=int(joueur.vie))
		
		texte_arme.texte = "Bonus dégats: {degats}".format(degats=joueur \
			.degats_bonus)
		texte_vitesse.texte = "Bonus vitesse: x{vitesse}".format(vitesse= \
			round(joueur.vitesse, 2))

	def obtenir_taille(self):
		""" Renvoie la taille en pixel de la surface à la racine de la
			fenêtre (largeur, hauteur). """
			
		return self.fenetre.get_size()