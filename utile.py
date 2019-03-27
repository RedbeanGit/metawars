# -*- coding: utf-8 -*-

import constantes

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"

import os
import sys


def arret():
	print("Arrêt de {nom}...".format(nom=constantes.NOM))
	sys.exit()


def lit_fichier(chemin_fichier):
	"""Permet de lire un fichier à l'emplacement 'chemin_fichier'"""

	# On teste si le fichier existe bel et bien
	if os.path.exists(chemin_fichier):
		# si oui, on l'ouvre en mode lecture ("r")
		# et on le stocke dans la variable 'fichier'
		with open(chemin_fichier, "r") as fichier:
			# on retourne son contenu avec la methode read()
			return fichier.read()
	else:
		print("Le fichier '{chemin}' est introuvable !".format(chemin=chemin_fichier))
		return False


def ecrit_fichier(chemin_fichier, contenu):
	"""Permet d'écrire 'contenu' dans un fichier à l'emplacement 'chemin_fichier'.
	Si le fichier n'existe pas, il sera créé automatiquement par python."""

	# On ouvre le fichier en mode écriture ("w")
	# et on le stocke dans la variable 'fichier'
	with open(chemin_fichier, "w") as fichier:
		fichier.write(contenu)