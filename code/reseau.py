# -*- coding: utf-8 -*-

"""
	Contient des classes liées au communications réseau (type client / serveur).
"""

"""
plan:

heberger partie:
	creer serveur
	creer niveau
	quand serveur recoit connexion:
		recevoir pseudo
		ajouter joueur
		envoyer infos niveau
		tant que connecté:
			recevoir evenements
			envoyer infos niveau
		supprimer joueur

rejoindre partie:
	creer client
	quand client connecté:
		envoyer pseudo
		creer niveau
		recevoir infos niveau
		tant que connecté:
			envoyer evenements
			recevoir infos niveau
		retourner menu principal
"""