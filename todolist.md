# MetaWars, TO DO LIST

## affichage.py
- Affichage: En cours
	* __init__(): Fait
	* charge_images(): Fait
	* obtenir_images(chemin_image): Fait
	* creer_splash(): A créer [Permet d'afficher la petite animation de démarrage]
	* creer_menu(): A créer [Permet d'afficher un bouton "Jouer", un titre, etc]
	* creer_niveau(): A créer [Permet d'afficher le score, les pièces, ...]
	* actualise(niveau): En cours [Les widgets ne sont pas encore affichés]
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
	* bouge(temps): En cours [L'entité ne doit pas sortir de la carte]
	* collisionne(): Fait
	* meurt(): En cours (à vérifier) [Supprime l'entitée du niveau] 

- Joueur(Entite): En cours
	* __init__(niveau): En cours [Certains attributs comme la taille du joueur doivent être redéfinis]
	* charge_image(affichage): Fait
	* tir(): En cours [Doit créer un tir dont la direction et la position dépendent de celles du joueur]
	* avance(): Fait
	* recule(): Fait
	* stop(): Fait
	* meurt(): En cours [Doit arreter le niveau]

- Ennemi(Entite): En cours
	* __init__(niveau): En cours [Certains attributs comme la taille de l'ennemi doivent être redéfinis]
	* charge_image(): Fait
	* tir(): En cours [Doit créer un tir dont la direction et la position dépendent de celles de l'ennemi]
	* actualise(temps): Fait
	* oriente(): Fait
	* tir(): Fait

- Bonus(Entite): En cours
	* __init__(niveau): En cours [Certains attributs comme la taille du bonus doivent être redéfinis]
	* charge_image(affichage): Fait
	* actualise(temps): Fait
	* attrape(): En cours [Doit modifier le joueur, pour l'instant, ne fait rien]

- Tir(Entite): En cours
	* __init__(niveau, tireur): En cours [L'entité ayant tiré doit être connue du tir]
	* charge_image(affichage): En cours [Les tirs n'ont toujours pas d'image]
	* actualise(temps): En cours [Les tirs doivent tester si ils touchent une entité]
	* touche(entite): En cours [Doit faire perdre de la vie à l'entité touchée]

## niveau.py
- Niveau: En cours
	* __init__(): En cours [La gestion du score et des pièces doit être ajouté]
	* charge_image(affichage): En cours [Bug avec le fond de carte]
	* actualise(temps): Fait
	* fait_apparaite(temps): En cours [Doit faire apparaitre des bonus aléatoirement et en fonction du temps écoulé]
	* enleve_entite(entite): En cours [Doit enlever une entite de la liste des entites du niveau]

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
	* __init__(affichage, action): Fait
	* charge_images(): Fait
	* actualise(): Fait
	* actualise_evenement(evenement): Fait