# -*- coding: utf-8 -*-

#	This file is part of Metawars.
#
#	Metawars is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	Metawars is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with Metawars. If not, see <https://www.gnu.org/licenses/>

"""
	Propose des fonctions utilitaires pouvant êtres utilisées n'importe où.
"""

import constantes

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"

import inspect
import json
import math
import os
import sys
import datetime


def arreter():
	""" Arrête le jeu en tuant le programme. """

	debogguer("Arrêt de " + constantes.General.NOM)
	sys.exit()


def lire_fichier(chemin_fichier):
	""" Permet de lire un fichier à un emplacement donné. 

		<chemin_fichier> (str): Le chemin du fichier. """

	if os.path.exists(chemin_fichier):
		with open(chemin_fichier, "r") as fichier:
			return fichier.read()
	else:
		debogguer("Le fichier '" + chemin_fichier + "' est introuvable !", 1)
		return False


def ecrire_fichier(chemin_fichier, contenu):
	""" Ecrit du texte dans un fichier à un emplacement spécifique. Le fichier
		est créé si il n'existe pas, sinon il est effacé puis recréé.

		<chemin_fichier> (str): Le chemin du fichier.
		<contenu> (str): Le texte à écrire dans le fichier. """

	with open(chemin_fichier, "w") as fichier:
		fichier.write(contenu)


def radian_en_degres(angle):
	""" Convertit un angle en radian, en degré.

		<angle> (float): L'angle en radian à convertir. """

	return angle * 180 / math.pi


def degres_en_radian(angle):
	""" Convertit un angle en degré, en radian.

		<angle> (float): L'angle en degré à convertir. """

	return angle * math.pi / 180


def debogguer(message, niveau_erreur=0):
	""" Affiche un message de debug dans la sortie standard.

		<message> (str): Le message à afficher.
		<niveau_erreur> (int): Le niveau d'erreur entre 0=INFO, 1=ATTENTION ou
			2=ERREUR FATALE (0 par défaut). """

	if constantes.General.DEBUG:
		s = "[{h}:{m}:{s}] [{e}] {t}"
		d = datetime.datetime.now()
		erreur = constantes.General.ERREURS[niveau_erreur]
		print(s.format(h=d.hour, m=d.minute, s=d.second, e=erreur, t=message))


def obtenir_nb_args(fonction):
	""" Renvoie le nombre d'arguments qu'une fonction ou méthode peut prendre.

		<fonction> (callable): La fonction ou méthode à analyser """
		
	signature = inspect.signature(fonction)
	return len(signature.parameters)


def obtenir_classe(module, nom):
	""" Renvoie la classe portant un nom donnée ou None si celle-ci est 
		introuvable.

		<nom> (str): Nom de la classe à chercher """

	if nom in vars(sys.modules[module]):
		return getattr(sys.modules[module], nom)
	return None


def charger_json(s):
	""" Convertit une chaine de caractères au format JSON en object Python.

		<s> (str): La chaine à convertir. """

	return json.loads(s)


def formater_json(o):
	""" Formatte un object Python en chaine de caractère JSON.

		o (object): L'object à formater. """

	return json.dumps(o)