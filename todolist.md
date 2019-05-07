# MetaWars, TO DO LIST

- Ajouter des docstring (pour plus d'info, me contacter)

## data
- "data/images/joueur/joueur_bouclier.png" doit être ajouté
- "data/images/fond.png" doit être modifié car mauvais pour les yeux

## main.py
- main(): En cours
	[Le niveau ne doit plus être actualisé par les actions utilisateur (car utilisé en fond du menu principal)]

- lancer_partie(affichage): A créer
	[Identique à main() excepté qu'il ne gère pas le menu principal mais l'écran de jeu lui-même]
	[Doit supprimer les widgets de affichage et appeler 'creer_widgets_niveau()']
	[Doit actualiser le niveau avec les évènements utilisateurs (comme jusqu'a maintenant en fait)]
	
## affichage.py
- Affichage: En cours
	* creer_widgets_splash(): A créer [Permet d'afficher la petite animation de démarrage]
	* creer_widgets_menu(fct_partie): En cours [Permet d'afficher un bouton "Jouer", un titre, etc]
	* creer_widgets_niveau(): En cours [Un bouton "retour" ne serait pas de trop]
	* creer_widgets_fin_niveau(): A créer [Doit afficher un bouton pour revenir au menu principal, le temps et les pièces]
	* actualise_evenements(niveau, en_partie): En cours [Ajouter un évènement pour mettre le jeu en pause]
		[Si 'en_partie' vaut True, il ne faut pas faire bouger le joueur ni le faire tirer]

## entities.py
- Joueur(Entite): En cours
	* attaque(degat): En cours [Doit remplacer touche()]
		[Doit prendre en compte le bouclier]
		[Doit utiliser charge_image_touche() au lieu de changer l'image elle-même]

- Ennemi(Entite): En cours
	* attaque(degat): A créer [Doit remplacer touche()]
		[Doit utiliser charge_image_touche() au lieu de changer l'image elle-même]

- Bonus(Entite): En cours
	* attrape(): En cours [il faudrait rajouter des limites au bonus restant car il devienne trop pété après mdrrr]

- Tir(Entite): En cours
	* touche(entite): En cours [Ne doit plus faire perdre de la vie à l'entité touchée mais appeler entite.attaque(degat)]

## niveau.py
- Niveau: En cours
	* fait_apparaite(temps): En cours [Doit faire apparaitre de plus en plus d'ennemis en fonction du temps total]
	* termine(): En cours [Doit appeler Affichage.creer_widgets_fin_niveau()]