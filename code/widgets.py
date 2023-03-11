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
	Propose des classes permettant la création de widgets.
	Un widget est un élément graphique indépendant et autonome tel qu'un
	bouton, une zone de texte ou une image.
"""

import os.path as op
import time
import pyglet

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"

import constantes


class Widget(object):
    def __init__(self, affichage, position=(0, 0), taille=(1, 1),
                 ancrage=(-1, -1)):
        """ Initialise un widget. 

                <affichage> (affichage.Affichage): La fenêtre sur laquelle
                        dessiner le widget.
                [position] (tuple): La position (x, y) du widget en pixel.
                [taille] (tuple): La taille (largeur, hauteur) du widget en 
                        pixel.
                [ancrage] (tuple): Le point (x, y) d'ancrage du widget en pixel. """

        self.affichage = affichage
        self.position = position
        self.taille = taille
        self.ancrage = ancrage
        self.expire = False

    def actualiser(self):
        """ Cette méthode est appelée à chaque frame de jeu pour redessiner le
                widget sur l'affichage. Ne fait rien par défaut. """

        pass

    def obtenir_position_reelle(self):
        """ Renvoie la position du coin supérieur gauche du widget
                en fonction de ses attributs 'position' et 'ancrage'. """

        x, y = self.position
        ax, ay = self.ancrage
        l, h = self.taille

        if ax == "centre":
            x -= l / 2
        elif ax == "droite":
            x -= l

        if ay == "centre":
            y -= h / 2
        elif ay == "base":
            y -= h / 2
        elif ay == "haut":
            y -= h

        return x, y

    def est_dans_widget(self, position):
        """ Renvoie True si la position est dans le widget sinon False.

                <position> (tuple): La position (x, y) à tester. """

        x, y = self.obtenir_position_reelle()
        largeur, hauteur = self.taille

        if position[0] >= x and position[0] <= x + largeur:
            if position[1] >= y and position[1] <= y + hauteur:
                return True
        return False

    def nettoyer(self):
        pass


class Texte(Widget):
    def __init__(self, affichage, texte, taille_police=18,
                 couleur=(255, 255, 255, 255), **kwargs):

        kwargs["taille"] = (1, 1)
        super().__init__(affichage, **kwargs)

        ax = {"gauche": "left",
              "centre": "center",
              "droite": "right"}.get(self.ancrage[0], "left")
        ay = {"bas": "bottom",
              "centre": "center",
              "base": "baseline",
              "haut": "top"}.get(self.ancrage[1], "bottom")

        self.texte = texte
        self.taille_police = taille_police
        self.nom_police = op.splitext(constantes.Ressources.POLICES[0])[0]
        self.couleur = couleur

        self.etiquette = pyglet.text.Label(self.texte,
                                           font_size=self.taille_police, font_name=self.nom_police,
                                           color=self.couleur,
                                           x=self.position[0], y=self.position[1],
                                           anchor_x=ax, anchor_y=ay)

        self.taille = (self.etiquette.content_width,
                       self.etiquette.content_height)

    def changer_texte(self, texte):
        self.texte = texte
        self.etiquette.text = texte

    def changer_police(self, nom_police):
        self.nom_police = nom_police
        self.etiquette.font_name = nom_police

    def changer_taille_police(self, taille_police):
        self.taille_police = taille_police
        self.etiquette.font_size = taille_police

    def changer_couleur(self, couleur):
        self.couleur = couleur
        self.etiquette.color = couleur

    def actualiser(self):
        self.etiquette.draw()

    def nettoyer(self):
        super().nettoyer()
        self.etiquette.delete()


class Bouton(Widget):
    def __init__(self, affichage, action, texte="", arguments_action=(),
                 taille_police=18, couleur_texte=(255, 255, 255, 255), **kwargs):

        super().__init__(affichage, **kwargs)

        tx, ty = self.obtenir_position_texte()
        self.texte = Texte(affichage, texte, position=(tx, ty),
                           ancrage=("centre", "centre"), taille_police=taille_police,
                           couleur=couleur_texte)

        self.arguments_action = arguments_action
        self.action = action
        self.sprites = {}
        self.etat = "normal"

        self.charger_sprites()
        self.lier_evenements()

    def charger_sprites(self):
        """ Charge les images de fond du bouton. """

        etats = ("clic_central", "clic_droit", "clic_gauche", "desactive",
                 "normal", "survol")

        for etat in etats:
            chemin_image = op.join(constantes.Chemin.IMAGES, "bouton",
                                   "{etat}.png".format(etat=etat))
            sprite = self.affichage.obtenir_sprite(chemin_image)

            image = sprite.image
            ex = self.taille[0] / image.width
            ey = self.taille[1] / image.height
            x, y = self.obtenir_position_reelle()

            sprite.update(x=x, y=y,
                          scale_x=ex, scale_y=ey)

            self.sprites[etat] = sprite

    def lier_evenements(self):
        fenetre = self.affichage.fenetre
        fenetre.push_handlers(on_mouse_motion=self.quand_souris_bouge,
                              on_mouse_press=self.quand_souris_appuie,
                              on_mouse_release=self.quand_souris_relache)

    def actualiser(self):
        self.sprites[self.etat].draw()
        self.texte.actualiser()

    def quand_souris_bouge(self, x, y, dx, dy):
        if self.est_dans_widget((x, y)):
            self.etat = "survol"
        else:
            self.etat = "normal"

    def quand_souris_appuie(self, x, y, bouton, modificateurs):
        if self.est_dans_widget((x, y)):
            if bouton == pyglet.window.mouse.LEFT:
                self.etat = "clic_gauche"
            elif bouton == pyglet.window.mouse.MIDDLE:
                self.etat = "clic_central"
            elif bouton == pyglet.window.mouse.RIGHT:
                self.etat = "clic_droit"

    def quand_souris_relache(self, x, y, bouton, modificateurs):
        if self.est_dans_widget((x, y)):
            if bouton == pyglet.window.mouse.LEFT:
                self.action(*self.arguments_action)

            self.etat = "survol"
        else:
            self.etat = "normal"

    def obtenir_position_texte(self):
        x, y = self.obtenir_position_reelle()
        w, h = self.taille

        return x+w//2, y+h//2

    def nettoyer(self):
        super().nettoyer()

        fenetre = self.affichage.fenetre
        fenetre.remove_handlers(on_mouse_motion=self.quand_souris_bouge,
                                on_mouse_press=self.quand_souris_appuie,
                                on_mouse_release=self.quand_souris_relache)

        self.texte.nettoyer()

        for sprite in self.sprites.values():
            sprite.delete()


class Image(Widget):
    def __init__(self, affichage, chemin_image, **kwargs):
        super().__init__(affichage, **kwargs)

        self.chemin_image = chemin_image
        self.sprite = None
        self.charger_sprite()

    def charger_sprite(self):
        self.sprite = self.affichage.obtenir_sprite(self.chemin_image)
        image = self.sprite.image
        x, y = self.obtenir_position_reelle()

        if self.taille != (0, 0):
            ex = self.taille[0] / image.width
            ey = self.taille[1] / image.height

            self.sprite.update(x=x, y=y, scale_x=ex, scale_y=ey)
        else:
            self.taille = (image.width, image.height)
            self.sprite.update(x=x, y=y)

    def actualiser(self):
        self.sprite.draw()

    def nettoyer(self):
        super().nettoyer()
        self.sprite.delete()


class TexteEditable(Texte):
    def __init__(self, affichage, texte, couleur_curseur=(0, 0, 0, 0),
                 largeur_min=0, **kwargs):

        super().__init__(affichage, texte, **kwargs)

        self.en_edition = False
        self.position_curseur = 0
        self.lier_evenements()

    def lier_evenements(self):
        fenetre = self.affichage.fenetre
        fenetre.push_handlers(on_mouse_motion=self.quand_souris_bouge,
                              on_mouse_press=self.quand_souris_appuie,
                              on_mouse_release=self.quand_souris_relache,
                              on_key_press=self.quand_touche_appuie)

    def deplacer_curseur(self, position):
        if position < 0:
            self.position_curseur = 0
        elif position > len(self.texte):
            self.position_curseur = len(self.texte)
        else:
            self.position_curseur = position

    def quand_souris_bouge(self, x, y, dx, dy):
        if self.est_dans_widget((x, y)):
            r, v, b, a = self.couleur

            r -= 70 if r >= 70 else 0
            v -= 70 if v >= 70 else 0
            b -= 70 if b >= 70 else 0

            self.etiquette.color = (r, v, b, a)
        else:
            self.etiquette.color = self.couleur

    def quand_souris_appuie(self, x, y, bouton, modificateurs):
        self.en_edition = self.est_dans_widget((x, y))

    def quand_souris_relache(self, x, y, bouton, modificateurs):
        pass

    def quand_touche_appuie(self, symbole, modificateurs):
        if self.en_edition:
            touches = pyglet.window.key
            p = self.position_curseur

            if symbole == touches.BACKSPACE:
                if p > 0:
                    self.changer_texte(self.texte[:p-1] + self.texte[p:])
                    self.deplacer_curseur(p - 1)
            elif symbole == touches.DELETE:
                self.changer_texte(self.texte[:p] + self.texte[p+1:])
            elif symbole == touches.LEFT:
                self.deplacer_curseur(p - 1)
            elif symbole == touches.RIGHT:
                self.deplacer_curseur(p + 1)
            elif symbole == touches.UP:
                self.deplacer_curseur(0)
            elif symbole == touches.DOWN:
                self.deplacer_curseur(len(self.texte))
            elif symbole == touches.ESCAPE:
                self.en_edition = False
            elif symbole == touches.ENTER:
                self.en_edition = False
            else:
                pass

    def nettoyer(self):
        fenetre = self.affichage.fenetre
        fenetre.remove_handlers(on_mouse_motion=self.quand_souris_bouge,
                                on_mouse_press=self.quand_souris_appuie,
                                on_mouse_release=self.quand_souris_relache)

        super().nettoyer()


class TexteTemporaire(Texte):
    def __init__(self, affichage, texte, duree, **kwargs):
        """ Initialise un TexteTemporaire avec une durée de vie donnée.

                <affichage> (affichage.Affichage): La fenêtre sur laquelle
                        dessiner l'image.
                <text> (str): Le texte à afficher.
                <duree> (float): La durée de vie du texte.
                [**kwargs] (object): Les attributs hérités de Texte. """

        self.duree = duree
        self.depart = time.time()

        super().__init__(affichage, texte, **kwargs)

    def redemarrer(self):
        """ Remet à zéro le widget. """

        self.expire = False
        self.depart = time.time()

    def actualiser(self):
        """ Redessine le texte sur l'affichage et met à jour son état en
                fonction du temps écoulé. """

        temps_actuel = time.time()

        if temps_actuel - self.depart >= self.duree:
            self.expire = True

        r, v, b, a = self.etiquette.color

        a = 255 - int((time.time() - self.depart) / self.duree * 255)

        if a > 255:
            a = 255
        elif a < 0:
            a = 0

        self.changer_couleur((r, v, b, a))

        super().actualiser()
