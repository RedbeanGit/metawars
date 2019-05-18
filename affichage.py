# -*- coding: utf-8 -*-

"""
	Contient une classe permettant de créer une fenêtre et de gérer les images.
"""


import constantes
import utile
import niveau
from widgets import Texte, Bouton, Image

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"

import math
import os
import pygame


class Affichage(object):
	""" Permet de créer une fenêtre, charger des images et gérer des Widgets. """

	def __init__(self):
		""" Initialise un nouvel affichage. """

		# on cree une fenetre
		self.fenetre = pygame.display.set_mode(constantes.TAILLE_ECRAN)
		self.images = {}
		self.widgets = []

		# on defini un titre a notre fenetre (ici: MetaWars)
		pygame.display.set_caption(constantes.NOM)
		icone = pygame.image.load(os.path.join("data", "images", "icone.png"))
		pygame.display.set_icon(icone)

	def charge_images(self):
		""" Charge les images du disque dur en mémoire vive. Il est préférable 
			de n'appeler cette méthode qu'une seule fois pour éviter de ralentir le jeu. """

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
		""" Renvoie une surface pygame à un emplacement défini. Si l'image n'a pas été 
			chargée, crée une nouvelle surface noire. 

			<chemin_image> (str): L'emplacement de l'image. """

		if chemin_image in self.images:
			# si l'image existe, on la renvoie
			return self.images[chemin_image].convert_alpha()
		else:
			# sinon, on renvoie une surface noire de 50x50 pixels
			return pygame.Surface((50, 50))

	def supprimer_widgets(self):
		""" Supprime tous les widgets de cet affichage en vidant la liste des widgets. """

		self.widgets.clear() # vide la liste des widgets de cet affichage

	def creer_widgets_niveau(self):
		""" Crée les textes à afficher pendant la partie renseignant sur le temps écoulé,
			les pièces amassées, la vie restante, les dégats et vitesse bonus. """

		texte_temps = Texte(self, "Temps: 0s", (10, 10))
		texte_pieces = Texte(self, "Pièces: 0", (10, 40))
		texte_vie = Texte(self, "Vie: 0", (10, 70))

		texte_arme = Texte(self, "Bonus dégats: 0", (constantes.TAILLE_ECRAN[0] - 10, 10), ancrage=(1, -1))
		texte_vitesse = Texte(self, "Bonus vitesse: x1", (constantes.TAILLE_ECRAN[0] - 10, 40), ancrage=(1, -1))
		
		self.widgets.append(texte_temps)
		self.widgets.append(texte_pieces)
		self.widgets.append(texte_vie)

		self.widgets.append(texte_arme)
		self.widgets.append(texte_vitesse)

	def creer_widgets_menu(self, fct_partie):
		""" Crée un bouton 'Jouer', un bouton 'Quitter', une image de titre et des textes informatifs. """

		milieu_ecran_x = constantes.TAILLE_ECRAN[0] // 2
		milieu_ecran_y = constantes.TAILLE_ECRAN[1] // 2
		milieu_du_milieu_ecran_y = milieu_ecran_y // 2

		bouton_jouer_menu = Bouton(self, fct_partie, "Jouer", position=(milieu_ecran_x, milieu_ecran_y), \
			taille=(300, 50), ancrage=(0, 0), taille_police=20, arguments_action=(self,))

		bouton_quitter_menu = Bouton(self, utile.arreter, "Quitter", position=(milieu_ecran_x, milieu_ecran_y+80), \
			taille=(300, 50), ancrage=(0, 0), taille_police=20)

		logo_menu = Image(self, os.path.join("data", "images", "titre.png"), \
			position=(milieu_ecran_x, milieu_du_milieu_ecran_y), taille=(400, 80),ancrage=(0, 0))

		texte_version = Texte(self, "v" + __version__, position=(10, constantes.TAILLE_ECRAN[1] - 10), \
			ancrage=(-1, 1), taille_police=16)

		texte_dev = Texte(self, __author__, \
			position=(constantes.TAILLE_ECRAN[0] - 10, constantes.TAILLE_ECRAN[1] - 10), ancrage=(1, 1), \
			taille_police=16)

		self.widgets.append(bouton_jouer_menu)
		self.widgets.append(bouton_quitter_menu)
		self.widgets.append(logo_menu)
		self.widgets.append(texte_version)
		self.widgets.append(texte_dev)

	def actualise(self, niveau, en_partie):
		""" Efface la fenêtre, redessine le terrain, les entités, puis les widgets en les actualisant. 

			<niveau> (niveau.Niveau): Le niveau à afficher
			<en_partie> (bool): Si True, actualise les textes affichant les stats du joueur """

		# On rend tous les pixels de la fenetre blanc
		self.fenetre.fill((255, 255, 255))

		# on affiche le fond du niveau
		self.affiche_carte(niveau)

		# on affiche les entités (dont le joueur)
		self.affiche_entite(niveau.joueur)

		for entite in niveau.entites:
			self.affiche_entite(entite)

		# si on est en partie, on acalise le score
		if en_partie:
			# on actualise le score en fonction de celui du niveau
			self.actualise_scores(niveau)

		# on redessine les widgets
		self.affiche_widgets()

		# On actualise l'écran
		pygame.display.update()

	def actualise_evenements(self, niveau, en_partie):
		""" Lit les évenements du clavier et de la souris et exécute les fonctions associées
			à certaines touches (ex: Appui sur la touche Z -> le joueur monte).

			<niveau> (niveau.Niveau): Le niveau à actualiser en fonction des actions utilisateur.
			<en_partie> (bool): si True, fait bouger et tirer le joueur, sinon le joueur ne réagit pas. """

		# on parcourt l'ensemble des evenements utilisateurs (clic, appui sur une touche, etc)
		for evenement in pygame.event.get():

			# si l'utilisateur a cliqué sur la croix rouge de la fenêtre
			# on arrete le jeu
			if evenement.type == pygame.QUIT:
				utile.arreter()

			# sinon si on est en partie (et pas dans le menu principal)
			elif en_partie:
				# si l'utilisateur appui sur une touche du clavier...
				if evenement.type == pygame.KEYDOWN:
					# en fonction de la touche appuyée, on appelle la fonction
					# commandant le déplacement correspondant
					if evenement.key == pygame.K_w:
						niveau.joueur.haut()

					if evenement.key == pygame.K_s:
						niveau.joueur.bas()

					if evenement.key == pygame.K_a:
						niveau.joueur.gauche()

					if evenement.key == pygame.K_d:
						niveau.joueur.droite()

					if evenement.key == pygame.K_ESCAPE:
						utile.arreter()

				# si l'utilisateur relache une touche du clavier...
				elif evenement.type == pygame.KEYUP:
					# en fonction de la touche appuyée, on appelle la fonction
					# commandant le déplacement inverse
					if evenement.key == pygame.K_w:
						niveau.joueur.bas()

					if evenement.key == pygame.K_s:
						niveau.joueur.haut()

					if evenement.key == pygame.K_a:
						niveau.joueur.droite()

					if evenement.key == pygame.K_d:
						niveau.joueur.gauche()

				# si il clique avec la souris
				elif evenement.type == pygame.MOUSEBUTTONDOWN:
					# si le bouton cliqué est le bouton droit de la souris (3)
					if evenement.button == 1:
						niveau.joueur.tir()

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

			# on actualise les évenements pour chaque widget
			for widget in self.widgets:
				widget.actualise_evenement(evenement)

	def affiche_entite(self, entite):
		""" Affiche une entité en fonction de ses attributs de position, taille et rotation.

			<entite> (entites.Entite): L'entité à afficher. """

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
		""" Dessine le fond du niveau en fonction de la position du joueur pour donner
			l'impression que celui-ci bouge alors qu'il reste constament centré en plein
			milieu de l'écran. 

			<niveau> (niveau.Niveau): Le niveau à afficher. """

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
		""" Redessine tous les widgets de cet affichage. """

		for widget in self.widgets:
			widget.actualise()

	def actualise_scores(self, niveau):
		""" Change le texte des Widgets affichant les stats du joueur. 

			<niveau> (niveau.Niveau): Le niveau dont il faut afficher les stats. """

		texte_temps = self.widgets[0]
		texte_pieces = self.widgets[1]
		texte_vie = self.widgets[2]
		texte_arme = self.widgets[3]
		texte_vitesse = self.widgets[4]

		texte_temps.texte = "Temps: {temps}s".format(temps=int(niveau.temps_total))
		texte_pieces.texte = "Pièces: {pieces}".format(pieces=niveau.pieces)
		texte_vie.texte = "Vie: {vie}".format(vie=int(niveau.joueur.vie))
		
		texte_arme.texte = "Bonus dégats: {degats}".format(degats=niveau.joueur.degats_bonus)
		texte_vitesse.texte = "Bonus vitesse: x{vitesse}".format(vitesse=round(niveau.joueur.vitesse, 2))