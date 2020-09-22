# MetaWars, TO DO LIST

## data
- "data/images/joueur/joueur_bouclier.png" doit être ajouté
- "data/images/fond.png" doit être modifié car mauvais pour les yeux
	
## affichage.py
- Affichage: En cours
	* creer_widgets_splash(): A créer [Affiche une animation au démarrage]

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
	* heberger(): A créer [Crée un serveur et un niveau maitre multijoueur]
	* rejoindre(): A créer [Crée un client et un niveau esclave multijoueur]

## reseau.py
- Serveur: A creer
	* lancer(): A créer [Lance une boucle dans un autre processus en attente de connexions]
	* arreter(): A créer [Déconnecter tous les clients et arrete la boucle de connexion]
	* envoyer(donnee, client): A créer [Envoie une trame binaire à un client]
	* recevoir(client): A créer [Lit les trames en attentes envoyées par un client donné]
	* deconnecter(client): A créer [Déconnecte un client et le supprime de la liste des clients]

- Client: A creer
	* envoyer(donnee): A créer [Envoie une trame binaire au serveur]
	* recevoir(): A créer [Lit les trames en attentes envoyées par le serveur]
	* connecter(): A créer [Connecte le client à un serveur donné]
	* deconnecte(): A créer [Déconnecte le client du serveur]