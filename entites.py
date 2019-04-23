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
		self.position = [0, 0]
		self.image = None

	def charge_image(self, affichage):
		pass

	def actualise(self, temps):
		self.bouge(temps)

	def bouge(self, temps):
		# Un peu de trigonométrie...
		self.position[0] += self.vitesse * math.cos(self.angle) * temps
		self.position[1] += self.vitesse * math.sin(self.angle) * temps

	def collisionne(self, entite):
		if self.position[0] + self.taille[0] / 2 > entite.position[0] - entite.taille[0] / 2: 
			if self.position[0] - self.taille[0] / 2 < entite.position[0] + entite.taille[0] / 2:
				if self.position[1] + self.taille[1] / 2 > entite.position[1] - entite.taille[1] / 2: 
					if self.position[1] - self.taille[1] / 2 < entite.position[1] + entite.taille[1] / 2:
						return True
		return False

	def meurt(self, entite):
		del self.niveau.entite

class Joueur(Entite):
	"""
	Classe définissant l'entité dirigée par le joueur.
	"""
	def __init__(self, niveau):
		super().__init__(niveau)
		self.vie = constantes.VIE_JOUEUR

	def charge_image(self, affichage):
		taille_pixel_x = self.taille[0] * constantes.ZOOM
		taille_pixel_y = self.taille[1] * constantes.ZOOM

		self.image = affichage.obtenir_image(os.path.join("data", "images", "joueur", "joueur_0.png"))
		self.image = pygame.transform.scale(self.image, (taille_pixel_x, taille_pixel_y))

	def tir(self):
		self.niveau.entites.append(Tir())

	def avance(self):
		self.vitesse = constantes.VITESSE_JOUEUR

	def recule(self):
		self.vitesse = -constantes.VITESSE_JOUEUR

	def stop(self):
		self.vitesse = 0


class Ennemi(Entite):
	"""
	Classe définissant une entité ennemie.
	"""

	def __init__(self, niveau):
		super().__init__(niveau)
		self.vitesse = constantes.VITESSE_ENNEMI
		self.vie = constantes.VIE_ENNEMI

	def charge_image(self, affichage):
		""" A implementer...
			Cette méthode doit charger la texture de l'ennemi
			et la redimensionner à la bonne taille (en prenant en compte le zoom)"""
		taille_pixel_x = self.taille[0] * constantes.ZOOM
		taille_pixel_y = self.taille[1] * constantes.ZOOM

		self.image = affichage.obtenir_image(os.path.join("data", "images", "ennemi", "ennemi.png"))
		self.image = pygame.transform.scale(self.image, (taille_pixel_x, taille_pixel_y))

	def actualise(self, temps):
		super().actualise(temps)
		self.oriente()
		if self.est_trop_pret() == True:
			self.vitesse = 0

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
			self.angle = angle + math.pi
		else:
			# si y < 0 alors on se trouve ne bas du cercle trigonométrique
			# donc l'angle est entre -pi et 0 (donc opposé)
			self.angle = -angle + math.pi

	def tir(self):
		self.niveau.entites.append(Tir())

	def est_trop_pret(self):
		dx = self.position[0] - self.niveau.joueur.position[0]
		dy = self.position[1] - self.niveau.joueur.position[1]
		d = math.sqrt(dx ** 2 + dy ** 2)

		if d <= constantes.ZONE_AUTOUR_JOUEUR:
			return True
		else:
			return False


class Bonus(Entite):
	"""
	Classe définissant un bonus attrapable par le joueur.
	"""
	def __init__(self, niveau):
		super().__init__(niveau)
		# On choisi aléatoirement un bonus
		self.type = random.choice(constantes.TYPE_BONUS)

	def charge_image(self, affichage):
		""" A implementer...
			Cette méthode doit charger la texture du bonus (et du bon bonus)
			et la redimensionner à la bonne taille (en prenant en compte le zoom)"""

		taille_pixel_x = self.taille[0] * constantes.ZOOM
		taille_pixel_y = self.taille[1] * constantes.ZOOM

		self.image = affichage.obtenir_image(os.path.join("data", "images", "bonus", self.type))
		self.image = pygame.transform.scale(self.image, (taille_pixel_x, taille_pixel_y))

	def actualise(self, temps):
		super().actualise(temps)
		
		# il y a un probleme ici coco, car "entite" n'est pas defini.
		# il faut tester si le bonus collisionne avec le joueur
		if collisionne(entite) == True:
			self.attrape()

	def attrape(self):
		""" A implementer...
			Cette methode doit ajouter une modification au joueur
			en fonction du type de bonus"""
		if self.type == "soin" and self.niveau.joueur.vie < VIE_JOUEUR//2:
			self.niveau.joueur.vie += VIE_JOUEUR//2
		
		elif self.type == "soin" and self.niveau.joueur.vie >= VIE_JOUEUR//2:
			self.niveau.joueur.vie = VIE_JOUEUR

class Tir(Entite):
	"""
	Classe définissant un tir de missile.
	"""

	def actualise(self, temps):
		super().actualise(temps)
		"""Cette methode doit tester si le tir entre en collision
			avec un ennemi ou le joueur et appeler Tir.touche si c'est le cas"""

		if self.collisionne(self.niveau.joueur):
			self.touche(self.niveau.joueur)

	def touche(self, entite):
		"""Cette methode doit reduire la vie de entite"""
		entite.vie -= constantes.DEGAT_TIR