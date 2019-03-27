# -*- coding: utf-8 -*-

from entites import Joueur

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"


class Niveau(object):
	"""
	Gere l'ensemble des entités du jeu.
	"""

	def __init__(self):
		self.texture = None
		self.joueur = Joueur(self)
		self.entites = []

	def charge_image(self, affichage):
		# Cette methode ne fonctionne pas sur Windows
		# a vous de regler le probleme ehe :-p
		self.texture = affichage.obtenir_image("data/images/map_background.png")
		self.joueur.charge_image(affichage)

	def actualise(self, temps):
		self.joueur.actualise(temps)
		
		for entite in self.entites:
			entite.actualise(temps)