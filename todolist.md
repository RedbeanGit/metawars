# MetaWars, TO DO LIST

## data
- data/images/joueur/joueur_bouclier.png

## affichage.py
- Affichage: En cours
	* __init__(): Fait
	* charge_images(): Fait
	* obtenir_images(chemin_image): Fait
	* creer_widgets_splash(): A créer [Permet d'afficher la petite animation de démarrage]
	* creer_widgets_menu(): A créer [Permet d'afficher un bouton "Jouer", un titre, etc]
	* creer_widgets_niveau(): En cours [Un bouton "retour" ne serait pas de trop]
	* creer_widgets_fin_niveau(): A créer [Doit afficher un bouton pour revenir au menu principal, le temps et les pièces]
	* actualise(niveau): Fait
	* actualise_evenements(niveau): En cours [Ajouter un évènement pour mettre le jeu en pause]
	* actualise_scores(niveau): Fait
	* affiche_entite(entite): Fait
	* affiche_carte(niveau): Fait
	* affiche_widgets(): Fait

## constantes.py
- Supprimer FREQUENCE_TIR_JOUEUR
- Supprimer "frequence_tir_acceleree" des bonus car inutile

## entities.py
- Entite: Fait
	* __init__(niveau): Fait
	* __charge_image__(chemin_image): Fait
	* charge_image(): Fait
	* actualise(temps): Fait
	* bouge(temps): Fait
	* collisionne(): Fait
	* meurt(): Fait

- Joueur(Entite): En cours [L'attribut frequence_tir est inutile]
	* __init__(niveau): Fait
	* charge_image(): Fait
	* charge_image_touche(): Fait
	* charge_image_bouclier(): Fait
	* regarde_position(dx, dy): Fait
	* bouge(temps): Fait
	* tir(): Fait
	* haut(): Fait
	* bas(): Fait
	* droite(): Fait
	* gauche(): Fait
	* stop(): Fait
	* attaque(degat): En cours [Doit remplacer touche()]
		[Doit prendre en compte le bouclier]
		[Doit utiliser charge_image_touche() au lieu de changer l'image elle-même]
	* meurt(): Fait

- Ennemi(Entite): En cours
	* __init__(niveau): Fait
	* charge_image(): Fait
	* charge_image_touche(): Fait
	* actualise(temps): Fait
	* oriente(): Fait
	* attaque(degat): A créer [Doit remplacer touche()]
		[Doit utiliser charge_image_touche() au lieu de changer l'image elle-même]
	* tir(): Fait
	* est_trop_pres(): Fait

- Bonus(Entite): En cours
	* __init__(niveau): Fait
	* charge_image(): Fait
	* actualise(temps): Fait
	* attrape(): En cours [il faudrait rajouter des limites au bonus restant car il devienne trop pété après mdrrr]

- Tir(Entite): En cours
	* __init__(niveau, tireur): Fait
	* charge_image(): Fait
	* actualise(temps): Fait
	* touche(entite): En cours [Ne doit plus faire perdre de la vie à l'entité touchée mais appeler entite.attaque(degat)]

## niveau.py
- Niveau: En cours
	* __init__(): Fait
	* charge_image(): Fait
	* actualise(temps): Fait
	* fait_apparaite(temps): En cours [Doit utiliser cree_bonus() et cree_ennemi()]
	* enleve_entite(entite): Fait
	* cree_bonus(): En cours [Crée un nouveau bonus et lui attribue une position aléatoire autour du joueur]
	* cree_ennemi(): En cours [Crée un nouvel ennemi et lui attribue une position aléatoire autour du joueur]
	* termine(): En cours [Doit appeler Affichage.creer_widgets_fin_niveau()]

## widgets.py
- Widget: Fait
	* __init__(affichage): Fait
	* actualise(): Fait
	* actualise_evenement(evenement): Fait
	* obtenir_position_reelle(): Fait
	* est_dans_widget(position): Fait

- Text(Widget): Fait
	* __init__(affichage, texte): Fait
	* actualise(): Fait

- Bouton(Widget): Fait
	* __init__(affichage, texte, action): En cours [Doit afficher un texte centré]
	* charge_images(): Fait
	* actualise(): Fait
	* actualise_evenement(evenement): Fait