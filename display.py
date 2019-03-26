# -*- coding: utf-8 -*-

import constants
import util

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"

import os
import pygame
from pygame.locals import QUIT


class Display(object):
	def __init__(self):
		self.window = pygame.display.set_mode((500, 500))
		self.images = {}

	def load_images(self):
		print("Chargement des images !!!")
		for chemin in constants.IMAGES:
			chemin = os.path.join("data", "images", *chemin)

			try:
				self.images[chemin] = pygame.image.load(chemin)
				print("L'image {image} a été chargé !".format(image=chemin))
			except pygame.error:
				print("L'image {image} n'existe pas !".format(image=chemin))

	def get_image(self, chemin_image):
		if chemin_image in self.images:
			return self.images[chemin_image].convert_alpha()
		else:
			return pygame.Surface((50, 50))

	def update(self, level):
		self.window.fill((0, 0, 0))

		if level.texture:
			self.window.blit(level.texture, (0, 0))

		if level.player:
			self.window.blit(level.player.texture, (250, 250))

		pygame.display.update()

	def update_events(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				util.exit()