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
	Contient une classe gérant les activités du jeu.
"""

import pyglet
import time

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois; Crush et l'Avocat"

import utile

from affichage import Affichage
from menus import MenuFin, MenuHeberger, MenuMultijoueur, MenuPartie, \
    MenuPause, MenuPrincipal, MenuRejoindre
from niveau import Niveau, NiveauClient, NiveauServeur
from reseau import Serveur, Client


class Jeu:
    """ Cette classe sert principalement d'interface entre un Affichage et un 
            Niveau. Elle initialise et actualise les objets à chaque changement de
            menu. """

    def __init__(self):
        """ Initialise le jeu en créant un nouvel affichage et en définissant
                tous les attributs de l'objet à None ou False. """

        self.affichage = Affichage()
        self.niveau = None
        self.serveur = None
        self.client = None
        self.en_boucle = False
        self.en_partie = False

    def charger(self):
        """ Charge les images du jeu dans la mémoire vive. """

        self.affichage.charger_polices()
        self.affichage.charger_images()
        self.affichage.lier_evenements()

    def arreter(self):
        """ Arrête le programme après avoir arrêté le serveur et / ou le
                client si une partie en réseau a été lancée. """

        if self.serveur:
            self.serveur.arreter_ecoute()
            self.serveur.arreter_echange()

        if self.client:
            self.client.arreter_echange()
            self.client.deconnecter()

        self.affichage.nettoyer()
        utile.arreter()

    def initialiser_menu_principal(self):
        """ Crée un niveau de fond et les widgets du menu principal. """

        utile.debogguer("Initialisation du menu principal")

        self.affichage.supprimer_menus()
        self.affichage.ajouter_menu(MenuPrincipal(self))

        self.creer_niveau()

        joueur = self.niveau.creer_joueur()
        joueur.droite()
        joueur.vie = float("inf")

        self.niveau.ajouter_entite(joueur)
        self.niveau.joueur_id = joueur.identifiant
        self.en_partie = False

    def initialiser_menu_multijoueur(self):
        """ Crée les widgets du menu multijoueur principal. Réutilise le
                niveau de fond déjà crée. """

        utile.debogguer("Initialisation du menu multijoueur")
        self.affichage.supprimer_menus()
        self.affichage.ajouter_menu(MenuMultijoueur(self))

    def initialiser_menu_heberger(self):
        """ Crée les widgets du menu de réglage du serveur (héberger).
                Réutilise le niveau de fond déjà crée. """

        utile.debogguer("Initialisation du menu héberger")
        self.affichage.supprimer_menus()
        self.affichage.ajouter_menu(MenuHeberger(self))

    def initialiser_menu_rejoindre(self):
        """ Crée les widgets du menu de réglage du client (rejoindre).
                Réutilise le niveau de fond déjà crée. """

        utile.debogguer("Initialisation du menu rejoindre")
        self.affichage.supprimer_menus()
        self.affichage.ajouter_menu(MenuRejoindre(self))

    def initialiser_partie(self):
        """ Crée un niveau et les widgets de partie. """

        utile.debogguer("Initialisation d'une partie")
        self.affichage.supprimer_menus()
        self.affichage.ajouter_menu(MenuPartie(self))

        self.creer_niveau()
        self.niveau.lier_evenements()

        joueur = self.niveau.creer_joueur()
        self.niveau.ajouter_entite(joueur)
        self.niveau.joueur_id = joueur.identifiant

        self.en_partie = True

    def initialiser_partie_serveur(self, port):
        """ Crée puis lance un serveur écoutant sur un port donné. Si le
                serveur arrive à se lier au port donné, crée un niveau ainsi
                que les widgets de partie (comme en mode solo).

                <port> (int): Le port d'écoute du serveur. """

        self.serveur = Serveur(self, port)

        if not self.serveur.accrocher():
            self.affichage.afficher_message("Impossible de créer un serveur")
            self.arreter_boucle()
        else:
            utile.debogguer("Initialisation d'une partie (serveur)")
            self.affichage.supprimer_menus()
            self.affichage.ajouter_menu(MenuPartie(self))

            self.creer_niveau("serveur")
            self.niveau.lier_evenements()

            joueur = self.niveau.creer_joueur()
            self.niveau.ajouter_entite(joueur)
            self.niveau.joueur_id = joueur.identifiant

            self.serveur.lancer_ecoute()
            self.serveur.lancer_echange()

            self.en_partie = True

    def initialiser_partie_client(self, adresse, port):
        """ Crée un client et lance une tentative de connexion à l'adresse et
                le port donnés. Si la tentative réussi, crée un niveauClient et
                lance la boucle d'échange du client.

                <adresse> (str): L'adresse du serveur à joindre.
                <port> (int): Le port d'écoute du serveur. """

        self.client = Client(self)

        if not self.client.connecter(adresse, port):
            self.affichage.afficher_message("Impossible de se connecter")
            self.arreter_boucle()
        else:
            utile.debogguer("Initialisation d'une partie (client)")
            self.affichage.supprimer_menus()
            self.affichage.ajouter_menu(MenuPartie(self))
            self.affichage.afficher_message("Connecté au serveur !")

            self.creer_niveau("client")
            self.niveau.lier_evenements()

            self.client.lancer_echange()

            self.en_partie = True

    def creer_niveau(self, mode="solo"):
        """ Crée et initialise un nouveau niveau ainsi qu'un joueur.

                [mode] (str): Le mode de gestion du niveau (solo, client ou
                        serveur). (solo par défaut). """

        utile.debogguer("Création d'un nouveau niveau")

        if self.niveau:
            self.niveau.nettoyer()

        if mode == "solo":
            self.niveau = Niveau(self)
        elif mode == "client":
            self.niveau = NiveauClient(self, self.client)
        elif mode == "serveur":
            self.niveau = NiveauServeur(self, self.serveur)
        self.niveau.charger_fond()

    def lancer_boucle(self):
        """ Lance une nouvelle boucle de jeu en mettant en pause la boucle 
                de jeu actuellement active. Une nouvelle boucle est généralement
                lancée à la création d'un nouveau menu. """

        utile.debogguer("Lancement de la boucle de jeu")
        pyglet.clock.schedule(self.actualiser)
        pyglet.app.run()
        utile.debogguer("Fin de la boucle de jeu")

    def actualiser(self, temps_ecoule):
        self.niveau.actualiser(temps_ecoule)
        self.affichage.actualiser(self.niveau, self)

    def arreter_partie(self):
        """ Déconnecte le client ou arrête le serveur si une partie réseau est
                en cours. """

        if self.client:
            self.client.arreter_echange()
            self.client.deconnecter()
        if self.serveur:
            self.serveur.arreter_ecoute()
            self.serveur.arreter_echange()

    def finir_partie(self):
        """ Affiche le menu de fin de partie. """

        utile.debogguer("Fin de la partie")

        self.niveau.en_pause = True
        self.en_partie = False
        self.affichage.ajouter_menu(MenuFin(self))

    def finir_partie_serveur(self):
        """ Affiche le menu de fin de partie en tant que serveur. """

        utile.debogguer("Fin de partie en tant que serveur")
        self.niveau.enlever_entite(self.niveau.obtenir_joueur_local())

    def finir_partie_client(self):
        """ Affiche le menu de fin de partie en tant que client. """

        utile.debogguer("Fin de partie en tant que client")
        self.niveau.enlever_entite(self.niveau.obtenir_joueur_local())

    def geler_partie(self, pause=True):
        """ Met la partie en pause en créant le menu de pause ou continue la
                partie en supprimant les widgets de pause.

                [pause] (bool): Si True, met le jeu en pause, sinon continue la
                        partie. (True par défaut). """

        self.niveau.en_pause = pause

        if pause:
            utile.debogguer("Gel de la partie")
            self.affichage.ajouter_menu(MenuPause(self))
        else:
            utile.debogguer("Dégel de la partie")
            self.affichage.supprimer_menu()

    def ajouter_client(self, adresse):
        """ Ajoute un joueur à la partie et envoie le niveau en cours à ce
                dernier. Cette méthode est généralement appelée par un serveur
                lorsqu'un client se connecte.

                <adresse> (str): L'adresse du client qui vient de se connecter. """

        self.affichage.afficher_message("Un joueur vient de se connecter")

        joueur = self.niveau.creer_joueur()
        self.niveau.ajouter_entite(joueur)
        self.niveau.envoyer()
        self.niveau.definir_joueur(adresse, joueur)

    def enlever_client(self, adresse):
        """ Enlève un joueur de la partie et préviens touts les autres. Cette
                méthode est généralement appelée par un serveur lorsqu'un client
                se déconnecte.

                <adresse> (str): L'adresse du client qui vient de se déconnecter. """

        self.affichage.afficher_message("Un joueur vient de se déconnecter")
