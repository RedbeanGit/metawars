# -*- coding: utf-8 -*-

import constants

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"

import math
import random


class Entity(object):
	"""
	Classe de base pour l'ensemble des entités.
	"""

    def __init__(self, level):
    	self.level = level
        self.size = [0, 0]
        self.speed = 0
        self.angle = 0
        self.pos = [0, 0]
        self.texture = None

    def update(self, deltatime):
    	self.move(deltatime)

    def move(self, deltatime):
    	self.pos[0] += self.speed * math.cos(self.angle) * deltatime
    	self.pos[1] += self.speed * math.sin(self.angle) * deltatime


class Player(Entity):
	"""
	Classe définissant l'entité dirigée par le joueur.
	"""

    def shot(self):
    	self.level.entities.append(Shot())

    def forward(self):
    	self.speed = constants.PLAYER_SPEED

    def backward(self):
    	self.speed = -constants.PLAYER_SPEED

    def stop(self):
    	self.speed = 0


class Enemy(Entity):
	"""
	Classe définissant une entité ennemie.
	"""

	def __init__(self):
		super().__init__()
		self.speed = constants.ENEMY_SPEED

	def update(self, deltatime):
		super().update(deltatime)
		self.rotate()

	def rotate(self):
		x = self.pos[0] - self.level.player.pos[0]
		y = self.pos[1] - self.level.player.pos[1]

		r = math.sqrt(x ** 2 + y ** 2)
		c = x / r

		angle = math.acos(c)

		if y >= 0:
			self.angle = angle
		else:
			self.angle = -angle

    def shot(self):
    	self.level.entities.append(Shot())


class Bonus(Entity):
	"""
	Classe définissant un bonus attrapable par le joueur.
	"""
	def spawn(self):
		self.pos = [random.randint(0,SCREEN_SIZE_X),random.randint(0,SCREEN_SIZE_Y)]
		


class Shot(Entity):
	"""
	Classe définissant un tir de missile.
	"""

	def __init__(self):
		self.damage = constants.SHOT_DAMAGE
