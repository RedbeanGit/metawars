#!/usr/bin/python3z
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
	Script principal du jeu. Ne contient qu'une seule fonction permettant de
	créer et lancer le jeu.
"""

import traceback

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__repo__ = "https://github.com/Ptijuju22/metawars.git"

import constantes
import utile

from jeu import Jeu


def demarrer():
	""" Crée une instance de Jeu lance une première boucle de jeu. Si une
		erreur se produit, affiche un rapport d'erreur et arrête le jeu
		proprement. """

	jeu = Jeu()
	jeu.charger()
	jeu.initialiser_menu_principal()

	try:
		jeu.lancer_boucle()
	except Exception as e:
		utile.debogguer("Une erreur non gérée est survenue pendant l'exécution", 2)
		traceback.print_exc()
	finally:
		jeu.arreter()



if __name__ == "__main__":
	# le programme démarre ici
	utile.debogguer("Démarrage de " + constantes.General.NOM)
	demarrer()
