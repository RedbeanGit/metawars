# MetaWars, TO DO LIST

## data
- "data/images/joueur/joueur_bouclier.png" doit être ajouté
- "data/images/fond.png" doit être modifié car mauvais pour les yeux
	
## affichage.py
- Affichage: En cours
	* creer_widgets_splash(jeu): A créer [Affiche une animation au démarrage]
	* creer_widgets_heberger(jeu): A créer [Affiche des textes éditables et boutons pour paramètrer un serveur]
	* creer_widgets_rejoindre(jeu): A créer [Affiche des textes éditables et boutons pour rejoindre un serveur]

## entities.py
- Joueur(Entite): En cours
	* attaque(degat): En cours [Doit prendre en compte le bouclier]

- Bonus(Entite): En cours
	* attrape(): En cours [il faudrait rajouter des limites au bonus restant car il devienne trop pété après mdrrr]

## niveau.py
- Niveau: En cours
	* fait_apparaite(temps): En cours [Doit faire apparaitre de plus en plus d'ennemis en fonction du temps total]
	* sauvegarde(): A créer [Sauvegarde le temps et les pièces seulement si ces scores sont meilleurs que ceux déjà enregistrés]

## jeu.py
- Jeu: En cours
	* lancer_mode_heberger(): En cours [Doit demander au joueur les infos du serveur à créer]
	* lancer_mode_rejoindre(): En cours [Doit demander au joueur les infos du serveur à rejoindre]
	* heberger(): A créer [Crée un serveur et un niveau maitre multijoueur]
	* rejoindre(): A créer [Crée un client et un niveau esclave multijoueur]
	* ajouter_joueur(pseudo): En cours [Doit gérer la connexion d'un nouveau joueur]
	* enlever_joueur(pseudo): En cours [Doit gérer la déconnexion d'un joueur]

## reseau.py
- Serveur: En cours
	* lancer(): En cours [Doit vérifier si le serveur est déjà lancé]
	* arreter(): En cours [Doit vérifier si le serveur n'est pas lancé]
	* envoyer(donnee, addresse): En cours [Doit gérer les erreurs d'envoi]
	* recevoir(addresse): En cours [Doit gérer les erreurs de réception]

- Client: En cours
	* envoyer(donnee): En cours [Doit gérer les erreurs d'envoi]
	* recevoir(): En cours [Doit gérer les erreurs de réception]