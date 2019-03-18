# -*- coding: utf-8 -*-

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"


class Level(object):
	"""
	Gere l'ensemble des entités du jeu.
	"""

	def __init__(self):
		self.texture = None
		self.player = None
		self.entities = []

	def update(self, deltatime):
		self.player.update(deltatime)
		
		for entity in self.entities:
			entity.update(deltatime)