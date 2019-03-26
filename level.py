# -*- coding: utf-8 -*-

from entity import Player

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

	def load_image(self, display):
		self.texture = display.get_image("data/images/map_background.png")

	def init_player(self):
		self.player = Player(self)

	def update(self, deltatime):
		self.player.update(deltatime)
		
		for entity in self.entities:
			entity.update(deltatime)