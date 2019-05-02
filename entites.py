# -*- coding: utf-8 -*-

import constantes

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"

import math
import os
import pygame
import random


class Entite(object):
	"""
	Classe de base pour l'ensemble des entités.
	"""

	def __init__(self, niveau):
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
		affichage = self.niveau.affichage
		taille_pixel_x = int(self.taille[0] * constantes.ZOOM)
		taille_pixel_y = int(self.taille[1] * constantes.ZOOM)

		self.image = affichage.obtenir_image(chemin_image)
		self.image = pygame.transform.scale(self.image, (taille_pixel_x, taille_pixel_y))

	def charge_image(self):
		pass

	def actualise(self, temps):
		self.bouge(temps)

	def bouge(self, temps):
		# Un peu de trigonométrie...
		self.position[0] += self.vitesse * math.cos(self.angle) * temps
		# on soustrait la position car les coordonées de l'écran en pixels sont inversées
		# elles vont de haut en bas au lieu d'aller de bas en haut 
		self.position[1] -= self.vitesse * math.sin(self.angle) * temps

	def collisionne(self, entite):
		# on renvoie True si une entité déborde sur une autre
		if self.position[0] + self.taille[0] / 2 > entite.position[0] - entite.taille[0] / 2: 
			if self.position[0] - self.taille[0] / 2 < entite.position[0] + entite.taille[0] / 2:
				if self.position[1] + self.taille[1] / 2 > entite.position[1] - entite.taille[1] / 2: 
					if self.position[1] - self.taille[1] / 2 < entite.position[1] + entite.taille[1] / 2:
						return True
		return False

	def meurt(self):
		print("Une entité est morte")
		self.niveau.enleve_entite(self)


class Joueur(Entite):
	"""
	Classe définissant l'entité dirigée par le joueur.
	"""
	def __init__(self, niveau):
		super().__init__(niveau)
		self.vie = constantes.VIE_JOUEUR

		self.degat_tir = constantes.DEGAT_JOUEUR
		self.bouclier = False
		self.velocite = [0,0]
		self.vitesse = 1

		# cette variable permet de savoir si l'entité est en animation de dégat
		self.est_touche = False
		self.temps_animation_degat = 0

	def charge_image(self):
		self.__charge_image__(os.path.join("data", "images", "joueur", "joueur.png"))

	def charge_image_touche(self):
		self.__charge_image__(os.path.join("data", "images", "joueur", "joueur_touche.png"))

	def charge_image_bouclier(self):
		self.__charge_image__(os.path.join("data", "images", "joueur", "joueur_bouclier.png"))

	def regarde_position(self, dx, dy):
		""" Tourne le joueur de façon à ce qu'il regarde en direction de (dx, dy)"""
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
		super().actualise(temps)

		self.temps_animation_degat += temps

		# si l'animation a assez duré, on l'arrête et on recharge l'image par défaut du joueur
		if self.temps_animation_degat >= constantes.DUREE_ANIMATION_DEGAT:
			self.est_touche = False
			self.temps_animation_degat = 0
			self.charge_image()

		if self.vie <= 0:
			self.meurt()

	def tir(self):
		# on crée un tir
		tir = Tir(self.niveau, self)
		# on lui fait charge son image
		tir.charge_image()
		# on l'ajoute a la liste des entités du niveau
		self.niveau.entites.append(tir)

	def bouge(self, temps):
		# on redéfinit cette méthode pour changer les déplacements du joueur
		# il ne dépend plus de son angle de rotation
		self.position[0] += self.velocite[0] * temps * self.vitesse
		self.position[1] += self.velocite[1] * temps * self.vitesse

	def touche(self):
		self.est_touche = True

		# on change l'image du joueur pour qu'il ai l'image du joueur touché
		affichage = self.niveau.affichage
		taille_pixel_x = int(self.taille[0] * constantes.ZOOM)
		taille_pixel_y = int(self.taille[1] * constantes.ZOOM)

		self.image = affichage.obtenir_image(os.path.join("data", "images", "joueur", "joueur_touche.png"))
		self.image = pygame.transform.scale(self.image, (taille_pixel_x, taille_pixel_y))

	def haut(self):
		self.velocite[1] -= constantes.VITESSE_JOUEUR

	def bas(self):
		self.velocite[1] += constantes.VITESSE_JOUEUR

	def droite(self):
		self.velocite[0] += constantes.VITESSE_JOUEUR

	def gauche(self):
		self.velocite[0] -= constantes.VITESSE_JOUEUR

	def stop(self):
		self.velocite[0] = 0
		self.velocite[1] = 0

	def attaque(degat):
		pass

	def meurt(self):
		print("Le joueur est mort !")
		self.niveau.termine()


class Ennemi(Entite):
	"""
	Classe définissant une entité ennemie.
	"""

	def __init__(self, niveau):
		super().__init__(niveau)
		self.vitesse = constantes.VITESSE_ENNEMI
		self.degat_tir = constantes.DEGAT_ENNEMI
		self.vie = constantes.VIE_ENNEMI

		# cette variable permet de savoir si l'entité est en animation de dégat
		self.est_touche = False
		self.temps_animation_degat = 0

	def charge_image(self):
		self.__charge_image__(os.path.join("data", "images", "ennemi", "ennemi.png"))

	def charge_image_touche(self):
		self.__charge_image__(os.path.join("data", "images", "ennemi", "ennemi_touche.png"))

	def actualise(self, temps):
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
		if self.temps_animation_degat >= constantes.DUREE_ANIMATION_DEGAT:
			self.est_touche = False
			self.temps_animation_degat = 0
			self.charge_image()

		# si l'ennemi est trop près du joueur, on l'arrête
		if self.est_trop_pret():
			self.vitesse = 0
		else:
			# sinon... et ben il avance lol
			self.vitesse = constantes.VITESSE_ENNEMI

		if self.vie <= 0:
			self.meurt()

	def oriente(self):
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

	def touche(self):
		self.est_touche = True

		# on change l'image de l'ennemi pour qu'il est l'image d'un ennemi touché
		affichage = self.niveau.affichage
		taille_pixel_x = int(self.taille[0] * constantes.ZOOM)
		taille_pixel_y = int(self.taille[1] * constantes.ZOOM)

		self.image = affichage.obtenir_image(os.path.join("data", "images", "ennemi", "ennemi_touche.png"))
		self.image = pygame.transform.scale(self.image, (taille_pixel_x, taille_pixel_y))

	def tir(self):
		# on crée un tir
		tir = Tir(self.niveau, self)
		# on lui fait charge son image
		tir.charge_image()
		# on l'ajoute a la liste des entités du niveau
		self.niveau.entites.append(tir)

	def est_trop_pret(self):
		dx = self.position[0] - self.niveau.joueur.position[0]
		dy = self.position[1] - self.niveau.joueur.position[1]
		d = math.sqrt(dx ** 2 + dy ** 2)

		if d <= constantes.ZONE_AUTOUR_JOUEUR:
			return True
		else:
			return False

	def meurt(self):
		super().meurt()
		self.niveau.piece += constantes.PIECE_ENNEMI

	def doit_tirer(self, temps):
		nb = random.random()

		if nb <= temps / constantes.FREQUENCE_TIR_ENNEMI:
			return True
		return False


class Bonus(Entite):
	"""
	Classe définissant un bonus attrapable par le joueur.
	"""
	def __init__(self, niveau):
		super().__init__(niveau)
		# On choisi aléatoirement un bonus
		self.taille = constantes.TAILLE_BONUS
		self.type = random.choice(constantes.TYPE_BONUS)
		self.temps_vie = 0

	def charge_image(self):
		self.__charge_image__(os.path.join("data", "images", "bonus", self.type + ".png"))

	def actualise(self, temps):
		super().actualise(temps)

		self.temps_vie += temps

		if self.temps_vie >= constantes.DUREE_BONUS:
			self.meurt()

		if self.collisionne(self.niveau.joueur):
			self.attrape(self.niveau.joueur)

	def attrape(self, joueur):
		""" Cette methode doit ajouter une modification au joueur
			en fonction du type de bonus"""

		if self.type == "soin":
			joueur.vie += constantes.BONUS_SOIN

			if joueur.vie > constantes.VIE_JOUEUR:
				joueur.vie = constantes.VIE_JOUEUR

		elif self.type == "vitesse_augmentee":
			joueur.vitesse += constantes.BONUS_VITESSE

			if joueur.vitesse >= 4 * constantes.BONUS_VITESSE:
				joueur.vitesse = 4 * constantes.BONUS_VITESSE

		elif self.type == "arme_amelioree":
			joueur.degat_tir += constantes.BONUS_DEGAT

		self.meurt()


class Tir(Entite):
	"""
	Classe définissant un tir de missile.
	"""

	def __init__(self, niveau, tireur):
		super().__init__(niveau)
		self.tireur = tireur
		# on fait une copie de la position du joueur pour éviter les effets de bord
		self.position = self.tireur.position[:]
		self.angle = self.tireur.angle
		self.vitesse = constantes.VITESSE_TIR
		self.taille = constantes.TAILLE_TIR

		self.temps_vie = 0

	def charge_image(self):
		self.__charge_image__(os.path.join("data", "images", "tir", "tir.png"))
	
	def actualise(self, temps):
		super().actualise(temps)

		self.temps_vie += temps

		if self.temps_vie >= constantes.DUREE_TIR:
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
		"""Cette methode reduit la vie de entite"""
		entite.vie -= self.tireur.degat_tir
		entite.touche()
		self.meurt()