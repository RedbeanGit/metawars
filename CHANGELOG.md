# Changelog 5

## projet
- Ajout d'une licence
- Réorganisation du projet
- Suppression de todolist.md

## affichage
- Ajout de Affichage.creer\_widgets\_heberger()
- Ajout de Affichage.creer\_widgets\_rejoindre()
- Ajout de Affichage.obtenir\_taille()

## constantes
- Ajout de General.VERSION
- Ajout de docstrings
- Modification de Chemin.RESSOURCES

## entites
- Ajout de l'attribut Entite.identifiant
- Ajout de Entite.exporter()
- Ajout de Entite.importer()
- Ces deux méthodes sont surchargés par tous les types d'entité

## jeu
- Ajout de Jeu.initialiser\_menu\_multijoueur()
- Ajout de Jeu.initialiser\_menu\_heberger()
- Ajout de Jeu.initialiser\_menu\_rejoindre()
- Ajout de Jeu.initialiser\_partie\_serveur()
- Ajout de Jeu.initialiser\_partie\_client()
- Ajout de Jeu.arreter\_partie() pour prévenir les clients ou le serveur lorsqu'un joueur se déconnecte
- Ajout de Jeu.finir\_partie\_serveur()
- Ajout de Jeu.finir\_partie\_client()
- Ajout de Jeu.ajouter\_client()
- Ajout de Jeu.enlever\_client()
- Jeu.arreter() déconnecte maintenant un éventuel client ou serveur
- Jeu.creer\_niveau() permet maintenant de créer un niveau avec prise en charge réseau
- Suppression de Jeu.lancer\_mode\_heberger() au profit de Jeu.initialiser\_menu\_heberger()
- Suppression de Jeu.lancer\_mode\_rejoindre() au profit de Jeu.initialiser\_menu\_rejoindre()

## main
- En cas d'erreur non gérée, le jeu est maintenant proprement arrêté

## niveau
- Ajout de Niveau.joueur\_id
- Ajout de Niveau.ajouter\_entite()
- Ajout de Niveau.obtenir\_entite() pour trouver une entité à partir d'un identifiant
- Ajout de Niveau.obtenir\_joueurs()
- Ajout de Niveau.commander\_joueur()
- Ajout de Niveau.quand\_joueur\_meurt()
- Ajout de la classe NiveauReseau permettant la prise en charge des parties en réseau
- Ajout de la classe NiveauClient
- Ajout de la classe NiveauServeur
- Niveau.creer\_joueur(), Niveau.creer\_bonus() et Niveau.creer\_ennemi() n'ajoutent plus l'entité créé au niveau mais la renvoie
- Niveau.obtenir\_joueur\_local() renvoie maintenant le joueur associé à Niveau.joueur\_id
- Niveau.actualiser\_evenement() délègue maintenant la gestion des évènements s'appliquant au joueur à Niveau.commander\_joueur()
- NiveauReseau.actualiser() envoie et reçoit les données des autres joueurs
- Suppression de Niveau.supprimer\_joueur()

## reseau
- Ajout de la classe Tampon
- Ajout de Serveur.accrocher()
- Ajout de Serveur.echanger()
- Ajout de Serveur.lancer_ecoute()
- Ajout de Serveur.lancer_echange()
- Ajout de Serveur.arreter_ecoute()
- Ajout de Serveur.arreter_echange()
- Ajout de Serveur.obtenir_adresse_tampon()
- Ajout de Serveur.envoyer_broadcast()
- Ajout de Serveur.recevoir_broadcast()
- Ajout de la classe Client
- Ajout de Client.echanger()
- Ajout de Client.lancer_echange()
- Ajout de Client.arreter_echange()
- Serveur.\_\_bool\_\_() dépend de l'état de la boucle d'échange et d'écoute du serveur
- Serveur.envoyer() et Serveur.recevoir() passent maintenant par un tampon
- Client.\_\_bool\_\_() dépend de l'état de la boucle d'échange
- Client.connecter() prend maintenant en charge les erreurs de connexion
- Client.envoyer() et Client.recevoir() passent maintenant par un tampon
- Suppression de Serveur.lancer()
- Suppression de Serveur.arreter()

## utile
- Ajout de obtenir\_nb\_args()
- Ajout de charger\_json()
- Ajout de formater\_json()

___

# Changelog 4

## projet
- Ajout de jeu et reseau
- Les objets principaux sont maintenant centralisés dans la classe Jeu (jeu.py)

## affichage
- Ajout de Affichage.creer\_widgets\_pause()
- Ajout de Affichage.creer\_widgets\_fin()
- Ajout de Affichage.creer\_widgets\_multijoueur()
- Ajout de Affichage.supprimer\_widgets\_pause()
- Ajout de Affichage.afficher\_message()

## jeu
- Ajout de la classe Jeu pour centraliser les objets et opérations principales

## main
- Ajout de demarrer()
- Suppression de lancer\_jeu() et lancer\_partie()

## niveau
- Ajout de Niveau.supprimer\_joueur()
- Ajout de Niveau.joueurs pour associer les joueurs à leur pseudo
- Ajout de Niveau.quand\_joueur\_meurt()
- Prise en charge de plusieurs joueurs dans un même Niveau
- Suppression de Niveau.terminer()

## reseau
- Ajout de la classe Serveur
- Ajout de la classe Client

## widgets
- Ajout de la classe TexteEditable
- Ajout de la classe TexteTemporaire
- Ajout de Texte.obtenir\_surface()
- La taille des Texte est maintenant calculée sans nécessiter un premier appel à Texte.actualiser()
- Les attributs hérités des widgets sont maintenant gérés directement par le widget qui les implémentes

___

# Changelog 3

## projet
- todolist.md contient uniquement les trucs à faire, les fonctions et méthodes terminées ne sont plus indiquées
- Suppression des print() inutiles (ralentit le jeu sur Windows en surchargeant la console)

## constantes
- VITESSE\_JOUEUR = 3 -> 4
- BONUS\_VITESSE = 0.2 -> 0.15

## widgets
- Ajout de la classe Image

## main
- Ajout de lancer\_partie()
- main() -> lancer\_jeu()
- niveau -> niveau\_menu

___

# Changelog 2

## data
- 'data/joueur/joueur\_0.png' -> 'data/joueur/joueur.png'

## affichage
- Ajout de Affichage.affiche\_carte()
- Les évènements claviers sont maintenant différenciés grâce à l'attribut 'unicode'

## constantes
- Ajout de DUREE\_BONUS
- 'joueur\_0.png' -> 'joueur.png'
- 'joueur\_coeur\_touche.png' -> 'joueur\_touche.png'
- Les listes sont remplacées par des tuples (car plus rapide et non mutable donc plus adaptés pour contenir des constantes)
- Suppression de TAILLE\_CARTE
- Suppression du chemin vers l'image 'joueur\_1.png'
- Suppression du chemin vers l'image 'joueur\_2.png'
- Suppression du chemin vers l'image 'joueur\_3.png'
- Suppression du chemin vers l'image 'joueur\_4.png'
- Suppression du chemin vers l'image 'joueur\_5.png'
- Suppression du chemin vers l'image 'joueur\_6.png'
- Suppression du chemin vers l'image 'joueur\_7.png'
- Suppression du chemin vers l'image 'joueur\_8.png'
- Suppression du chemin vers l'image 'joueur\_9.png'
- Suppression du chemin vers l'image 'joueur\_coeur.png'

## entites
- Ajout de Bonus.temps\_vie
- Le joueur utilise maintenant la texture 'joueur.png' au lieu de 'joueur\_0.png'
- Bonus.actualise() fait maintenant mourir le bonus si celui-ci reste plus de DUREE\_BONUS secondes

## niveau
- Le niveau charge maintenant une image de fond

___

# Changelog 1

## affichage
- Ajout de Affichage.affiche\_entite()
- Affichage.obtenir\_image() n'affiche plus d'erreur si l'image demandée n'a pas été chargée
- Affichage.actualise() utilise maintenant Affichage.affiche\_entite() pour afficher les entités
- Le clic gauche de la souris permet de tirer (plus intuitif)

## constantes
- Ajout de TAILLE\_BONUS
- Ajout de DEGAT\_ENNEMI
- Ajout de BONUS\_SOIN
- Ajout de BONUS\_VITESSE
- Ajout de BONUS\_FREQUENCE\_TIR
- Ajout de BONUS\_DEGAT
- Réorganisation des constantes pour mieux s'y retrouver
- FREQUENCE\_DE\_TIR -> FREQUENCE\_TIR
- DEGAT\_TIR -> DEGAT\_JOUEUR
- TYPE\_DE\_BONUS -> TYPE\_BONUS

## entites
- Ajout de Joueur.bouclier
- Ajout de Ennemi.degat\_tir
- Ajout de Ennemi.meurt()
- Ajout de Tir.tireur
- Les entités ont maintenant une image par défaut au lieu de None
- Entite.charge\_image() utilise maintenant directement l'affichage du niveau auquel elle appartient
- Entite.meurt() doit être appelée sans argument. Une entite peut mourir sans être forcément tuée par une autre entité
- Joueur.frequence\_de\_tir -> Joueur.frequence\_tir
- Joueur.tir() et Ennemi.tir() on été recréées
- Bonus.attrape() a été revue (Attention à n'utiliser cette méthode que sur le joueur)
- Le tir doit maintenant savoir qui l'a généré, sinon il ne peut pas savoir quelles entités tuer
- Tir.actualise() teste maintenant les collisions avec toutes les entités
- Tir.touche() reduit la vie de l'entité touchée en fonction des dégats du tireur

## niveau
- Niveau.enleve\_entite() a été défini
- Le nombre aléatoire utilisé pour faire apparaitre un bonus est maintenant différent de celui pour faire apparaitre les ennemis

## utile
- Ajout de la fonction radian\_en\_degres()
- Ajout de la fonction degres\_en\_radian()