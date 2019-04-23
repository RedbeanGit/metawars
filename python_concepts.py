# Voici toutes les concepts pythonesques que vous devez connaitre


"""//////////////////////////////////////////////////////////////////////////////////////////////
/// Les variables ///////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////"""

# les variables permettent de référencer les objets dans la mémoire
# c'est à dire, donner un nom humainement lisible à la case mémoire
# dans laquelle est stocké l'objet

je_suis_une_variable = 4

# on suit généralement une convention pour nommer les variables
# elles doivent commencer par une lettre minuscule
	Je_suis_une_variable = 4 # ça c'est mal

# elles ne doivent pas contenir d'espace, ou de lettre accentuer
	je suis une variable = 4 # ça c'est très mal
	jé_sûìs_ùné_v@rîàblè = 4 # pas ouf comme nom

# les différents mots de nom de variable sont séparés par "_"
	jesuisunevariable = 4 # pas cool pour celui qui va lire
	jeSuisUneVariable = 4 # on fait ça dans d'autres langages mais pas en Python

# pour indiquer qu'une variable ne doit pas être modifiée (même si on peut quand même)
# on ajoute un "_" avant le nom de la variable
	_je_suis_une_variable_cache = 4

# les variables créées automatiquement par Python ou utilisée uniquement par Python
# sont entourées par "__"
	__je_suis_une_variable_speciale__ = 4
	__author__ = "François Hollande ma gueule"	# cette variable spéciale peut être utile
												# pour indiquer l'auteur du script mais
												# n'est pas utilisée par le programme

# contrairement à d'autres langages, les variables peuvent référencer n'importe
# quel type d'objet (car Python utilise le typage dynamique blabla osef)
	je_suis_une_variable = 4
	je_suis_une_variable = "mouah ah ah"	# aucune erreur, incroyable !

# une variable peut référencer un objet référencer par une autre variable
	je_suis_une_variable = "mouah ah ah"
	une_autre_variable = je_suis_une_variable	# les 2 variables référencent la même case mémoire
												# ! ATTENTION ! Si l'objet est modifié pour une variable,
												# il l'est aussi pour l'autre vu que c'est le même :-p


"""//////////////////////////////////////////////////////////////////////////////////////////////
/// Les types d'objet par défaut ////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////"""

# les objets sont caractérisés par leur type
# un nombre entier est de type 'int'
	4 # ceci est un int

# un nombre à virgule est de type 'float'
	4.56 # ceci est un float

# une chaine de caractère (du texte) est de type 'str'
	"salut les amis" # ceci est un str

# une liste d'objets est de type 'list'
	[1, "salut", 4.56] # est de type list

# une liste non modifiable est de type 'tuple'
	(1, "salut", 4.56) # est de type tuple

# un dictionnaire (voir plus bas) est de type 'dict'
	{"prenom": "François", "nom": "Hollande", "age": 64} # est du type dict


"""//////////////////////////////////////////////////////////////////////////////////////////////
/// L'appel de fonctions ////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////"""

# Une fonction est un bloc de code qui éxecute un ensemble d'instruction cachées pour nous
# Pas besoin de comprendre comment elle fonctionne, il suffit de savoir à quoi elle sert
	int(4.56)	# crée un entier à partir de l'argument passé (ici renvoie 4 à partir de 4.56)

# un fonction peut prendre zero, un ou plusieurs arguments
# chaque argument est séparé par une virgule
	min(2, 56)	# prend 2 arguments et renvoie le plus petit d'entre eux
	int(4.56)	# ne prend qu'un seul argument
	quit()	# ne prend aucun argument

# certaines fonctions peuvent prendre un nombre infini d'arguments
	print("salut", "les", "amis", "j'ai", 18, "ans")
# certaines fonctions peuvent prendre des arguments par mot clé
	enumerate(("chou", "beignet", "fleur"), start=4)	# démarre à 4 au lieu de 0 mais c'est optionnel
	enumerate(("chou", "beignet", "fleur"))	# marche aussi mais démarre à 0

# les fonctions renvoient toutes un objet (une sorte de résultat)
# qu'il est possible de référencer par une variable
	nombre_entier = int(4.56) # nombre_entier référence l'entier 4
# celle qui n'ont pas pour objectif de renvoyer un résultat renvoient quand même 'None'
	variable_inutile = print("salut")	# variable_inutile référence maintenant None car print()
										# n'a pas d'interêt à retourner un objet

# il est possible de passer un argument à une fonction à l'aide d'une variable
# l'objet référencé par la variable est alors utilisé
	print(variable_inutile) # affiche 'None'


"""//////////////////////////////////////////////////////////////////////////////////////////////
/// Les fonctions builtins //////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////"""

# pour afficher dans un terminal (ou invite de commande sur Windows) un objet:
	print("salut les amis")
# cette fonction va chercher à représenter l'objet passé en paramètre, même pour les plus abstrait
	print(4)	# affiche '4'
# elle peut prendre une infinité d'arguments
	print("j'ai", 4, "ans")	# affiche "j'ai 4 ans"
# par défaut, chaque argument est affiché séparé de l'argument précédent par un espace
# mais ce caractère est modifiable
	print("j'ai", 4, "ans", sep="|") # affiche "j'ai|4|ans"
# par défaut, un retour à la ligne est effectué à la fin de l'execution de cette fonction
# mais ce caractère est modifiable
	print("j'ai", 4, "ans", end=";")
	print("salut")						# affiche "j'ai 4 ans;salut" sur une même ligne

# pour lire le texte tapé par l'utilisateur dans le terminal et le référencer par une variable:
	ma_variable = input()
# cette fonction bloque l'execution du programme tant que l'utilisateur n'a pas fini d'écrire, 
# c'est à dire, tant qu'il n'a pas tapé sur "Entrer"
# cette fonction peut prendre un paramêtre, un objet à afficher avant le texte tapé 
# par l'utilisateur
	ma_variable = input("Entrez du texte ici : ")
# Attention, cette fonction retourne toujours un objet de type 'str' (chaine de caratère)
# même si l'utilisateur ne tape que des nombres ! Et "4" est différent de 4


# pour créer une suite arithmétique d'entiers naturels
	suite = range(5, 89, 56)	# crée une suite contenant tous les nombres de 5 (inclus)
								# à 89 (non inclus) avec un pas de 56
								# autrement dit: (5, 61)

# pour trier une liste de nombres (float et/ou int)
	liste_trie = sorted([56, 2, 48, 46, 23])	# liste_trie référence maintenant:
												# [2, 23, 46, 48, 56]
# pour trier à l'envers, on utilise l'argument optionnel 'reverse'
	liste_trie = sorted([56, 2, 48, 46, 23], reverse=True)	# liste_trie référence maintenant:
															# [56, 48, 46, 23, 2]

# pour obtenir la taille d'une suite, d'une liste, d'un tuple, d'un dictionnaire, ...
	len([4, 45, 65, 12, 89])	# renvoie 5 car il y a 5 objet dans cette liste


"""//////////////////////////////////////////////////////////////////////////////////////////////
/// Les commentaires ////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////"""

# ceci est un commentaire (il n'est pas interpreté par Python)

"""
Ceci es un commentaire
sur plusieurs lignes
"""

# certains commentaires sont spéciaux:
# celui-ci signifie que votre script utilise l'encodage "utf-8"
	# -*- coding: utf-8 -*-

# celui-là indique aux systèmes basés sur GNU/Linux qu'il doit executer le script avec Python 3
	#!/usr/bin/python3