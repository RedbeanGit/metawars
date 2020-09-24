# -*- coding: utf-8 -*-

"""
	Contient une classe gérant les activités du jeu.
"""

import constantes
import utile

from affichage import Affichage
from niveau import Niveau
from reseau import Serveur, Client

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"

import time


class Jeu:
	def __init__(self):
		self.affichage = Affichage()
		self.niveau = None
		self.serveur = None
		self.client = None
		self.en_boucle = False
		self.en_partie = False

	def charger(self):
		self.affichage.charger_images()

	def arreter(self):
		if self.serveur:
			self.serveur.arreter()
		utile.arreter()

	def initialiser_menu_principal(self):
		utile.debogguer("Initialisation du menu principal")
		self.affichage.supprimer_widgets()
		self.affichage.creer_widgets_menu(self)
		self.creer_niveau()

		joueur = self.niveau.obtenir_joueur_local()
		joueur.droite()
		joueur.vie = float("inf")
		self.en_partie = False

	def initialiser_partie(self):
		utile.debogguer("Initialisation de la partie")
		self.affichage.supprimer_widgets()
		self.affichage.creer_widgets_partie()
		self.creer_niveau()
		self.en_partie = True

	def initialiser_menu_multijoueur(self):
		utile.debogguer("Initialisation du menu multijoueur")
		self.affichage.supprimer_widgets()
		self.affichage.creer_widgets_multijoueur(self)

	def creer_niveau(self):
		utile.debogguer("Création d'un nouveau niveau")
		self.niveau = Niveau(self)
		self.niveau.creer_joueur()
		self.niveau.initialiser_image()

	def lancer_boucle(self):
		utile.debogguer("Lancement d'une nouvelle boucle de jeu")
		temps_precedent = time.time()
		self.en_boucle = True

		while self.en_boucle:
			temps_ecoule = time.time() - temps_precedent
			temps_precedent = time.time()

			self.affichage.actualiser_evenements(self)
			self.niveau.actualiser(temps_ecoule)
			self.affichage.actualiser(self.niveau, self)

		self.en_boucle = True
		utile.debogguer("Fin d'une boucle de jeu")

	def arreter_boucle(self):
		self.en_boucle = False

	def finir_partie(self):
		utile.debogguer("Fin de la partie")
		self.niveau.en_pause = True
		self.affichage.creer_widgets_fin(self)

	def geler_partie(self, pause=True):
		self.niveau.en_pause = pause

		if pause:
			utile.debogguer("Gêle de la partie")
			self.affichage.creer_widgets_pause(self)
		else:
			utile.debogguer("Dégèle de la partie")
			self.affichage.supprimer_widgets_pause()

	def lancer_mode_heberger(self):
		self.affichage.afficher_message("Ce mode n'est pas encore pris en charge")

	def lancer_mode_rejoindre(self):
		self.affichage.afficher_message("Ce mode n'est pas encore pris en charge")

	def ajouter_joueur(self, pseudo):
		pass

	def enlever_joueur(self, pseudo):
		pass