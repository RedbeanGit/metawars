
"""
	Voici l'ordre d'éxecution des différentes fonctions et méthodes de MetaWars

	Une tabulation signifie que la fonction est appelée par la fonction avec le niveau de tabulation précédent, ex:
		Bonus.attrape(bonus, joueur)
			Entite.meurt(bonus) # Entite.meurt() est appelé à l'intérieur de Bonus.attrape()

	Un nom commençant par une Majuscule est un nom de classe, ex: Niveau
	Un nom commençant par une minuscule est un nom d'objet, ex: niveau (de classe Niveau)

	Attention à ne pas confondre un objet et une classe
	Les objets sont créés à partir des classes
	Les objets peuvent ensuite évoluer (leurs attributs peuvent changer), pas les classes
	Les classes sont uniques, les objets peuvent être en nombre infinis, ex:
		A partir de l'unique classe 'Ennemi', il est possible de créer plein d'objets 'ennemi'

	On peut utiliser des méthodes de classes pour modifier des objets, ex:
		Joueur.tir(joueur) # signifie que l'on applique la méthode tir que propose la classe Joueur sur l'objet joueur

	La syntaxe: Joueur.tir(joueur) peut être simplifiée en: joueur.tir() (dans ce cas, le premier argument de la fonction
	est remplacé par l'objet joueur)
	Dans ce fichier récapitulatif, on utilise la première syntaxe mais on utilise la deuxième dans le code du jeu
	
	Pour acceder à l'attribut d'un objet, on utilise la syntaxe: objet.attribut
"""



# initialisation des variables

affichage = Affichage() # on crée un affichage
	Affichage.__init__(affichage) # on initialise l'affichage avec __init__ (se fait automatiquement lorsqu'on utilise Affichage())

Affichage.charge_images(affichage) # on charge toutes les images (du disque dur vers la RAM)

Affichage.creer_widgets_niveau(affichage) # on crée les widgets pour afficher le score, le temps, la vie du joueur, etc
	texte_temps = Texte(affichage, "Temps: 0", (10, 10)) # on crée un widget Texte pour afficher le temps total
		Texte.__init__(texte_temps, affichage, "Temps: 0", position=(10, 10)) # on initialise le Texte avec __init__
			Widget.__init__(texte_temps, affichage, position=(10, 10), taille=(1, 1), ancrage=(-1, -1)) # le Texte initialise
			# ...les attributs qu'il hérite de Widget
	texte_pieces = Texte(affichage, "Pièces: 0", (10, 40)) # on crée un widget Texte pour afficher le nombre de pièces
		Texte.__init__(texte_pieces, affichage, "Pièces: 0", position=(10, 40)) # on initialise le Texte avec __init__
			Widget.__init__(texte_pieces, affichage, position=(10, 40), taille=(1, 1), ancrage=(-1, -1)) # le Texte initialise
			# ...les attributs qu'il hérite de Widget

niveau = Niveau() # on crée un niveau
	Niveau.__init__(niveau, affichage) # on initialise le niveau avec __init__
		niveau.joueur = Joueur() # le niveau crée un joueur
			Joueur.__init__(niveau.joueur, niveau) # on initialise le joueur du niveau avec __init__
				Entite.__init__(niveau.joueur, niveau) # le joueur initialise les attributs qu'il hérite de Entite

Niveau.charge_image(niveau) # on fait en sorte que le niveau récupère une copie des images dont lui et le joueur a besoin
	niveau.image = Affichage.obtenir_image(affichage, "data/images/fond_carte.png") # c'est grâce à cette méthode que le niveau 
	# ...récupère une copie de l'image de fond
	Joueur.charge_image(niveau.joueur) # on fait en sorte que le joueur récupère une copie de l'image dont il a besoin
		niveau.joueur.image = Affichage.obtenir_image(affichage, "data/images/joueur/joueur.png") # c'est grâce à cette méthode que 
		# ...le joueur récupère une copie de l'image "joueur.png"



# toutes les variables "globales" que l'on a besoin sont créée est initialisées
# on peut maintenant lancer la boucle de jeu

while True: # cette boucle est infinie (sauf si le joueur quitte le jeu ou qu'il crash)
	Affichage.actualise_evenements(affichage, niveau) # on gère les évènements utilisateurs (clic de souris, appui sur une touche, ...)

		# en imaginant que le joueur ferme la fenêtre (evenement.type == pygame.QUIT):
		utile.arreter()

		# en imaginant que le joueur appui sur la touche "D" du clavier:
		Joueur.droite(niveau.joueur)

		# en imaginant que le joueur relâche la touche "D" du clavier:
		Joueur.gauche(niveau.joueur)

		# en imaginant que le joueur déplace la souris:
		Joueur.regarde_position(niveau.joueur, dx, dy)

		# en imaginant que le joueur clic sur le bouton gauche de la souris:
		Joueur.tir(niveau.joueur)
			tir = Tir(niveau, entite) # le joueur crée un tir dont il est le tireur
				Tir.__init__(tir, niveau, entite) # on initialise le tir avec __init__
					Entite.__init__(tir, niveau) # le tir initialise les attributs hérités de Entite
			Tir.charge_image(tir) # on fait en sorte que le tir charge son image
				tir.image = Affichage.obtenir_image(affichage, "data/images/tir/tir.png") # c'est grâce à cette méthode 
				# ...que le tir récupère une copie de l'image "tir.png"

	Niveau.actualise(niveau, temps_ecoule_depuis_la_derniere_actualisation) # cette variable n'existe pas mais c'est plus simple pour
	# ...comprendre
		# si le niveau n'est pas en pause:
		Joueur.actualise(niveau.joueur, temps_ecoule_depuis_la_derniere_actualisation) # on actualise le joueur
			Entite.actualise(niveau.joueur, temps_ecoule_depuis_la_derniere_actualisation) # le joueur utilise la méthode actualise
			# ...qu'il a hérité de Entite (ça évite de recopier le code de Entite.actualise() dans Joueur.actualise())
				Joueur.bouge(niveau.joueur, temps_ecoule_depuis_la_derniere_actualisation) # on déplace légèrement le joueur

			# si le joueur est en animation (de dégat) et qu'il dépasse la durée d'animation (constantes.DUREE_ANIMATION_DEGAT):
			Joueur.charge_image(niveau.joueur) # on charge de nouveau l'image de base du joueur

			# si le joueur n'a plus de vie:
			Joueur.meurt(niveau.joueur) # il meurt (logique)

		# pour chaque entité du niveau excepté le joueur (celles dans la liste 'niveau.entites'):
		# ici, 'entite' correspond à une entité quelconque du niveau présente dans 'niveau.entites'

		# si l'entité est un ennemi:
		Ennemi.actualise(entite, temps_ecoule_depuis_la_derniere_actualisation) # on actualise l'ennemi
			Entite.actualise(entite, temps_ecoule_depuis_la_derniere_actualisation) # l'ennemi utilise la méthode actualise
			# ...qu'il a hérité de Entite (ça évite de recopier le code de Entite.actualise() dans Ennemi.actualise())
				Entite.bouge(entite, temps_ecoule_depuis_la_derniere_actualisation) # on bouge légèrement l'ennemi
			Ennemi.oriente(entite) # l'ennemi s'oriente en direction du joueur
			Ennemi.doit_tirer(entite, temps_ecoule_depuis_la_derniere_actualisation) # on teste si l'ennemi doit tirer

				# si oui:
				Ennemi.tir(entite)
					tir = Tir(niveau, entite) # l'ennemi crée un tir dont il est le tireur
						Tir.__init__(tir, niveau, entite) # on initialise le tir avec __init__
							Entite.__init__(tir, niveau) # le tir initialise les attributs hérités de Entite
					Tir.charge_image(tir) # on fait en sorte que le tir charge son image
						tir.image = Affichage.obtenir_image(affichage, "data/images/tir/tir.png") # c'est grâce à cette méthode 
						# ...que le tir récupère une copie de l'image "tir.png"

			# si l'ennemi est en animation (de dégat) et qu'il dépasse la durée d'animation (constantes.DUREE_ANIMATION_DEGAT):
			Ennemi.charge_image(niveau.ennemi) # on charge de nouveau l'image de base de l'ennemi
			
			Ennemi.est_trop_pres(entite) # on teste si l'ennemi est trop prêt du joueur
			# ...si oui on defini sa vitesse à 0

			# si l'ennemi n'a plus de vie:
			Ennemi.meurt(entite) # il meurt (logique)
				Entite.meurt(entite) # l'ennemi utilise la méthode meurt qu'il a hérité de Entite

		# si l'entité est un bonus:
		Bonus.actualise(entite, temps_ecoule_depuis_la_derniere_actualisation) # on actualise le bonus
			Entite.actualise(entite, temps_ecoule_depuis_la_derniere_actualisation) # le bonus utilise la méthode actualise
			# ...qu'il a hérité de Entite (ça évite de recopier le code de Entite.actualise() dans Bonus.actualise())
				Entite.bouge(entite, temps_ecoule_depuis_la_derniere_actualisation) # on bouge légèrement le bonus

			# si le bonus a dépassé la durée de vie d'un bonus (constantes.DUREE_BONUS)
			Entite.meurt(entite) # il meurt lol (PS: on utilise Entite.meurt() car Bonus n'a pas de méthode meurt())

			Entite.collisione(entite, niveau.joueur) # on teste si le bonus collisionne le joueur

				# si oui:
				Entite.attrape(entite, niveau.joueur) # on applique au joueur les effet du bonus
					Entite.meurt(entite) # puis le bonus meurt

		# si l'entité est un tir:
		Tir.actualise(entite, temps_ecoule_depuis_la_derniere_actualisation) # on actualise le tir
			Entite.actualise(entite, temps_ecoule_depuis_la_derniere_actualisation) # le tir utilise la méthode actualise
			# ...qu'il a hérité de Entite (ça évite de recopier le code de Entite.actualise() dans Tir.actualise())
				Entite.bouge(entite, temps_ecoule_depuis_la_derniere_actualisation) # on bouge légèrement le tir

			# si le tir a dépassé la durée de vie d'un tir (constantes.DUREE_TIR)
			Entite.meurt(entite) # il meurt lol (PS: on utilise Entite.meurt() car Tir n'a pas de méthode meurt())

			# si le tireur du tir est un joueur:
				# pour chaque entité du niveau excepté le joueur
				# ici, 'entite2' correspond à une entité quelconque du niveau présente dans 'niveau.entites'

				Entite.collisionne(entite2) # on teste si le tir collisionne avec une autre entité

					# si oui et que l'entité est un ennemi:
					Tir.touche(entite2) # le tir touche l'ennemi
						Ennemi.touche(entite2) # l'ennemi est touché
							entite2.image = Affichage.obtenir_image(affichage, "data/images/ennemi/ennemi_touche.png") # on récupère
							# ...une copie de l'image de l'ennemi touché
						Entite.meurt(entite) # le tir meurt (on utilise Entite.meurt() car Tir n'a pas de méthode meurt())

			# si le tireur du tir est un ennemi:
			Entite.collisionne(entite, niveau.joueur) # on teste si l'ennemi collisionne le joueur

				# si oui:
				Tir.touche(niveau.joueur) # le tir touche le joueur
					Joueur.touche(niveau.joueur) # le joueur est touché
						niveau.joueur.image = Affichage.obtenir_image(affichage, "data/images/joueur/joueur_touche.png") # on récupère
						# ...une copie de l'image du joueur touché
					Entite.meurt(entite) # le tir meurt

		Niveau.faire_apparaitre(niveau, temps_ecoule_depuis_la_derniere_actualisation) # on essaie de faire apparaitre un ennemi et/ou
		# ...un bonus
			# si on a sélectionné un nombre aléatoire suffisamment petit pour les bonus:
			bonus = Bonus(niveau) # on crée un bonus
				Bonus.__init__(bonus, niveau) # on initialise le bonus avec __init__
					Entite.__init__(bonus, niveau) # le bonus initialise les attributs qu'il hérite de Entite
			Bonus.charge_image(bonus) # on fait en sorte que le bonus charge son image
				bonus.image = Affichage.obtenir_image(affichage, "data/images/bonus/soin.png") # c'est grâce à cette méthode que 
				# ...le bonus récupère une copie de l'image "soin.png" (dans le cas d'un bonus de soin)

			# si on a sélectionné un nombre aléatoire suffisamment petit pour les ennemis:
			ennemi = Ennemi(niveau) # on crée un ennemi
				Ennemi.__init__(ennemi, niveau) # on initialise l'ennemi avec __init__
					Entite.__init__(ennemi, niveau) # l'ennemi initialise les atributs qu'il hérite de Entite
			Ennemi.charge_image(ennemi) # on fait en sorte que l'ennemi charge son image
				ennemi.image = Affichage.obtenir_image(affichage, "data/images/ennemi/ennemi.png") # c'est grâce à cette méthode que 
				# ...l'ennemi récupère une copie de l'image "ennemi.png"

	Affichage.actualise(affichage, niveau) # on redessine le contenu de la fenêtre afin que le joueur voit ce qui a changé
		Affichage.afficher_carte(affichage, niveau) # on redessine le fond du niveau (magnifique grille verte)
		Affichage.afficher_entite(affichage, niveau.joueur) # on redessine le joueur

		# pour chaque entité du niveau excepté le joueur (celles dans la liste niveau.entites)
		# 'entite' correspond à une entité quelconque de la liste niveau.entites
		Affichage.afficher_entite(affichage, entite) # on dessine chacune des entités
		
		Affichage.actualise_scores(affichage, niveau) # on change le texte des widgets affichant le temps et les pièces
		Affichage.afficher_widgets(affichage) # on redessine tous les widgets

			# pour chaque widget de l'affichage (dans la liste affichage.widgets)
			# 'widget' correspond à un widget quelconque de la liste affichage.widgets

			# si le widget est un texte:
			Texte.actualise(widget)

# la boucle recommence après cette instruction et ne s'arrête jamais