# Changelog 2:

## data
* 'data/joueur/joueur_0.png' -> 'data/joueur/joueur.png'

## affichage.py
+ Ajout de Affichage.affiche_carte(self, niveau)
* Les évènements claviers sont maintenant différenciés grâce à l'attribut 'unicode'

## constantes.py
+ Ajout de DUREE_BONUS
- Suppression de TAILLE_CARTE
- Suppression du chemin vers l'image 'joueur_1.png'
- Suppression du chemin vers l'image 'joueur_2.png'
- Suppression du chemin vers l'image 'joueur_3.png'
- Suppression du chemin vers l'image 'joueur_4.png'
- Suppression du chemin vers l'image 'joueur_5.png'
- Suppression du chemin vers l'image 'joueur_6.png'
- Suppression du chemin vers l'image 'joueur_7.png'
- Suppression du chemin vers l'image 'joueur_8.png'
- Suppression du chemin vers l'image 'joueur_9.png'
- Suppression du chemin vers l'image 'joueur_coeur.png'
* 'joueur_0.png' -> 'joueur.png'
* 'joueur_coeur_touche.png' -> 'joueur_touche.png'
* Les listes sont remplacées par des tuples (car plus rapide et non mutable donc plus adaptés pour contenir des constantes)

## entites.py
+ Ajout de Bonus.temps_vie
* Le joueur utilise maintenant la texture 'joueur.png' au lieu de 'joueur_0.png'
* Bonus.actualise(self, temps) fait maintenant mourir le bonus si celui-ci reste plus de DUREE_BONUS secondes

## niveau.py
* Le niveau charge maintenant une image de fond