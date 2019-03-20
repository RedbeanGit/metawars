# -*- coding: utf-8 -*-

import constants

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"

import json
import os
import sys


def exit():
	print("Arrêt de {name}...".format(name=constants.NAME))
	sys.exit()


def read_file(path):
	"""Permet de lire un fichier à l'emplacement 'path'"""

	# On teste si le fichier existe bel et bien
	if os.path.exists(path):
		# si oui, on l'ouvre en mode lecture ("r")
		# et on le stocke dans la variable file
		with open(path, "r") as file:
			# on retourne son contenu avec la methode read()
			return file.read()
	else:
		print("Le fichier '{path}' est introuvable !".format(path=path))
		return False


def write_file(path, content):
	"""Permet d'écrire 'content' dans un fichier à l'emplacement 'path'.
	Si le fichier n'existe pas, il sera créé automatiquement par python."""

	# On ouvre le fichier en mode écriture ("w")
	# et on le stocke dans la variable file
	with open(path, "w") as file:
		file.write(content)


def read_json(path):
	"""Permet de lire un fichier .json et renvoi une structure de donnée python
	(ex: list, dict, str, int, float)"""

	# On charge le contenu du fichier dans la variable content
	content = read_file(path)

	# On teste si le contenu du fichier a bien été lu
	# Si ce n'est pas le cas, content vaut False
	if content:
		# On transforme le contenu sous forme de text en objets python
		# ex: list, dict, str, int ou encore float
		return json.loads(content)
	else:
		return False


def write_json(path, content):
	"""Écrit un objet python dans un fichier json.
	Seuls les objets de type float, int, list, dict ou str sont acceptés"""

	# On transforme nos objets python en texte
	text = json.dumps(content, indent="\t")
	# On écrit ce texte dans un fichier
	write_file(path, text)