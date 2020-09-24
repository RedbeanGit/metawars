# Changelog 4:

## projet
+ Ajout de jeu.py et reseau.py
* Les objets principaux sont maintenant centralisés dans la classe Jeu (jeu.py)

## affichage.py
+ Ajout de creer_widgets_pause(jeu)
+ Ajout de creer_widgets_fin(jeu)
+ Ajout de creer_widgets_multijoueur(jeu)
+ Ajout de supprimer_widgets_pause(jeu)
+ Ajout de afficher_message(message)

## jeu.py
+ Ajout de la classe Jeu pour centraliser les objets et opérations principales

## main.py
- Suppression de lancer_jeu() et lancer_partie()
+ Ajout de demarrer()

## niveau.py
+ Ajout de supprimer_joueur(pseudo)
+ Ajout de l'attribut Niveau.joueurs pour associer les joueurs à leur pseudo
+ Ajout de quand_joueur_meurt
* Prise en charge de plusieurs joueurs dans un même Niveau
- Suppression de terminer()

## reseau.py
+ Ajout de la classe Serveur
+ Ajout de la classe Client

## widgets.py
+ Ajout de la classe TexteEditable
+ Ajout de la classe TexteTemporaire
+ Ajout de Texte.obtenir_surface
* La taille des Texte est maintenant calculée sans nécessiter un premier appel à Texte.actualiser()
* Les attributs hérités des widgets sont maintenant gérés directement par le widget qui les implémentes