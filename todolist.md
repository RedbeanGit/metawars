# MetaWars, TO DO LIST


## affichage.py
- Affichage: En cours
	* __init__(): Fait
	* charge_images(): Fait
	* obtenir_images(chemin_image): Fait
	* creer_splash(): A créer [Permet d'affiche la petite animation de démarrage]
	* creer_menu(): A créer [Permet d'afficher un bouton "Jouer", un titre, etc]
	* creer_niveau(): A créer [Permet d'afficher le score, les pièces, ...]
	* actualise(niveau): En cours [Les entités du niveau et les widgets ne sont pas encore affichés]
	* actualise_evenements(): En cours [Rajouter des evenements pour bouger le joueur]


## constantes.py
Constantes manquantes (peut encore évoluer):
- TAILLE_JOUEUR
- TAILLE_ENNEMI
- TAILLE_BONUS
- TAILLE_TIR
- VITESSE_TIR
- FREQUENCE_BONUS


## entities.py
- Entite: En cours
	* __init__(niveau): Fait
	* charge_image(affichage): Fait
	* actualise(temps): Fait
	* bouge(temps): Fait
	* collisionne(): Fait
	* meurt(): A créer [Supprime l'entitée du niveau]

- Joueur(Entite): En cours
	* __init__(niveau): En cours [Certains attributs comme la taille du joueur doivent être redéfinis]
	* charge_image(affichage): Fait
	* tir(): En cours [Doit créer un tir dont la direction et la position dépendent de celles du joueur]
	* avance(): Fait
	* recule(): Fait
	* stop(): Fait
	* meurt(): En cours [Doit arreter le niveau]

- Ennemi(Entite): Fait
	* __init__(niveau): En cours [Certains attributs comme la taille de l'ennemi doivent être redéfinis]
	* charge_image(): En cours [Les ennemis n'ont toujours pas d'image]
	* tir(): En cours [Doit créer un tir dont la direction et la position dépendent de celles de l'ennemi]
	* actualise(temps): Fait
	* oriente(): Fait

- Bonus(Entite): Fait
	* __init__(niveau): En cours [Certains attributs comme la taille du bonus doivent être redéfinis]
	* charge_image(affichage): En cours [Les bonus n'ont toujours pas d'image]
	* actualise(temps): Fait
	* apparait(): En cours [Un bug à corriger]
	* attrape(): En cours [Doit modifier le joueur, pour l'instant, ne fait rien]

- Tir(Entite): Fait
	* __init__(niveau, tireur): En cours [L'entité ayant tiré doit être connue du tir]
	* charge_image(affichage): En cours [Les tirs n'ont toujours pas d'image]
	* actualise(temps): En cours [Les tirs doivent tester si elles touchent une entité]
	* touche(entite): En cours [Doit faire perdre de la vie à l'entité touchée]


## main.py
- main(): En cours [Doit d'abord lancer l'animation de démarrage, puis le menu principale, puis le niveau]
	[Doit enregistrer le score dans un fichier]


## niveau.py
- Niveau: En cours
	* __init__(): En cours [La gestion du score et des pièces doit être ajouté]
	* charge_image(affichage): En cours [Bug avec le fond de carte]
	* actualise(temps): En cours [Doit lancer Niveau.fait_apparaite()]
	* fait_apparaite(temps): En cours [Doit faire apparaitre des ennemis et des bonus aléatoirement et en fonction du temps écoulé]
	* enleve_entite(entite): En cours [Doit enlever une entite de la liste des entites du niveau]


## utile.py
- arreter(): Fait
- lire_fichier(): Fait
- ecrire_fichier(): Fait