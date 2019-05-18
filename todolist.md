# MetaWars, TO DO LIST

## data
- "data/images/joueur/joueur_bouclier.png" doit être ajouté
- "data/images/fond.png" doit être modifié car mauvais pour les yeux

## main.py
- lancer_partie(affichage): En cours
	[La boucle doit s'arrêter lorsque l'on quitte la partie (pour revenir au menu principal)]
	
## affichage.py
- Affichage: En cours
	* creer_widgets_splash(): A créer [Permet d'afficher la petite animation de démarrage]
	* creer_widgets_fin_niveau(): A créer [Doit afficher un bouton pour revenir au menu principal, le temps et les pièces]
	* actualise_evenements(niveau, en_partie): En cours [Ajouter un évènement pour mettre le jeu en pause]

## entities.py
- Joueur(Entite): En cours
	* attaque(degat): En cours [Doit prendre en compte le bouclier]

- Bonus(Entite): En cours
	* attrape(): En cours [il faudrait rajouter des limites au bonus restant car il devienne trop pété après mdrrr]

## niveau.py
- Niveau: En cours
	* fait_apparaite(temps): En cours [Doit faire apparaitre de plus en plus d'ennemis en fonction du temps total]
	* termine(): En cours [Doit appeler Affichage.creer_widgets_fin_niveau()]
	* sauvegarde(): A créer [Doit sauvegarder le temps et les pièces seulement si ces scores sont meilleurs que ceux déjà enregistrés]