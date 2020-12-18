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
	Contient des classes liées au communications réseau (type client / serveur).
"""

import errno
import select
import socket as sckt
import threading
import time

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"

import utile


class Tampon(object):
	""" Stocke les messages en séparant ceux en cours de réception et ceux
		complètement téléchargés. """

	def __init__(self, socket):
		""" Initialise un tampon sur un socket donné.

			<socket> (socket.socket): Le socket à utiliser pour envoyer et
				recevoir les messages. """

		self.socket = socket

		self.message = bytes()
		self.entete = bytes()
		self.taille_message = 0
		self.taille_entete = 2
		
		self.messages_reception = []
		self.messages_envoi = bytes()

	def fileno(self):
		""" Renvoie le numéro de fichier du socket. Cette méthode est utilisée
			pour savoir si le socket est prêt à être lu ou écrit. """

		return self.socket.fileno()

	def envoyer(self):
		""" Envoie les messages stockés jusqu'à ce que le socket soit plein ou
			qu'il n'y ait plus de messages à envoyer. """

		if self.messages_envoi:
			try:
				envoye = self.socket.send(self.messages_envoi)
				self.messages_envoi = self.messages_envoi[envoye:]
			except sckt.error as erreur:
				return erreur.errno == errno.EAGAIN
			except sckt.timeout:
				return True
		return True

	def recevoir(self):
		""" Lit le socket et complète le message en cours. Une fois fini, lit
			le message suivant et ainsi de suite. La taille d'un message est
			déterminée à partir des deux premiers octets reçus. """

		message_brute = bytes()

		try:
			message_brute = self.socket.recv(2048)
		except sckt.timeout:
			pass
		except sckt.error as erreur:
			if erreur.errno != errno.EAGAIN:
				return False
		
		for indice in range(len(message_brute)):
			caractere = message_brute[indice:indice+1]

			if self.taille_entete:
				self.entete += caractere
				self.taille_entete -= 1

				if not self.taille_entete:
					self.taille_message = int.from_bytes(self.entete, "big")
			
			elif self.taille_message:
				self.message += caractere
				self.taille_message -= 1

				if not self.taille_message:
					self.messages_reception.append(self.message)
					self.message = bytes()
					self.entete = bytes()
					self.taille_message = 0
					self.taille_entete = 2
		return True

	def lire(self):
		""" Renvoie le message complètement reçu le plus ancien puis le
			supprime du tampon. Si ce tampon ne contient aucun message,
			renvoie un bytes vide. """

		if self.messages_reception:
			return self.messages_reception.pop(0)
		return bytes()

	def ecrire(self, message):
		""" Ajoute un message et son entête au tampon. L'entête représente la
			taille du message et est stockée sur les deux premiers octets.

			<message> (bytes): Le message à envoyer. """
			
		self.messages_envoi += len(message).to_bytes(2, "big") + message


class Serveur(object):
	""" Accepte les connexions entrantes et échange avec les clients par
		l'intermédiaire de tampons. """

	def __init__(self, jeu, port):
		""" Initialise un serveur.

			<jeu> (jeu.Jeu): Le jeu auquel appartient ce serveur.
			<port> (int): Le port sur lequel doit écouter ce serveur. """

		self.jeu = jeu
		self.port = port
		self.socket = sckt.socket()
		self.tampons = {}

		self.connecte = False
		self.activite_ecoute = False
		self.activite_echange = False
		
		self.fil_ecoute = threading.Thread(target=self.ecouter)
		self.fil_echange = threading.Thread(target=self.echanger)

	def __bool__(self):
		""" Renvoie True si le serveur est lié à un port, qu'il est en écoute
			ou qu'il est en échange. Sinon False. """

		return self.connecte or self.activite_ecoute or self.activite_echange

	def accrocher(self):
		""" Lie le serveur à un port. Si le port est inaccessible renvoie
			False, sinon True. """

		try:
			self.socket.bind(("localhost", self.port))
		except sckt.error:
			utile.debogguer("Impossible d'écouter sur le port " + str(self.port), 1)
			return False
		else:
			self.connecte = True
			return True

	def ecouter(self):
		""" Ecoute en continu sur le port du serveur pour accepter les
			connexions entrantes. """

		self.socket.listen()

		while self.activite_ecoute:
			try:
				socket, (adresse, port) = self.socket.accept()
			except OSError:
				utile.debogguer("Impossible d'accepter une nouvelle " \
					+ "connexion: socket fermé", 1)

			if self.activite_ecoute:
				self.connecter(adresse, socket)

	def echanger(self):
		""" Echange en continu avec les clients. """

		while self.activite_echange:
			tampons = self.tampons.values()

			if tampons:
				lisibles, ecrivables, _ = select.select(tampons, tampons, [])

				for tampon in ecrivables:
					if not tampon.envoyer():
						adresse = self.obtenir_adresse_tampon(tampon)
						self.deconnecter(adresse)

				for tampon in lisibles:
					if tampon in self.tampons.values():
						if not tampon.recevoir():
							adresse = self.obtenir_adresse_tampon(tampon)
							self.deconnecter(adresse)
			else:
				time.sleep(1)

	def lancer_ecoute(self):
		""" Lance un fil d'execution (thread) dédié aux écoutes (accepte les
			connexions entrantes). """

		if not self.activite_ecoute:
			utile.debogguer("Lancement d'une boucle d'écoute (serveur)")
			self.activite_ecoute = True
			self.fil_ecoute.start()
		
	def lancer_echange(self):
		""" Lance un fil d'execution (thread) dédié aux échanges. """

		if not self.activite_echange:
			utile.debogguer("Lancement d'une boucle d'échange (serveur)")
			self.activite_echange = True
			self.fil_echange.start()

	def arreter_ecoute(self):
		""" Stoppe la boucle d'écoute et le fil d'execution dédié. """

		if self.activite_ecoute:
			utile.debogguer("Arrêt d'une boucle d'écoute (serveur)")
			self.activite_ecoute = False

			sckt.socket().connect(("localhost", self.port))
			self.socket.close()
			self.fil_ecoute.join()

	def arreter_echange(self):
		""" Stoppe la boucle d'échange et le fil d'execution dédié. """

		if self.activite_echange:
			utile.debogguer("Arrêt d'une boucle d'échange (serveur)")
			self.activite_echange = False
			self.fil_echange.join()
			
			for adresse in list(self.tampons):
				self.deconnecter(adresse)

	def obtenir_adresse_tampon(self, tampon):
		""" Renvoie l'adresse du client associé à un tampon donné.

			<tampon> (reseau.Tampon): Le tampon dont l'adresse est à
				déterminer. """

		for adresse, tampon_cours in list(self.tampons.items()):
			if tampon_cours == tampon:
				return adresse
		return None

	def connecter(self, adresse, socket):
		""" Ajoute un client et crée un nouveau tampon associé.

			<adresse> (str): L'adresse du nouveau client.
			<socket> (str): Le socket associé. """

		socket.settimeout(0.1)
		self.tampons[adresse] = Tampon(socket)
		self.jeu.ajouter_client(adresse)

	def deconnecter(self, adresse):
		""" Ferme le socket associé à une adresse donnée et supprime le tampon
			lié à ce dernier.

			<adresse> (str): L'adresse du client à déconnecter. """

		self.tampons[adresse].socket.close()
		self.tampons.pop(adresse)
		self.connecte = False
		self.jeu.enlever_client(adresse)

	def envoyer(self, adresse, donnee):
		""" Ecrit un message dans un tampon associé à une adresse donnée.

			<adresse> (str): L'adresse à laquelle envoyer un message.
			<donnee> (bytes): Le message à envoyer. """

		if adresse in list(self.tampons):
			self.tampons[adresse].ecrire(donnee)

	def recevoir(self, adresse):
		""" Lit le plus ancien message reçu stocké dans le tampon associé à
			une adresse donnée.

			<adresse> (str): L'adresse du client dont on veut lire la réponse. """

		if adresse in list(self.tampons):
			return self.tampons[adresse].lire()
		return bytes()

	def envoyer_broadcast(self, donnee):
		""" Envoie un message à tous les clients.

			<donnee> (bytes): Le message à envoyer. """
		for tampon in list(self.tampons.values()):
			tampon.ecrire(donnee)

	def recevoir_broadcast(self):
		""" Lit les messages stockés dans les tampons associés à tous les
			clients connectés. """

		messages = {}

		for adresse, tampon in list(self.tampons.items()):
			message = tampon.lire()

			if message:
				messages[adresse] = message
		return messages


class Client(object):
	""" Connecte un socket à un serveur et échange avec lui. """

	def __init__(self, jeu):
		""" Initialise un client.

			<jeu> (jeu.Jeu): Le jeu auquel appartient ce client. """

		self.jeu = jeu
		self.socket = sckt.socket()
		self.tampon = Tampon(self.socket)
		
		self.connecte = False
		self.activite_echange = False
		self.fil_echange = threading.Thread(target=self.echanger)

	def __bool__(self):
		""" Renvoie True si le client est connecté à un serveur ou s'il une
			boucle d'échange est active. Sinon False. """

		return self.connecte or self.activite_echange

	def echanger(self):
		""" Echange en continu avec le serveur. """

		while self.activite_echange:
			if self.tampon.fileno() != -1:
				lisibles, ecrivables, _ = select.select([self.tampon], \
					[self.tampon], [], 0.1)
		
				for tampon in ecrivables:
					if not tampon.envoyer():
						self.deconnecter()

				for tampon in lisibles:
					if self.connecte:
						if not tampon.recevoir():
							self.deconnecter()

	def lancer_echange(self):
		""" Lance un fil d'execution (thread) dédié aux échanges. """

		if not self.activite_echange:
			utile.debogguer("Lancement d'une boucle d'échange (client)")
			self.activite_echange = True
			self.fil_echange.start()

	def arreter_echange(self):
		""" Stoppe la boucle d'échange et le fil d'execution dédié. """

		if self.activite_echange:
			utile.debogguer("Arrêt d'une boucle d'échange (client)")
			self.activite_echange = False
			self.fil_echange.join()

	def connecter(self, adresse, port):
		""" Connecte le client à un serveur à une adresse et sur un port
			donné.

			<adresse> (str): L'adresse du serveur.
			<port> (int): Le port sur lequel se connecter. """

		try:
			self.socket.settimeout(10)
			self.socket.connect((adresse, port))
		except sckt.timeout:
			utile.debogguer("Temps de connexion à '" + adresse \
				+ "' avec le port " + str(port) + " dépassé", 1)
		except sckt.error:
			utile.debogguer("Impossible de se connecter à '" + adresse \
				+ "' avec le port " + str(port), 1)
		else:
			self.connecte = True
			self.socket.settimeout(1)
			return True
		return False

	def deconnecter(self):
		""" Ferme le socket du client. """

		if self.connecte:
			self.socket.close()
			self.connecte = False

	def envoyer(self, donnee):
		""" Ecrit un message dans le tampon.

			<donnee> (bytes): Le message à envoyer. """

		self.tampon.ecrire(donnee)

	def recevoir(self):
		""" Lit le plus ancien message reçu stocké dans le tampon. """
		
		return self.tampon.lire()