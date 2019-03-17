# -*- coding: utf-8 -*-

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"


class Entity(object):
	"""
	Classe de base pour l'ensemble des entités.
	"""

    def __init__(self):
        pass


class Player(Entity):
	"""
	Classe définissant l'entité dirigée par le joueur.
	"""

    pass


class Enemy(Entity):
	"""
	Classe définissant une entité ennemie.
	"""

    pass


class Bonus(Entity):
	"""
	Classe définissant un bonus attrapable par le joueur.
	"""

	pass


class Shot(Entity):
	"""
	Classe définissant un tir de missile.
	"""

	pass