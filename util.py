# -*- coding: utf-8 -*-

import constants

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"

import sys


def exit():
	print("Arrêt de {name}...".format(name=constants.NAME))
	sys.exit()