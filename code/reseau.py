# -*- coding: utf-8 -*-

"""
	Contient des classes liées au communications réseau (type client / serveur).
"""

import socket as sckt
import threading


class Serveur(object):
	def __init__(self, jeu, port):
		self.jeu = jeu
		self.port = port
		self.socket = sckt.socket()
		self.en_activite = False
		self.clients = {}
		self.processus = threading.Thread(target=self.ecouter)

		self.socket.bind(("localhost", port))

	def ecouter(self):
		while self.en_activite:
			self.socket.listen()
			socket, (addresse, port) = self.socket.accept()

			if self.en_activite:
				self.connecter(addresse, socket)

	def lancer(self):
		self.en_activite = True
		self.processus.start()

	def arreter(self):
		for socket in self.clients.values():
			socket.close()

		self.en_activite = False
		sckt.socket().connect(("localhost", self.port))
		self.processus.join()

	def connecter(self, addresse, socket):
		self.clients[addresse] = socket
		self.jeu.ajouter_joueur(addresse)

	def deconnecter(self, addresse):
		self.clients[addresse].close()
		self.clients.pop(addresse)
		self.jeu.enlever_joueur(addresse)

	def envoyer(self, donnee, addresse):
		if not self.clients[addresse].send(donnee):
			self.deconnecter(addresse)

	def recevoir(self, addresse):
		donnee = self.clients[addresse].recv(4096)

		if not donnee:
			return self.deconnecter(addresse)
		return donnee


class Client(object):
	def __init__(self, jeu):
		self.jeu = jeu
		self.socket = sckt.socket()

	def connecter(self, addresse, port):
		self.socket.connect((addresse, port))

	def deconnecter(self):
		self.socket.close()

	def envoyer(self, donnee):
		if not self.socket.send(donnee):
			self.deconnecter()

	def recevoir(self):
		donnee = self.socket.recv(4096)

		if not donnee:
			return self.deconnecter()
		return donnee