# -*- coding: utf-8 -*-

"""
	Contient les classes des différentes entités du jeu.
	Une entité est objet qui se détache du niveau, défini
	notamment par sa position et sa taille. Ces paramètres
	peuvent varier, ce qui permet de créer une impression de
	mouvement.
"""

import constantes

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"

import math
import os
import pygame
import random


class Entite(object):
	""" Classe de base pour l'ensemble des entités. """

	def __init__(self, niveau):
		""" Initialise l'entité.

			<niveau> (niveau.Niveau): Le niveau auquel appartient l'entité. """

		self.niveau = niveau
		self.taille = [1, 1]
		self.vitesse = 0
		self.angle = 0
		# la position est un point centré sur l'entité
		self.position = [0, 0]
		# on charge une image vide par défaut pour éviter les problèmes
		# comme ça, toutes les entités on une image par défaut
		self.image = niveau.affichage.obtenir_image("")

	def __charge_image__(self, chemin_image):
		""" Méthode interne utilisée pour simplifier le chargement et le
			redimensionnement d'une image donnée. 

			<chemin_image> (str): Le chemin de l'image. """

		affichage = self.niveau.affichage
		taille_pixel_x = int(self.taille[0] * constantes.General.ZOOM)
		taille_pixel_y = int(self.taille[1] * constantes.General.ZOOM)

		self.image = affichage.obtenir_image(chemin_image)
		self.image = pygame.transform.scale(self.image, (taille_pixel_x, taille_pixel_y))

	def charge_image(self):
		""" Appelé pour charger l'image de l'entité. Ne fait rien par défaut. """
		pass

	def actualise(self, temps):
		""" Actualise l'entité. Par défaut, cette méthode ne fait que bouger l'entité. 

			<temps> (float): Le temps écoulé en seconde depuis la dernière actualisation. """

		self.bouge(temps)

	def bouge(self, temps):
		""" Change la position de l'entité en fonction de sa vitesse et son angle de rotation.

			<temps> (float): Le temps écoulé en seconde depuis la dernière actualisation. """

		# Un peu de trigonométrie...
		self.position[0] += self.vitesse * math.cos(self.angle) * temps
		# on soustrait la position car les coordonées de l'écran en pixels sont inversées
		# elles vont de haut en bas au lieu d'aller de bas en haut 
		self.position[1] -= self.vitesse * math.sin(self.angle) * temps

	def collisionne(self, entite):
		""" Renvoie True si l'entité collisionne avec celle donnée, sinon False. 

			<entite> (entites.Entite): L'entité à tester. """

		# on renvoie True si une entité déborde sur une autre
		if self.position[0] + self.taille[0] / 2 > entite.position[0] - entite.taille[0] / 2: 
			if self.position[0] - self.taille[0] / 2 < entite.position[0] + entite.taille[0] / 2:
				if self.position[1] + self.taille[1] / 2 > entite.position[1] - entite.taille[1] / 2: 
					if self.position[1] - self.taille[1] / 2 < entite.position[1] + entite.taille[1] / 2:
						return True
		return False

	def meurt(self):
		""" Supprime cette entité du niveau, elle n'est donc plus actualisée et affichée.
			On peut donc considérer quelle est 'morte'. """

		self.niveau.enleve_entite(self)


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

		# cette variable permet de savoir si l'entité est en animation de dégat
		self.est_touche = False
		self.temps_animation_degat = 0

	def charge_image(self):
		""" Charge une image de joueur. """

		self.__charge_image__(constantes.Joueur.IMAGE)

	def charge_image_touche(self):
		""" Charge une image de joueur qui prend des dégats. """

		self.__charge_image__(constantes.Joueur.IMAGE_TOUCHE)

	def charge_image_bouclier(self):
		""" Charge une image de joueur avec un bouclier. (inutilisé) """

		self.__charge_image__(constantes.Joueur.IMAGE_BOUCLIER)

	def regarde_position(self, dx, dy):
		""" Tourne le joueur de façon à ce qu'il regarde en direction de (dx, dy). 

			<dx> (float): La distance horizontale entre le point à regarder et le joueur (positif 
				si le point se trouve à droite du joueur, sinon négatif).
			<dy> (float): La distance verticale entre le point à regarder et le joueur (positif 
				si le point se trouve en bas du joueur, sinon négatif). """

		# on calcule la distance entre le joueur et cette position à l'aide de Pythagore
		d = math.sqrt(dx ** 2 + dy ** 2)

		# si la souris est à une distance de 0 du joueur, on ne peut pas définir d'angle
		if d != 0:
			# on détermine un angle possible à l'aide de Arc cosinus
			angle = math.acos(dx / d)

			# on détermine si on doit prendre la valeur négative ou positive de cette angle
			if dy >= 0:
				self.angle = -angle
			else:
				self.angle = angle

	def actualise(self, temps):
		""" Actualise le joueur en mettant à jour le temps d'animation de dégat et en vérifiant
			que ses points de vie ne tombent pas en dessous de 0.

			<temps> (float): Le temps écoulé en seconde depuis la dernière actualisation. """

		super().actualise(temps)

		if self.est_touche:
			self.temps_animation_degat += temps

			# si l'animation a assez duré, on l'arrête et on recharge l'image par défaut du joueur
			if self.temps_animation_degat >= constantes.Joueur.DUREE_ANIMATION_DEGAT:
				self.est_touche = False
				self.charge_image()

		if self.vie <= 0:
			self.meurt()

	def tir(self):
		""" Crée un tir au niveau du joueur qui a le même angle de rotation que lui. """

		# on crée un tir
		tir = Tir(self.niveau, self)
		# on lui fait charge son image
		tir.charge_image()
		# on l'ajoute a la liste des entités du niveau
		self.niveau.entites.append(tir)

	def bouge(self, temps):
		""" Change la position du joueur en fonction du vecteur vélocité, du temps écoulé et de sa
			vitesse. 

			<temps> (float): Le temps écoulé en seconde depuis la dernière actualisation. """

		# on redéfinit cette méthode pour changer les déplacements du joueur
		# il ne dépend plus de son angle de rotation
		self.position[0] += self.velocite[0] * temps * self.vitesse
		self.position[1] += self.velocite[1] * temps * self.vitesse

	def attaque(self, degat):
		""" Réduit la vie du joueur et lance l'animation de dégat (le joueur devient rouge).

			<degat> (float): Les dégats reçus. """

		self.est_touche = True
		self.vie -= degat
		self.temps_animation_degat = 0
		self.charge_image_touche()

	def haut(self):
		""" Défini le vecteur vélocité pour que le joueur aille vers le haut. """

		self.velocite[1] -= constantes.Joueur.VITESSE

	def bas(self):
		""" Défini le vecteur vélocité pour que le joueur aille vers le bas. """

		self.velocite[1] += constantes.Joueur.VITESSE

	def droite(self):
		""" Défini le vecteur vélocité pour que le joueur aille vers la droite. """

		self.velocite[0] += constantes.Joueur.VITESSE

	def gauche(self):
		""" Défini le vecteur vélocité pour que le joueur aille vers la gauche. """

		self.velocite[0] -= constantes.Joueur.VITESSE

	def stop(self):
		""" Défini le vecteur vélocité pour que le joueur s'arrête. (obsolète) """

		self.velocite[0] = 0
		self.velocite[1] = 0

	def meurt(self):
		""" Arrête la partie """
		self.niveau.termine()


class Ennemi(Entite):
	""" Classe définissant une entité ennemie. """

	def __init__(self, niveau):
		""" Initialise un ennemi.

			<niveau> (niveau.Niveau): Le niveau auquel appartient l'ennemi. """

		super().__init__(niveau)
		self.vitesse = constantes.Ennemi.VITESSE
		self.vie = constantes.Ennemi.VIE

		# cette variable permet de savoir si l'entité est en animation de dégat
		self.est_touche = False
		self.temps_animation_degat = 0

	def charge_image(self):
		""" Charge une image d'ennemi. """

		self.__charge_image__(constantes.Ennemi.IMAGE)

	def charge_image_touche(self):
		""" Charge une image d'ennemi qui prend des dégats. """

		self.__charge_image__(constantes.Ennemi.IMAGE_TOUCHE)

	def actualise(self, temps):
		""" Actualise l'ennemi en mettant à jour le temps d'animation de dégat, en vérifiant
			que ses points de vie ne tombent pas en dessous de 0, en tirant de temps à autre
			et en vérifiant qu'il n'est pas trop prêt du joueur.

			<temps> (float): Le temps écoulé en seconde depuis la dernière actualisation. """

		super().actualise(temps)

		# l'ennemi s'oriente en direction du joueur
		self.oriente()
		
		# si l'ennemi doit tirer
		if self.doit_tirer(temps):
			# il le fait !!!
			self.tir()

		# si l'entité est touchée, on augmente le temps
		# qu'elle passe pendant son animation de touche
		if self.est_touche:
			self.temps_animation_degat += temps

			# si l'animation a assez duré, on l'arrête et on recharge l'image par défaut de l'ennemi
			if self.temps_animation_degat >= constantes.Ennemi.DUREE_ANIMATION_DEGAT:
				self.est_touche = False
				self.charge_image()

		# si l'ennemi est trop près du joueur, on l'arrête
		if self.est_trop_pres():
			self.vitesse = 0
		else:
			# sinon... et ben il avance lol
			self.vitesse = constantes.Ennemi.VITESSE

		if self.vie <= 0:
			self.meurt()

	def oriente(self):
		""" Change l'angle de rotation de l'ennemi de façon à ce qu'il regarde le joueur. """

		# on calcule la distance entre le joueur et l'ennemi
		dx = self.position[0] - self.niveau.joueur.position[0]
		dy = self.position[1] - self.niveau.joueur.position[1]
		d = math.sqrt(dx ** 2 + dy ** 2)

		# on divise la distance x par la distance totale
		# pour connaitre l'importance de la distance x
		# dans la distance totale (on aurait aussi pu le faire pour y)
		c = dx / d

		# on recupere l'un des deux angles associé à cette valeur de x
		# math.cos ne retourne que des angles compris entre 0 et pi
		angle = math.acos(c)

		# seul un angle est bon donc
		# on determine quelle valeur utiliser en fonction de y
		if dy >= 0:
			# si y > 0 alors on se trouve en haut du cercle trigonométrique
			# donc l'angle est entre 0 et pi
			self.angle = -angle + math.pi
		else:
			# si y < 0 alors on se trouve ne bas du cercle trigonométrique
			# donc l'angle est entre -pi et 0 (donc opposé)
			self.angle = angle + math.pi

	def attaque(self, degat):
		""" Réduit la vie de l'ennemi et lance l'animation de dégat (l'ennemi devient rouge).

			<degat> (float): Les dégats reçus. """

		self.est_touche = True
		self.vie -= degat
		self.temps_animation_degat = 0
		self.charge_image_touche()

	def tir(self):
		""" Crée un tir au niveau de l'ennemi qui a le même angle de rotation que lui. """

		# on crée un tir
		tir = Tir(self.niveau, self)
		# on lui fait charge son image
		tir.charge_image()
		# on l'ajoute a la liste des entités du niveau
		self.niveau.entites.append(tir)

	def est_trop_pres(self):
		""" Renvoie True si l'ennemi est trop prêt du joueur, sinon False. """

		dx = self.position[0] - self.niveau.joueur.position[0]
		dy = self.position[1] - self.niveau.joueur.position[1]
		d = math.sqrt(dx ** 2 + dy ** 2)

		if d <= constantes.Joueur.ZONE:
			return True
		else:
			return False

	def meurt(self):
		""" Augmente le nombre de pièces et meurt. """
		super().meurt()
		self.niveau.pieces += constantes.Ennemi.PIECE

	def doit_tirer(self, temps):
		""" Retourne True si il est temps de tirer, sinon False.

			<temps> (float): Le temps écoulé en seconde depuis la dernière actualisation. """

		nb = random.random()

		if nb <= temps / constantes.Ennemi.FREQUENCE_TIR:
			return True
		return False


class Bonus(Entite):
	"""
	Classe définissant un bonus attrapable par le joueur.
	"""
	def __init__(self, niveau):
		""" Initialise un bonus.

			<niveau> (niveau.Niveau): Le niveau auquel appartient le bonus. """

		super().__init__(niveau)
		# On choisi aléatoirement un bonus
		self.taille = constantes.Bonus.TAILLE
		self.type = random.choice(constantes.Bonus.TYPES)
		self.temps_vie = 0

	def charge_image(self):
		""" Charge une image de bonus en fonction du type de celui-ci. """

		self.__charge_image__(constantes.Bonus.IMAGE(self.type))

	def actualise(self, temps):
		""" Actualise le bonus en mettant à jour sa durée de vie et en cherchant si il entre
			en collision avec le joueur.

			<temps> (float): Le temps écoulé en seconde depuis la dernière actualisation. """

		super().actualise(temps)

		self.temps_vie += temps

		if self.temps_vie >= constantes.Bonus.DUREE:
			self.meurt()

		if self.collisionne(self.niveau.joueur):
			self.attrape(self.niveau.joueur)

	def attrape(self, joueur):
		""" Modifie certains attributs du joueur.

			<joueur> (entites.Joueur): Le joueur sur lequel s'applique le bonus. """

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

		self.meurt()


class Tir(Entite):
	"""
	Classe définissant un tir de missile.
	"""

	def __init__(self, niveau, tireur):
		""" Initialise un tir.

			<niveau> (niveau.Niveau): Le niveau auquel appartient le tir. """

		super().__init__(niveau)
		self.tireur = tireur
		# on fait une copie de la position du joueur pour éviter les effets de bord
		self.position = self.tireur.position[:]
		self.angle = self.tireur.angle
		self.vitesse = constantes.Tir.VITESSE
		self.taille = constantes.Tir.TAILLE

		self.temps_vie = 0

	def charge_image(self):
		""" Charge une image de tir. """

		self.__charge_image__(constantes.Tir.IMAGE)
	
	def actualise(self, temps):
		""" Actualise le tir en mettant à jour sa durée de vie et en cherchant si il entre
			en collision avec une entité.

			<temps> (float): Le temps écoulé en seconde depuis la dernière actualisation. """

		super().actualise(temps)

		self.temps_vie += temps

		if self.temps_vie >= constantes.Tir.DUREE:
			self.meurt()

		# si le tireur est un joueur
		if type(self.tireur) == Joueur:
			# on teste pour toutes les entités du niveau
			for entite in self.niveau.entites:
				# si le tir touche une entité
				if self.collisionne(entite):
					# et si est un ennemi (et pas un bonus ou encore un autre tir)
					if type(entite) == Ennemi:
						# alors on appelle la méthode touche()
						self.touche(entite)
		else:
			# sinon, c'est que le tir vient d'un ennemi
			# si le tir touche le joueur
			if self.collisionne(self.niveau.joueur):
				# alors on appelle la méthode touche()
				self.touche(self.niveau.joueur)

	def touche(self, entite):
		""" Attaque une entité puis meurt. 

			<entite> (entites.Ennemi ou entites.Joueur): Le joueur ou ennemi touché. """

		if type(entite) == Joueur:
			entite.attaque(constantes.Ennemi.DEGAT)
		else:
			entite.attaque(constantes.Joueur.DEGAT + self.niveau.joueur.degats_bonus)
		self.meurt()