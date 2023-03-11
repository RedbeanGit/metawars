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
	Contient plusieurs classes définissant un niveau et ces variantes lors
	d'une partie en réseau.
"""

import pyglet
import random

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"

import constantes
import utile

from entites import Joueur, Ennemi, Bonus, Entite


class Niveau(object):
	""" Gère l'ensemble des entités du jeu ainsi que certaines données de
		partie. """

	def __init__(self, jeu):
		""" Initialise un niveau. Tous les attributs sont définis ici.

			<jeu> (jeu.Jeu): Le jeu auquel appartient ce niveau. """

		self.lignes_fond = []
		self.jeu = jeu
		self.entites = []
		self.pieces = 0
		self.temps_total = 0
		self.en_pause = False
		self.joueur_id = -1

	def __iter__(self):
		for entite in self.entites:
			yield entite

	def creer_joueur(self):
		""" Renvoie un nouveau joueur dont les images ont été chargées. """

		joueur = Joueur(self)
		joueur.charger_sprite()

		return joueur

	def creer_bonus(self):
		""" Renvoie un nouveau bonus en définissant une position aléatoire
			proche de l'un des joueurs. """

		bonus = Bonus(self)
		joueur = random.choice(self.obtenir_joueurs())

		dx = (random.random() - 0.5) * 2 * constantes.Bonus.DIS_MAX
		dy = (random.random() - 0.5) * 2 * constantes.Bonus.DIS_MAX

		bonus.position[0] = joueur.position[0] + dx
		bonus.position[1] = joueur.position[1] + dy

		bonus.charger_sprite()

		return bonus

	def creer_ennemi(self):
		""" Renvoie un nouvel ennemi en définissant une position aléatoire
			proche du joueur. """

		ennemi = Ennemi(self)
		joueur = random.choice(self.obtenir_joueurs())
		
		dx = (random.random() - 0.5) * 2 * constantes.Ennemi.DIS_MAX
		dy = (random.random() - 0.5) * 2 * constantes.Ennemi.DIS_MAX
		
		ennemi.position[0] = joueur.position[0] + dx
		ennemi.position[1] = joueur.position[1] + dy

		ennemi.charger_sprite()
		
		return ennemi

	def ajouter_entite(self, entite):
		""" Ajoute une entité à la liste des entités de ce niveau. Cette
			vérifie si l'entité ne fait pas déjà partie du niveau.

			<entite> (entites.Entite): L'entité à ajouter. """

		if entite not in self.entites:
			self.entites.append(entite)

	def enlever_entite(self, entite):
		""" Enlève une entité donnée de la liste des entités. Cette méthode
			vérifie si l'entité fait bien partie du niveau.

			<entite> (entites.Entite): L'entité à enlever. """

		if entite in self.entites:
			entite.nettoyer()
			self.entites.remove(entite)

	def obtenir_entite(self, identifiant):
		""" Renvoie l'entité associée à un identifiant donné ou None si aucune
			entité ne possède cet identifiant.

			<identifiant> (int): L'identifiant de l'entité à obtenir. """

		for entite in self.entites:
			if entite.identifiant == identifiant:
				return entite
		return None

	def obtenir_joueur_local(self):
		""" Renvoie le joueur associé à l'identifiant local ou un joueur
			fictif si aucun joueur n'est associé à cet identifiant. """

		joueur = self.obtenir_entite(self.joueur_id)

		if joueur:
			return joueur
		return Joueur(self)

	def obtenir_joueurs(self):
		""" Retourne la liste des joueurs. """

		return [e for e in self.entites if isinstance(e, Joueur)]

	def charger_fond(self):
		""" Charge l'image de fond et celle du joueur. """

		affichage = self.jeu.affichage
		self.lignes_fond = affichage.creer_fond()

	def actualiser(self, temps):
		""" Actualise les entités et tente de faire apparaitre des bonus et
			des ennemis.

			<temps> (float): Le temps écoulé depuis la dernière actualisation. """

		if not self.en_pause:
			self.temps_total += temps
			
			for entite in self.entites:
				entite.actualiser(temps)

			self.faire_apparaitre(temps)

	def actualiser_evenement(self, evenement):
		""" Modifie le niveau et les entités en fonction d'un évènement donné
			(appui sur une touche, clic de souris, déplacement de souris,...).

			<evenement> (pygame.event.Event): L'évènement déclencheur. """

		if evenement.type == pygame.KEYDOWN:
			if evenement.key == pygame.K_ESCAPE:
				self.jeu.geler_partie(not self.en_pause)

		joueur = self.obtenir_joueur_local()
		self.commander_joueur(joueur, evenement)

	def lier_evenements(self):
		fenetre = self.jeu.affichage.fenetre
		fenetre.push_handlers(on_mouse_motion=self.quand_souris_bouge, \
			on_mouse_press=self.quand_souris_appuie, \
			on_key_press=self.quand_touche_appuie, \
			on_key_release=self.quand_touche_relache)

	def quand_souris_bouge(self, x, y, dx, dy):
		joueur = self.obtenir_joueur_local()
		self.commander_joueur(joueur, "souris_bouge", x, y, dx, dy)

	def quand_souris_appuie(self, x, y, bouton, modificateurs):
		joueur = self.obtenir_joueur_local()
		self.commander_joueur(joueur, "souris_appuie", x, y, bouton, \
			modificateurs)

	def quand_touche_appuie(self, symbole, modificateurs):
		if symbole == pyglet.window.key.ESCAPE:
			self.jeu.geler_partie(not self.en_pause)

		joueur = self.obtenir_joueur_local()
		self.commander_joueur(joueur, "touche_appuie", symbole, modificateurs)

	def quand_touche_relache(self, symbole, modificateurs):
		joueur = self.obtenir_joueur_local()
		self.commander_joueur(joueur, "touche_relache", symbole, \
			modificateurs)

	def commander_joueur(self, joueur, type_evenement, *arguments):
		""" Fait bouger un joueur en fonction d'un évènement donné.

			<joueur> (entites.Joueur): Le joueur sur lequel s'applique cet
				évènement.
			<evenement> (pygame.event.Event): L'évènement déclencheur. """
		
		if type_evenement == "touche_appuie":
			if not self.en_pause:
				if arguments[0] == pyglet.window.key.Z:
					joueur.haut()
				elif arguments[0] == pyglet.window.key.S:
					joueur.bas()
				elif arguments[0] == pyglet.window.key.Q:
					joueur.gauche()
				elif arguments[0] == pyglet.window.key.D:
					joueur.droite()

		elif type_evenement == "touche_relache":
			if not self.en_pause:
				if arguments[0] == pyglet.window.key.Z:
					joueur.bas()
				elif arguments[0] == pyglet.window.key.S:
					joueur.haut()
				elif arguments[0] == pyglet.window.key.Q:
					joueur.droite()
				elif arguments[0] == pyglet.window.key.D:
					joueur.gauche()

		elif type_evenement == "souris_appuie":
			if not self.en_pause:
				if arguments[2] == pyglet.window.mouse.LEFT:
					joueur.tirer()

		elif type_evenement == "souris_bouge":
			if not self.en_pause:
				x, y, dx, dy = arguments
				l, h = self.jeu.affichage.obtenir_taille()
				
				distance_x = (x - l / 2) / constantes.General.ZOOM
				distance_y = (y - h / 2) / constantes.General.ZOOM

				joueur.regarder_position(distance_x, distance_y)

	def faire_apparaitre(self, temps):
		""" Fait parfois apparaitre un bonus et/ou un ennemi.

			<temps> (float): Le temps écoulé depuis la dernière actualisation. """

		nb = random.random()

		if nb <= temps / constantes.Ennemi.FREQUENCE_APPARITION:
			self.ajouter_entite(self.creer_ennemi())

		nb = random.random()

		if nb <= temps / constantes.Bonus.FREQUENCE_APPARITION:
			self.ajouter_entite(self.creer_bonus())

	def quand_joueur_meurt(self, joueur):
		""" Si le joueur mort est le joueur local alors lance les fonctions de
			fin de partie. Sinon supprime simplement le joueur mort.

			<joueur> (entites.Joueur): Le joueur venant de mourir. """

		if joueur == self.obtenir_joueur_local():
			self.jeu.finir_partie()
		else:
			self.enlever_entite(joueur)

	def nettoyer(self):
		fenetre = self.jeu.affichage.fenetre
		fenetre.remove_handlers(on_mouse_motion=self.quand_souris_bouge, \
			on_mouse_press=self.quand_souris_appuie, \
			on_key_press=self.quand_touche_appuie, \
			on_key_release=self.quand_touche_relache)

		while self.entites:
			self.entites.pop().nettoyer()


class NiveauReseau(Niveau):
	""" Classe de base des niveau gérant des parties en réseau. """

	def __init__(self, jeu):
		""" Initialise un niveau réseau en apportant un attribut actions pour
			référencer les actions de l'utilisateurs jusqu'à ce qu'ils soient
			envoyés.

			<jeu> (jeu.Jeu): Le jeu auquel appartient ce niveau. """

		super().__init__(jeu)

		self.actions = []

	def actualiser(self, temps):
		""" Actualise le niveau puis télécharge les informations du serveur ou
			des clients et envoie certains attributs.

			<temps> (float): Le temps en seconde depuis la dernière
				actualisation. """

		super().actualiser(temps)

		self.recevoir()
		self.envoyer()

	def envoyer(self):
		""" Ne fait rien ici. Cette méthode doit être redéfinie par les objets
			héritant de cette classe pour envoyer certaines données. """

		pass

	def recevoir(self):
		""" Ne fait rien ici. Cette méthode doit être redéfinie par les objets
			héritant de cette classe pour télécharger certaines données. """

		pass

	def importer(self, attributs):
		""" Ne fait rien ici. Cette méthode doit être redéfinie par les objets
			héritant de cette classe pour mettre à jour le niveau à partir
			d'un dictionnaire d'attributs.

			<attributs> (dict): Une dictionnaire contenant les nouvelles
				valeurs aux attributs du niveau. """

		pass

	def exporter(self):
		""" Renvoie un dictionnaire représentant le niveau. Seul les attributs
			essentiels doivent être retournés. Cette méthode renvoie un
			dictionnaire vide. Une surcharge est attendue. """

		return {}

	@staticmethod
	def creer_evenement(action):
		""" Renvoie un évènement pygame créé à partir d'un dictionnaire
			représentant une action effectuée par l'utilisateur. Cette méthode
			est statique.

			<action> (dict): Un dictionnaire représentant un évènement pygame. """

		t = action.get("type", pygame.USEREVENT)
		joueur_id = action.get("joueur_id", -1)
		details = {}

		if t in (pygame.KEYDOWN, pygame.KEYUP):
			details["key"] = action.get("touche", -1)

		elif t in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
			details["button"] = action.get("bouton", -1)

		elif t == pygame.MOUSEMOTION:
			details["pos"] = action.get("position", (0, 0))

		return pygame.event.Event(action.get("type"), details), joueur_id


class NiveauClient(NiveauReseau):
	""" Un niveau avec prise en charge réseau coté client. """

	def __init__(self, jeu, client):
		""" Initialise un niveau réseau coté client.

			<jeu> (jeu.Jeu): Le jeu auquel appartient ce niveau.
			<client> (reseau.Client): Le client à utiliser pour envoyer et
				recevoir les messages. """

		super().__init__(jeu)

		self.client = client

	def recevoir(self):
		""" Télécharge les messages du serveur et importe les attributs obtenu
			pour mettre à jour le niveau en le calquant sur celui du serveur. """

		message = self.client.recevoir()
		while message:
			self.importer(utile.charger_json(message.decode()))
			message = self.client.recevoir()

	def envoyer(self):
		""" Envoie une version simplifiée du niveau converti au format JSON. """

		niveau_formate = utile.formater_json(self.exporter())
		self.client.envoyer(niveau_formate.encode())
		self.actions.clear()

	def actualiser_evenement(self, evenement):
		""" Référence chaque évènement impactant le niveau dans la liste des
			actions. Actualise également le niveau avec l'évènement reçu comme
			avec un niveau sans prise en charge réseau.

			<evenement> (pygame.event.Event): L'évènement déclencheur. """

		super().actualiser_evenement(evenement)

		action = {}
		touches = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]

		# si l'utilisateur appui sur une touche du clavier...
		if evenement.type == pygame.KEYDOWN:
			if evenement.key in touches + [pygame.K_ESCAPE]:
				action["type"] = evenement.type
				action["touche"] = evenement.key
			if evenement.key == pygame.K_ESCAPE:
				action["joueur_id"] = -1

		# si l'utilisateur relache une touche du clavier...
		elif evenement.type == pygame.KEYUP:
			if evenement.key in touches:
				action["type"] = evenement.type
				action["touche"] = evenement.key

		# si il clique avec la souris
		elif evenement.type == pygame.MOUSEBUTTONDOWN:
			if evenement.button == 1:
				action["type"] = evenement.type
				action["bouton"] = evenement.button

		# si la souris bouge
		elif evenement.type == pygame.MOUSEMOTION:
			action["type"] = evenement.type
			action["position"] = list(evenement.pos)

		if action:
			if not "joueur_id" in action:
				action["joueur_id"] = self.joueur_id
			self.actions.append(action)

	def faire_apparaitre(self, temps):
		""" Ne fait plus rien. Le client ne s'occupe pas de faire apparaitre
			de nouvelles entités. """

		pass

	def quand_joueur_meurt(self, joueur):
		""" Si le joueur mort est le joueur local alors lance les fonctions de
			fin de partie (client). Sinon supprime simplement le joueur mort.

			<joueur> (entites.Joueur): Le joueur venant de mourir. """

		if joueur == self.obtenir_joueur_local():
			self.jeu.finir_partie_client()
		else:
			self.enlever_entite(joueur)

	def importer(self, attributs):
		""" Met à jour les attributs du niveau à partir d'un dictionnaire
			représentant une version simplifiée du niveau.

			<attributs> (dict): Le dictionnaire des attributs à importer. """

		self.pieces = attributs.get("pieces", self.pieces)
		self.temps_total = attributs.get("temps_total", self.temps_total)
		self.joueur_id = attributs.get("joueur_id", self.joueur_id)

		if self.en_pause != attributs.get("en_pause", self.en_pause):
			self.jeu.geler_partie(not self.en_pause)

		for attr_entite in attributs.get("entites", []):
			entite = self.obtenir_entite(attr_entite.get("identifiant", -1))

			if not entite:
				type_entite = attr_entite.get("TYPE", "Entite")
				classe_entite = Entite.obtenir_classe_entite(type_entite)
				nb_arguments = utile.obtenir_nb_args(classe_entite.__init__)
		
				entite = classe_entite(self, *([None] * (nb_arguments - 2)))
				entite.charger_image()
				self.ajouter_entite(entite)
		
			entite.importer(attr_entite)

	def exporter(self):
		""" Renvoie un dictionnaire contenant les actions à envoyer. """
		
		return {"actions": self.actions}


class NiveauServeur(NiveauReseau):
	""" Un niveau avec prise en charge réseau côté serveur. """

	def __init__(self, jeu, serveur):
		""" Initialise un niveau réseau coté serveur.

			<jeu> (jeu.Jeu): Le jeu auquel appartient ce niveau.
			<serveur> (reseau.Serveur): Le serveur à utiliser pour communiquer
				aux clients. """

		super().__init__(jeu)

		self.serveur = serveur

	def recevoir(self):
		""" Télécharge les messages des clients et prend en charge les
			évènements des autres joueurs. """

		messages = self.serveur.recevoir_broadcast()

		while messages:
			for message in messages.values():
				self.importer(utile.charger_json(message.decode()))
			messages = self.serveur.recevoir_broadcast()

	def envoyer(self):
		""" Envoie une version simplifiée du niveau au format JSON aux
			clients. """

		niveau_formate = utile.formater_json(self.exporter())
		self.serveur.envoyer_broadcast(niveau_formate.encode())
		self.actions.clear()

	def actualiser_evenement(self, evenement):
		""" Actualise le niveau avec un évènement donné puis référence ce
			dernier s'il permet de mettre en pause le niveau, afin de notifier
			plus tard les clients.

			<évènement> (pygame.event.Event): L'évènement déclencheur. """

		super().actualiser_evenement(evenement)

		if evenement.type == pygame.KEYDOWN:
			if evenement.key == pygame.K_ESCAPE:
				action = {"type": pygame.KEYDOWN, "touche": pygame.K_ESCAPE}
				self.actions.append(action)

	def definir_joueur(self, adresse, joueur):
		""" Envoie un nouvel identifiant de joueur local à un client donné.

			<adresse> (str): L'adresse du client concerné.
			<joueur> (entites.Joueur): Le joueur à associer au ce client. """

		formate = utile.formater_json({"joueur_id": joueur.identifiant})
		self.serveur.envoyer(adresse, formate.encode())

	def quand_joueur_meurt(self, joueur):
		""" Si le joueur mort est le joueur local alors lance les fonctions de
			fin de partie (serveur). Sinon supprime simplement le joueur mort.

			<joueur> (entites.Joueur): Le joueur venant de mourir. """

		if joueur == self.obtenir_joueur_local():
			self.jeu.finir_partie_serveur()
		else:
			self.enlever_entite(joueur)

	def importer(self, attributs):
		""" Applique les évènements reçus des clients aux joueurs de ce
			niveau.

			<attributs> (dict): Un dictionnaire contenant les actions
				effectuées par les autres joueurs. """

		actions = attributs.get("actions", [])

		for action in actions:
			evenement, joueur_id = self.creer_evenement(action)
			joueur = self.obtenir_entite(joueur_id)

			if joueur:
				self.commander_joueur(joueur, evenement)
			else:
				super().actualiser_evenement(evenement)

	def exporter(self):
		""" Renvoie un dictionnaire représentant une version simplifiée du
			niveau. """
			
		return {
			"entites": [entite.exporter() for entite in self.entites],
			"pieces": self.pieces,
			"temps_total": self.temps_total,
			"en_pause": self.en_pause
		}