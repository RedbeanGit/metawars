# Changelog:

## affichage.py
+ Ajout de Affichage.affiche_entite(self, entite)
	Permet de dessiner n'importe quelle entité en prenant en compte sa position, sa taille, sa texture et son angle de rotation
* Affichage.obtenir_image(self, chemin_image) n'affiche plus d'erreur si l'image demandée n'a pas été chargée
* Affichage.actualise(self) utilise maintenant Affichage.affiche_entite() pour afficher les entités (logique :-p)
* Le clic gauche de la souris permet de tirer (à la place du clic droit car c'est plus intuitif)

## constantes.py
+ Ajout de TAILLE_BONUS
+ Ajout de DEGAT_ENNEMI
+ Ajout de BONUS_SOIN
+ Ajout de BONUS_VITESSE
+ Ajout de BONUS_FREQUENCE_TIR
+ Ajout de BONUS_DEGAT
* Réorganisation des constantes pour mieux s'y retrouver
* FREQUENCE_DE_TIR -> FREQUENCE_TIR
* DEGAT_TIR -> DEGAT_JOUEUR
* TYPE_DE_BONUS -> TYPE_BONUS

## entites.py
+ Ajout de Joueur.bouclier
	Inutile pour l'instant, permettra au joueur de prendre ou non des dégats
+ Ajout de Ennemi.degat_tir
+ Ajout de Ennemi.meurt(self)
	Ajoute des pièce au niveau lors de la mort d'un ennemi
+ Ajout de Tir.tireur
* Les entités ont maintenant une image par défaut au lieu de None
* Entite.charge_image(self, affichage) -> Entite.charge_image(self)
	Cette méthode utilise maintenant directement l'affichage du niveau auquel elle appartient
* Entite.meurt(self, entite) -> Entite.meurt(self)
	Une entite peut mourir sans être forcément tuée par une autre entité
* Joueur.frequence_de_tir -> Joueur.frequence_tir
* Joueur.tir(self) et Ennemi.tir(self) on été recréées
* Bonus.attrape(self, entite) -> Bonus.attrape(self, joueur)
	Cette méthode a été revue (Attention à n'utiliser cette méthode que sur le joueur)
* Tir.__init__(self, niveau) -> Tir.__init__(self, niveau, tireur)
	Le tir doit savoir qui l'a généré, sinon il ne peut pas savoir quelles entités tuer
* Tir.actualise(self, temps) teste maintenant les collisions avec toutes les entités
* Tir.touche(self, entite) reduit la vie de l'entité touchée en fonction des dégats du tireur

## niveau.py
+ Niveau.enleve_entite(self, entite) a été défini
* Le nombre aléatoire utilisé pour faire apparaitre un bonus est maintenant différent de celui
	pour faire apparaitre les ennemis

## utile.py
+ Ajout de la fonction radian_en_degres(angle)
+ Ajout de la fonction degres_en_radian(angle)