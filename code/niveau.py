# -*- coding: utf-8 -*-

import constantes
import utile

from entites import Joueur, Ennemi, Bonus

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"

import os
import pygame
import random


class Niveau(object):
	""" Gère l'ensemble des entités du jeu ainsi que certaines données de partie. """

	def __init__(self, jeu):
		self.image = None
		self.jeu = jeu
		self.entites = []
		self.pieces = 0
		self.temps_total = 0
		self.en_pause = False

	def creer_joueur(self):
		joueur = Joueur(self)
		joueur.charger_image()
		self.entites.append(joueur)

	def obtenir_joueur_local(self):
		for entite in self.entites:
			if isinstance(entite, Joueur):
				return entite

		return Joueur(self)

	def initialiser_image(self):
		""" Charge l'image de fond et celle du joueur. """

		# on charge le fond du niveau
		self.image = self.jeu.affichage.obtenir_image(constantes.General.IMAGE_FOND)

	def actualiser(self, temps):
		""" Actualise les entités et tente de faire apparaitre des bonus et des ennemis.

			<temps> (float): Le temps écoulé depuis la dernière actualisation. """

		if not self.en_pause:
			self.temps_total += temps
			
			for entite in self.entites:
				entite.actualiser(temps)

			self.faire_apparaitre(temps)

	def actualiser_evenement(self, evenement):
		joueur = self.obtenir_joueur_local()

		# si l'utilisateur appui sur une touche du clavier...
		if evenement.type == pygame.KEYDOWN:
			if not self.en_pause:
				# en fonction de la touche appuyée, on appelle la fonction
				# commandant le déplacement correspondant
				if evenement.key == pygame.K_w:
					joueur.haut()
				if evenement.key == pygame.K_s:
					joueur.bas()
				if evenement.key == pygame.K_a:
					joueur.gauche()
				if evenement.key == pygame.K_d:
					joueur.droite()

			if evenement.key == pygame.K_ESCAPE:
				self.jeu.geler_partie(not self.en_pause)

		# si l'utilisateur relache une touche du clavier...
		elif evenement.type == pygame.KEYUP:
			if not self.en_pause:
				# en fonction de la touche appuyée, on appelle la fonction
				# commandant le déplacement inverse
				if evenement.key == pygame.K_w:
					joueur.bas()
				if evenement.key == pygame.K_s:
					joueur.haut()
				if evenement.key == pygame.K_a:
					joueur.droite()
				if evenement.key == pygame.K_d:
					joueur.gauche()

		# si il clique avec la souris
		elif evenement.type == pygame.MOUSEBUTTONDOWN:
			if not self.en_pause:
				# si le bouton cliqué est le bouton droit de la souris (1)
				if evenement.button == 1:
					joueur.tirer()

		# si la souris bouge
		elif evenement.type == pygame.MOUSEMOTION:
			if not self.en_pause:
				x, y = evenement.pos

				# on calcul l'écart entre la position de la souris et le milieu de la fenêtre
				dx = x - constantes.General.TAILLE_ECRAN[0] / 2
				dy = y - constantes.General.TAILLE_ECRAN[1] / 2

				# on enlève le zoom pour convertir cet écart dans l'échelle du niveau
				dx_niveau = dx / constantes.General.ZOOM
				dy_niveau = dy / constantes.General.ZOOM

				# on fait en sorte que le joueur regarde la position de la souris
				joueur.regarder_position(dx_niveau, dy_niveau)

	def faire_apparaitre(self, temps):
		""" Fait parfois apparaitre un bonus et/ou un ennemi.

			<temps> (float): Le temps écoulé depuis la dernière actualisation. """

		# on pioche un nombre aléatoire
		nb = random.random()

		# si le nombre pioché est inférieur au temps écoulé divisé 
		# par la fréquence moyenne d'apparition...
		if nb <= temps / constantes.Ennemi.FREQUENCE_APPARITION:
			# on crée un ennemi
			self.creer_ennemi()

		# pareil pour les bonus
		nb = random.random()

		if nb <= temps / constantes.Bonus.FREQUENCE_APPARITION:
			self.creer_bonus()

	def enlever_entite(self, entite):
		""" Enlève une entité donnée de la liste des entités. 

			<entite> (entites.Entite): L'entité à enlever. """

		# si l'entité fait bien parti de la liste des entités de ce niveau
		if entite in self.entites:
			# on la retire de la liste (elle ne fait donc plus parti du niveau)
			self.entites.remove(entite)

	def creer_bonus(self):
		""" Crée un nouveau bonus à une position aléatoire proche du joueur. """

		# on crée un bonus
		bonus = Bonus(self)
		joueur = self.obtenir_joueur_local()

		# on choisi aléatoirement la distance entre le joueur et le bonus
		dx = (random.random() - 0.5) * 2 * constantes.Bonus.DIS_MAX
		dy = (random.random() - 0.5) * 2 * constantes.Bonus.DIS_MAX

		# on redéfinit la position du Bonus autour le joueur
		bonus.position[0] = joueur.position[0] + dx
		bonus.position[1] = joueur.position[1] + dy

		# on lui fait charger son image
		bonus.charger_image()

		# on ajoute le bonus a la liste des entités
		self.entites.append(bonus)

	def creer_ennemi(self):
		""" Crée un nouvel ennemi à une position aléatoire proche du joueur. """

		# on crée un ennemi
		ennemi = Ennemi(self)
		joueur = self.obtenir_joueur_local()
		
		# on choisi aléatoirement la distance entre l'ennemi et le joueur
		dx = (random.random() - 0.5) * 2 * constantes.Ennemi.DIS_MAX
		dy = (random.random() - 0.5) * 2 * constantes.Ennemi.DIS_MAX
		# on redéfinit la position de l'ennemi autour du joueur
		ennemi.position[0] = joueur.position[0] + dx
		ennemi.position[1] = joueur.position[1] + dy

		# on lui fait charger ses images
		ennemi.charger_image()
		# on ajoute l'ennemi a la liste des entités
		self.entites.append(ennemi)

	def quand_joueur_meurt(self, joueur):
		""" Met en pause le niveau. """

		if joueur == self.obtenir_joueur_local():
			self.jeu.finir_partie()
		else:
			utile.debogguer("Un joueur distant est mort")