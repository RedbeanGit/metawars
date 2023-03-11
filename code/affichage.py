# -*- coding: utf-8 -*-

# This file is part of Metawars.
#
# Metawars is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Metawars is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Metawars. If not, see <https://www.gnu.org/licenses/>

"""
	Contient une classe permettant de créer une fenêtre et de gérer les
	images.
"""

import math
import os.path as op
import pyglet

from pyglet.gl import *

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"

import constantes
import utile
from widgets import Texte, Bouton, Image, TexteTemporaire, TexteEditable


class Affichage(object):
    def __init__(self):
        largeur, hauteur = constantes.General.TAILLE_ECRAN
        titre = constantes.General.NOM

        self.fenetre = pyglet.window.Window(
            caption=titre, width=largeur, height=hauteur)
        self.images = {}
        self.menus = []

        self.batch_fond = pyglet.graphics.Batch()
        self.batch_entites = pyglet.graphics.Batch()

    def charger_images(self):
        utile.debogguer("Chargement des images...")

        for chemin_image in constantes.Ressources.IMAGES:
            chemin_image = op.join(constantes.Chemin.IMAGES,
                                   *chemin_image)

            try:
                self.images[chemin_image] = pyglet.image.load(chemin_image)
                utile.debogguer("L'image '" + chemin_image
                                + "' a été chargé !")
            except Exception:
                utile.debogguer("L'image '" + chemin_image
                                + "' n'existe pas !", 1)

        utile.debogguer("Fin du chargement des images !")

    def charger_polices(self):
        utile.debogguer("Chargement des polices...")

        for nom_police in constantes.Ressources.POLICES:
            chemin_police = op.join(constantes.Chemin.RESSOURCES,
                                    nom_police)

            if op.exists(chemin_police):
                pyglet.font.add_file(chemin_police)
                utile.debogguer("La police '" + nom_police
                                + "' a été chargée !")
            else:
                utile.debogguer("La police '" + nom_police
                                + "' n'existe pas !", 1)

        pyglet.font.load()
        utile.debogguer("Fin du chargement des polices !")

    def creer_fond(self):
        l, h = self.obtenir_taille()
        epaisseur = constantes.General.EPAISSEUR_LIGNE \
            * constantes.General.ZOOM
        taille_case = constantes.General.TAILLE_CASE

        nb_case_x = math.ceil(l / constantes.General.ZOOM / taille_case)
        nb_case_y = math.ceil(h / constantes.General.ZOOM / taille_case)

        lignes = []

        for i in range(nb_case_x):
            x = i * taille_case * constantes.General.ZOOM
            ligne = pyglet.shapes.Line(x, 0, x, h, width=epaisseur,
                                       color=(10, 80, 10), batch=self.batch_fond)
            lignes.append(ligne)

        for i in range(nb_case_y):
            y = i * taille_case * constantes.General.ZOOM
            ligne = pyglet.shapes.Line(0, y, l, y, width=epaisseur,
                                       color=(10, 80, 10), batch=self.batch_fond)
            lignes.append(ligne)
        return lignes

    def lier_evenements(self):
        self.fenetre.push_handlers(on_key_press=self.quand_touche_appuie)

    def quand_touche_appuie(self, symbole, modificateurs):
        if symbole == pyglet.window.key.ESCAPE:
            return pyglet.event.EVENT_HANDLED

    def obtenir_sprite(self, chemin_image):
        if chemin_image in self.images:
            return pyglet.sprite.Sprite(img=self.images[chemin_image])
        else:
            fausse_image = pyglet.image.create(16, 16)
            return pyglet.sprite.Sprite(img=fausse_image)

    def ajouter_menu(self, menu):
        self.menus.append(menu)

    def obtenir_dernier_menu(self):
        return self.menus[-1]

    def supprimer_menu(self, menu=None):
        if menu:
            menu.nettoyer()
            self.menus.remove(menu)
        else:
            self.menus.pop().nettoyer()

    def supprimer_menus(self):
        while self.menus:
            self.menus.pop().nettoyer()

    def actualiser(self, niveau, jeu):
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glClearColor(0, 0.4, 0, 1)

        self.fenetre.clear()
        self.actualiser_carte(jeu)

        for entite in niveau:
            self.actualiser_entite(entite)

        self.batch_fond.draw()
        self.batch_entites.draw()

        self.actualiser_menus()

    def actualiser_carte(self, jeu):
        l, h = self.obtenir_taille()
        jx, jy = jeu.niveau.obtenir_joueur_local().position
        lignes = jeu.niveau.lignes_fond
        taille_case = constantes.General.TAILLE_CASE

        nb_case_x = math.ceil(l / constantes.General.ZOOM / taille_case)
        nb_case_y = math.ceil(h / constantes.General.ZOOM / taille_case)
        dx, dy = jx % taille_case, jy % taille_case

        for i in range(nb_case_x):
            x = (i * taille_case - dx) * constantes.General.ZOOM
            lignes[i].x = x
            lignes[i].y = 0
            lignes[i].x2 = x
            lignes[i].y2 = h

        for i in range(nb_case_y):
            y = (i * taille_case - dy) * constantes.General.ZOOM
            lignes[nb_case_x + i].x = 0
            lignes[nb_case_x + i].y = y
            lignes[nb_case_x + i].x2 = l
            lignes[nb_case_x + i].y2 = y

    def actualiser_entite(self, entite):
        jx, jy = entite.niveau.obtenir_joueur_local().position
        fl, fh = self.obtenir_taille()

        rotation = utile.radian_en_degres(entite.angle)
        x = (entite.position[0] - jx) * constantes.General.ZOOM + fl / 2
        y = (entite.position[1] - jy) * constantes.General.ZOOM + fh / 2
        largeur = entite.taille[0] * constantes.General.ZOOM
        hauteur = entite.taille[1] * constantes.General.ZOOM

        image = entite.sprite.image
        echelle_x = largeur / image.width
        echelle_y = hauteur / image.height

        entite.sprite.update(x=x, y=y, rotation=rotation,
                             scale_x=echelle_x, scale_y=echelle_y)

    def actualiser_menus(self):
        for menu in self.menus:
            menu.actualiser()

    def obtenir_taille(self):
        return self.fenetre.get_size()

    def nettoyer(self):
        self.fenetre.remove_handlers(on_key_press=self.quand_touche_appuie)

    def afficher_message(self, message):
        self.obtenir_dernier_menu().afficher_message(message)
