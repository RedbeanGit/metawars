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
	Contient les classes des différentes entités du jeu. Une entité est objet
	qui se détache du niveau, défini notamment par sa position et sa taille.
	Ces paramètres peuvent varier, ce qui permet de créer une impression de
	mouvement.
"""

import math
import os
import random

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"

import constantes
import utile


class Entite(object):
	""" Classe de base pour l'ensemble des entités. """
	
	nb_entites = 0

	def __init__(self, niveau):
		""" Initialise l'entité.

			<niveau> (niveau.Niveau): Le niveau auquel appartient l'entité. """

		self.identifiant = Entite.nb_entites
		self.niveau = niveau
		self.taille = [1, 1]
		self.vitesse = 0
		self.angle = 0
		self.position = [0, 0]
		self.sprite = niveau.jeu.affichage.obtenir_sprite("")

		Entite.nb_entites += 1

	def __charger_sprite__(self, chemin_image):
		""" Méthode interne utilisée pour simplifier le chargement et le
			redimensionnement d'une image donnée.

			<chemin_image> (str): Le chemin de l'image. """

		affichage = self.niveau.jeu.affichage
		self.sprite = affichage.obtenir_sprite(chemin_image)
		self.sprite.batch = affichage.batch_entites

		image = self.sprite.image
		image.anchor_x = image.width / 2
		image.anchor_y = image.height / 2
		
	def charger_sprite(self):
		""" Appelé pour charger l'image de l'entité. Ne fait rien par défaut. """
		pass

	def actualiser(self, temps):
		""" Actualise l'entité. Par défaut, cette méthode ne fait que bouger
			l'entité. 

			<temps> (float): Le temps écoulé en seconde depuis la dernière
				actualisation. """

		self.bouger(temps)

	def bouger(self, temps):
		""" Change la position de l'entité en fonction de sa vitesse et son
			angle de rotation.

			<temps> (float): Le temps écoulé en seconde depuis la dernière
				actualisation. """

		self.position[0] += self.vitesse * math.cos(self.angle) * temps
		self.position[1] -= self.vitesse * math.sin(self.angle) * temps

	def en_collision(self, entite):
		""" Renvoie True si l'entité collisionne avec celle donnée, sinon
			False.

			<entite> (entites.Entite): L'entité à tester. """

		if entite != self:
			x1, y1 = self.position
			l1, h1 = self.taille

			x2, y2 = entite.position
			l2, h2 = entite.taille

			if x1 + l1 / 2 > x2 - l2 / 2:
				if x1 - l1 / 2 < x2 + l2 / 2:
					if y1 + h1 / 2 > y2 - h2 / 2:
						if y1 - h1 / 2 < y2 + h2 / 2:
							return True
		return False

	def calculer_distance(self, entite):
		""" Renvoie la distance directe entre cette entité et une autre.

			<entite> (entites.Entite): L'entité à évaluer. """

		dx = abs(entite.position[0] - self.position[0])
		dy = abs(entite.position[1] - self.position[1])

		return math.sqrt(dx**2 + dy**2)

	def mourir(self):
		""" Supprime cette entité du niveau, elle n'est donc plus actualisée
			et affichée. On peut donc considérer quelle est 'morte'. """

		self.niveau.enlever_entite(self)

	def exporter(self):
		""" Renvoie un dictionnaire des attributs de l'entité. Une surcharge
			de cette méthode est attendue. """

		return {
			"TYPE": "Entite",
			"identifiant": self.identifiant,
			"taille": self.taille,
			"vitesse": self.vitesse,
			"angle": self.angle,
			"position": self.position
		}

	def importer(self, attributs):
		""" Met à jour les attributs de l'entité à partir d'un dictionnaire
			d'attributs. Une surcharge de cette méthode est attendue.

			<attributs> (dict): Dictionnaire au format {nom_attribut1: 
				valeur1, nom_attribut2: valeur2, ...}. """

		self.identifiant = attributs.get("identifiant", 0)
		self.taille = attributs.get("taille", [1, 1])
		self.vitesse = attributs.get("vitesse", 0)
		self.angle = attributs.get("angle", 0)
		self.position = attributs.get("position", [0, 0])

	def nettoyer(self):
		self.sprite.delete()

	@classmethod
	def obtenir_classe_entite(cls, nom_classe):
		""" Retourne la classe d'entité correspondante à un nom donné. Si
			aucune classe portant ce nom n'est trouvée, renvoie la classe
			'entites.Entite'.

			<nom_classe> (str): Nom de la classe d'entité. """

		classe = utile.obtenir_classe(cls.__module__, nom_classe)

		if classe:
			return classe
		return Entite


class Joueur(Entite):
	""" Classe définissant l'entité dirigée par le joueur. """

	def __init__(self, niveau):
		""" Initialise un joueur.

			<niveau> (niveau.Niveau): Le niveau auquel appartient le joueur. """

		super().__init__(niveau)
		self.vie = constantes.Joueur.VIE

		self.degats_bonus = 0
		self.bouclier = False
		self.velocite = [0, 0]
		self.vitesse = 1

		self.est_touche = False
		self.temps_animation_degat = 0

	def charger_sprite(self):
		""" Charge une image de joueur. """

		self.__charger_sprite__(constantes.Joueur.IMAGE)

	def charger_sprite_touche(self):
		""" Charge une image de joueur qui prend des dégats. """

		self.__charger_sprite__(constantes.Joueur.IMAGE_TOUCHE)

	def charger_sprite_bouclier(self):
		""" Charge une image de joueur avec un bouclier. (inutilisé) """

		self.__charger_sprite__(constantes.Joueur.IMAGE_BOUCLIER)

	def regarder_position(self, dx, dy):
		""" Tourne le joueur de façon à ce qu'il regarde en direction de
			(dx, dy).

			<dx> (float): La distance horizontale entre le point à regarder et
				le joueur (positif si le point se trouve à droite du joueur,
				sinon négatif).
			<dy> (float): La distance verticale entre le point à regarder et
				le joueur (positif si le point se trouve en bas du joueur,
				sinon négatif). """

		d = math.sqrt(dx ** 2 + dy ** 2)

		if d != 0:
			angle = math.acos(dx / d)

			if dy >= 0:
				self.angle = -angle
			else:
				self.angle = angle

	def actualiser(self, temps):
		""" Actualise le joueur en mettant à jour le temps d'animation de
			dégat et en vérifiant que ses points de vie ne tombent pas en
			dessous de 0.

			<temps> (float): Le temps écoulé en seconde depuis la dernière
				actualisation. """

		super().actualiser(temps)

		if self.est_touche:
			self.temps_animation_degat += temps

			duree_max = constantes.Joueur.DUREE_ANIMATION_DEGAT
			if self.temps_animation_degat >= duree_max:
				self.est_touche = False
				self.charger_sprite()

		if self.vie <= 0:
			self.mourir()

	def tirer(self):
		""" Crée un tir au niveau du joueur qui a le même angle de rotation
			que lui. """

		tir = Tir(self.niveau, self)
		tir.charger_sprite()
		self.niveau.ajouter_entite(tir)

	def bouger(self, temps):
		""" Change la position du joueur en fonction du vecteur vélocité, du
			temps écoulé et de sa vitesse.

			<temps> (float): Le temps écoulé en seconde depuis la dernière
				actualisation. """

		self.position[0] += self.velocite[0] * temps * self.vitesse
		self.position[1] += self.velocite[1] * temps * self.vitesse

	def blesser(self, degat):
		""" Réduit la vie du joueur et lance l'animation de dégat (le joueur
			devient rouge).

			<degat> (float): Les dégats reçus. """

		self.est_touche = True
		self.vie -= degat
		self.temps_animation_degat = 0
		self.charger_sprite_touche()

	def attaquer(self, entite):
		""" Blesse une entité en prenant en compte les dégats bonus du joueur.

			<entite> (entites.Entite): L'entité à attaquer. """
			
		entite.blesser(constantes.Joueur.DEGAT + self.degats_bonus)

	def haut(self):
		""" Défini le vecteur vélocité pour que le joueur aille vers le haut. """

		self.velocite[1] += constantes.Joueur.VITESSE

	def bas(self):
		""" Défini le vecteur vélocité pour que le joueur aille vers le bas. """

		self.velocite[1] -= constantes.Joueur.VITESSE

	def droite(self):
		""" Défini le vecteur vélocité pour que le joueur aille vers la droite. """

		self.velocite[0] += constantes.Joueur.VITESSE

	def gauche(self):
		""" Défini le vecteur vélocité pour que le joueur aille vers la gauche. """

		self.velocite[0] -= constantes.Joueur.VITESSE

	def mourir(self):
		""" Avertit le niveau que le joueur et est mort. """

		self.niveau.quand_joueur_meurt(self)

	def exporter(self):
		""" Renvoie un dictionnaire des attributs de ce joueur. """

		attributs = super().exporter()
		attributs.update({
			"TYPE": "Joueur",
			"vie": self.vie,
			"degats_bonus": self.degats_bonus,
			"bouclier": self.bouclier,
			"velocite": self.velocite,
			"est_touche": self.est_touche,
			"temps_animation_degat": self.temps_animation_degat
		})
		
		return attributs

	def importer(self, attributs):
		""" Met à jour les attributs du joueur à partir d'un dictionnaire 
			d'attributs.

			<attributs> (dict): Dictionnaire au format {nom_attribut1: 
				valeur1, nom_attribut2: valeur2, ...}. """

		super().importer(attributs)

		self.vie = attributs.get("vie", 0)
		self.degats_bonus = attributs.get("degats_bonus", 0)
		self.bouclier = attributs.get("bouclier", False)
		self.velocite = attributs.get("velocite", False)
		self.est_touche = attributs.get("est_touche", False)
		self.temps_animation_degat = attributs.get("temps_animation_degat", 0)


class Ennemi(Entite):
	""" Classe définissant une entité ennemie des joueurs. """

	def __init__(self, niveau):
		""" Initialise un ennemi.

			<niveau> (niveau.Niveau): Le niveau auquel appartient l'ennemi. """

		super().__init__(niveau)
		self.vitesse = constantes.Ennemi.VITESSE
		self.vie = constantes.Ennemi.VIE
		self.est_touche = False
		self.temps_animation_degat = 0

	def charger_sprite(self):
		""" Charge une image d'ennemi. """

		self.__charger_sprite__(constantes.Ennemi.IMAGE)

	def charger_sprite_touche(self):
		""" Charge une image d'ennemi qui prend des dégats. """

		self.__charger_sprite__(constantes.Ennemi.IMAGE_TOUCHE)

	def actualiser(self, temps):
		""" Actualise l'ennemi en mettant à jour le temps d'animation de
			dégat, en vérifiant que ses points de vie ne tombent pas en
			dessous de 0, en tirant de temps à autre et en vérifiant qu'il
			n'est pas trop prêt du joueur.

			<temps> (float): Le temps écoulé en seconde depuis la dernière
				actualisation. """

		joueur = self.trouver_joueur_proche()
		
		if joueur:
			super().actualiser(temps)
			self.orienter(joueur)
		
		if self.doit_tirer(temps):
			self.tirer()

		if self.est_touche:
			self.temps_animation_degat += temps

			if self.temps_animation_degat >= constantes.Ennemi.DUREE_ANIMATION_DEGAT:
				self.est_touche = False
				self.charger_sprite()

		if self.est_trop_pres():
			self.vitesse = 0
		else:
			self.vitesse = constantes.Ennemi.VITESSE

		if self.vie <= 0:
			self.mourir()

	def trouver_joueur_proche(self):
		""" Renvoie le joueur le plus proche ou None si aucun joueur n'est
			trouvé. """

		def classer_entite(entite):
			if isinstance(entite, Joueur):
				return self.calculer_distance(entite)
			return float("inf")

		proche = min(self.niveau.entites, key=classer_entite)

		if isinstance(proche, Joueur):
			return proche
		return None

	def orienter(self, joueur):
		""" Change l'angle de rotation de l'ennemi de façon à ce qu'il regarde
			le joueur.

			<joueur> (entites.Joueur): Le joueur vers lequel orienter
				l'ennemi. """

		dx = self.position[0] - joueur.position[0]
		dy = self.position[1] - joueur.position[1]
		d = math.sqrt(dx ** 2 + dy ** 2)
		
		if d:
			c = dx / d

			angle = math.acos(c)

			if dy >= 0:
				self.angle = -angle + math.pi
			else:
				self.angle = angle + math.pi

	def blesser(self, degat):
		""" Réduit la vie de l'ennemi et lance l'animation de dégat (l'ennemi
			devient rouge).

			<degat> (float): Les dégats reçus. """

		self.est_touche = True
		self.vie -= degat
		self.temps_animation_degat = 0
		self.charger_sprite_touche()

	def attaquer(self, entite):
		""" Inflige des dégâts à une entité donnée.

			<entite> (entites.Entite): L'entité à attaquer. """

		entite.blesser(constantes.Ennemi.DEGAT)

	def tirer(self):
		""" Crée un tir au niveau de l'ennemi qui a le même angle de rotation
			que lui. """

		tir = Tir(self.niveau, self)
		tir.charger_sprite()
		self.niveau.entites.append(tir)

	def est_trop_pres(self):
		""" Renvoie True si l'ennemi est trop prêt du joueur, sinon False. """

		for entite in self.niveau.entites:
			if type(entite) == Joueur:
				if self.calculer_distance(entite) <= constantes.Joueur.ZONE:
					return True
		return False

	def mourir(self):
		""" Augmente le nombre de pièces et meurt. """

		super().mourir()
		self.niveau.pieces += constantes.Ennemi.PIECE

	def doit_tirer(self, temps):
		""" Retourne True si il est temps de tirer, sinon False.

			<temps> (float): Le temps écoulé en seconde depuis la dernière
				actualisation. """

		nb = random.random()

		if nb <= temps / constantes.Ennemi.FREQUENCE_TIR:
			return True
		return False

	def exporter(self):
		""" Renvoie un dictionnaire des attributs de cet Ennemi. """

		attributs = super().exporter()
		attributs.update({
			"TYPE": "Ennemi",
			"vie": self.vie,
			"est_touche": self.est_touche,
			"temps_animation_degat": self.temps_animation_degat
		})
		
		return attributs

	def importer(self, attributs):
		""" Met à jour les attributs de l'Ennemi à partir d'un dictionnaire
			d'attributs.

			<attributs> (dict): Dictionnaire au format {nom_attribut1: 
				valeur1, nom_attribut2: valeur2, ...}. """

		super().importer(attributs)

		self.vie = attributs.get("vie", 0)
		self.est_touche = attributs.get("est_touche", False)
		self.temps_animation_degat = attributs.get("temps_animation_degat", 0)


class Bonus(Entite):
	""" Classe définissant un bonus attrapable par le joueur. """

	def __init__(self, niveau):
		""" Initialise un bonus.

			<niveau> (niveau.Niveau): Le niveau auquel appartient le bonus. """

		super().__init__(niveau)
		
		self.taille = constantes.Bonus.TAILLE
		self.type = random.choice(constantes.Bonus.TYPES)
		self.temps_vie = 0

	def charger_sprite(self):
		""" Charge une image de bonus en fonction du type de celui-ci. """

		self.__charger_sprite__(constantes.Bonus.IMAGE(self.type))

	def actualiser(self, temps):
		""" Actualise le bonus en mettant à jour sa durée de vie et en
			cherchant si il entre en collision avec le joueur.

			<temps> (float): Le temps écoulé en seconde depuis la dernière
				actualisation. """

		super().actualiser(temps)

		self.temps_vie += temps

		if self.temps_vie >= constantes.Bonus.DUREE:
			self.mourir()

		for entite in self.niveau.entites:
			if self.en_collision(entite) and type(entite) == Joueur:
				self.attraper(entite)
				break

	def attraper(self, joueur):
		""" Modifie certains attributs du joueur.

			<joueur> (entites.Joueur): Le joueur sur lequel s'applique le
				bonus. """

		if self.type == "soin":
			joueur.vie += constantes.Bonus.SOIN

			if joueur.vie > constantes.Joueur.VIE:
				joueur.vie = constantes.Joueur.VIE

		elif self.type == "vitesse_augmentee":
			joueur.vitesse += constantes.Bonus.VITESSE

			if joueur.vitesse >= 4 * constantes.Bonus.VITESSE + 1:
				joueur.vitesse = 4 * constantes.Bonus.VITESSE + 1

		elif self.type == "arme_amelioree":
			joueur.degats_bonus += constantes.Bonus.DEGAT

		self.mourir()

	def exporter(self):
		""" Renvoie un dictionnaire des attributs de ce bonus. """

		attributs = super().exporter()
		attributs.update({
			"TYPE": "Bonus",
			"type": self.type,
			"temps_vie": self.temps_vie
		})
		
		return attributs

	def importer(self, attributs):
		""" Met à jour les attributs du bonus à partir d'un dictionnaire 
			d'attributs.

			<attributs> (dict): Dictionnaire au format {nom_attribut1: 
				valeur1, nom_attribut2: valeur2, ...}. """

		super().importer(attributs)

		self.type = attributs.get("type", constantes.Bonus.TYPES[0])
		self.temps_vie = attributs.get("temps_vie", 0)


class Tir(Entite):
	""" Classe définissant un tir de missile. """

	def __init__(self, niveau, tireur=None):
		""" Initialise un tir.

			<niveau> (niveau.Niveau): Le niveau auquel appartient le Tir.
			[tireur] (entite.Entite): L'entité à l'origine de ce Tir. None
				par défaut. """

		super().__init__(niveau)
		self.tireur = tireur
		
		if self.tireur:
			self.position = self.tireur.position[:]
			self.angle = self.tireur.angle
		
		self.vitesse = constantes.Tir.VITESSE
		self.taille = constantes.Tir.TAILLE

		self.temps_vie = 0

	def charger_sprite(self):
		""" Charge une image de tir. """

		self.__charger_sprite__(constantes.Tir.IMAGE)
	
	def actualiser(self, temps):
		""" Actualise le tir en mettant à jour sa durée de vie et en cherchant
			si il entre en collision avec une entité.

			<temps> (float): Le temps écoulé en seconde depuis la dernière
				actualisation. """

		super().actualiser(temps)

		self.temps_vie += temps

		if self.temps_vie >= constantes.Tir.DUREE:
			self.mourir()

		for entite in self.niveau.entites:
			if self.en_collision(entite):
				self.toucher(entite)

	def blesser(self, degat):
		""" Si une entité attaque ce Tir, il meurt instantanément. """

		self.mourir()

	def toucher(self, entite):
		""" Attaque une entité puis meurt.

			<entite> (entites.Ennemi ou entites.Joueur): Le joueur ou ennemi
				touché. """

		if not isinstance(entite, Bonus) and entite != self.tireur:
			if isinstance(self.tireur, Ennemi):
				if isinstance(entite, Joueur):
					self.tireur.attaquer(entite)

			elif self.tireur:
				self.tireur.attaquer(entite)
			self.mourir()

	def exporter(self):
		""" Renvoie un dictionnaire des attributs de ce tir. """

		attributs = super().exporter()
		attributs.update({
			"TYPE": "Tir",
			"tireur": self.tireur.identifiant,
			"temps_vie": self.temps_vie
		})
		
		return attributs

	def importer(self, attributs):
		""" Met à jour les attributs du tir à partir d'un dictionnaire
			d'attributs.

			<attributs> (dict): Dictionnaire au format {nom_attribut1: 
				valeur1, nom_attribut2: valeur2, ...}. """

		super().importer(attributs)

		self.tireur = self.niveau.obtenir_entite(attributs.get("tireur", 0))
		self.temps_vie = attributs.get("temps_vie", 0)