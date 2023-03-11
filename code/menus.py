__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"

import constantes
from widgets import Texte, Bouton, Image, TexteTemporaire, TexteEditable


class Menu(object):
    def __init__(self, jeu):
        self.jeu = jeu
        self.widgets = []
        self.creer()

    def creer(self):
        pass

    def actualiser(self):
        for widget in self.widgets:
            if widget.expire:
                self.widgets.remove(widget)
            else:
                widget.actualiser()

    def ajouter_widget(self, widget):
        self.widgets.append(widget)

    def afficher_message(self, message, couleur=(255, 255, 255, 255)):
        l, h = self.jeu.affichage.obtenir_taille()

        self.widgets.append(TexteTemporaire(self, message, 2,
                                            position=(l // 2, h*0.33), ancrage=(0, 0),
                                            couleur=couleur))

    def nettoyer(self):
        while self.widgets:
            self.widgets.pop().nettoyer()


class MenuPrincipal(Menu):
    def creer(self):
        super().creer()

        a = self.jeu.affichage
        l, h = a.obtenir_taille()

        mx = l // 2
        my = h // 2
        mmy = h - my // 2
        ecart = 5

        self.ajouter_widget(Bouton(a, self.jouer, texte="Jouer en solo",
                                   position=(mx, my), taille=(300, 50), ancrage=("centre", "centre"),
                                   taille_police=16))

        self.ajouter_widget(Bouton(a, self.multijoueur, texte="Multijoueur",
                                   position=(mx, my - 80), taille=(300, 50),
                                   ancrage=("centre", "centre"), taille_police=16))

        self.ajouter_widget(Bouton(a, self.quitter, texte="Quitter",
                                   position=(mx, my - 160), taille=(300, 50),
                                   ancrage=("centre", "centre"), taille_police=16))

        self.ajouter_widget(Image(a, constantes.General.IMAGE_TITRE,
                                  position=(mx, mmy), taille=(400, 80),
                                  ancrage=("centre", "centre")))

        self.ajouter_widget(Texte(a, "v" + constantes.General.VERSION,
                                  position=(ecart, ecart), ancrage=("gauche", "bas"), taille_police=14))

        self.ajouter_widget(Texte(a, __author__, position=(l-ecart, ecart),
                                  ancrage=("droite", "bas"), taille_police=14))

    def jouer(self):
        self.jeu.initialiser_partie()

    def multijoueur(self):
        self.jeu.initialiser_menu_multijoueur()

    def quitter(self):
        self.jeu.arreter()


class MenuPartie(Menu):
    def creer(self):
        super().creer()

        a = self.jeu.affichage
        l, h = a.obtenir_taille()
        ecart = 10

        self.ajouter_widget(Texte(a, "Temps: 0s", position=(ecart, h-ecart),
                                  ancrage=("gauche", "haut")))

        self.ajouter_widget(Texte(a, "Pièces: 0", position=(ecart, h-4*ecart),
                                  ancrage=("gauche", "haut")))

        self.ajouter_widget(Texte(a, "Vie: 0", position=(ecart, h-7*ecart),
                                  ancrage=("gauche", "haut")))

        self.ajouter_widget(Texte(a, "Bonus dégats: 0",
                                  position=(l-ecart, h-ecart), ancrage=("droite", "haut")))

        self.ajouter_widget(Texte(a, "Bonus vitesse: x1",
                                  position=(l-ecart, h-4*ecart), ancrage=("droite", "haut")))

    def actualiser(self):
        super().actualiser()

        texte_temps = self.widgets[0]
        texte_pieces = self.widgets[1]
        texte_vie = self.widgets[2]
        texte_arme = self.widgets[3]
        texte_vitesse = self.widgets[4]

        niveau = self.jeu.niveau
        joueur = niveau.obtenir_joueur_local()

        texte_temps.changer_texte("Temps: {temps}s".format(temps=int(niveau
                                                                     .temps_total)))
        texte_pieces.changer_texte("Pièces: {pieces}".format(
            pieces=niveau.pieces))
        texte_vie.changer_texte("Vie: {vie}".format(vie=int(joueur.vie)))

        texte_arme.changer_texte("Bonus dégats: {degats}".format(degats=joueur
                                                                 .degats_bonus))
        texte_vitesse.changer_texte(
            "Bonus vitesse: x{vitesse}".format(vitesse=round(joueur.vitesse, 2)))


class MenuMultijoueur(Menu):
    def creer(self):
        super().creer()

        a = self.jeu.affichage
        l, h = a.obtenir_taille()

        mx = l // 2
        my = h // 2
        mmy = h - my // 2

        self.ajouter_widget(Image(a, constantes.General.IMAGE_TITRE,
                                  position=(mx, mmy), taille=(400, 80),
                                  ancrage=("centre", "centre")))

        self.ajouter_widget(Texte(a, "Multijoueur",
                                  position=(mx, h * 0.6), ancrage=("centre", "centre"),
                                  taille_police=18))

        self.ajouter_widget(Bouton(a, self.heberger, texte="Héberger",
                                   position=(mx, my), taille=(300, 50),
                                   ancrage=("centre", "centre"), taille_police=16))

        self.ajouter_widget(Bouton(a, self.rejoindre, texte="Rejoindre",
                                   position=(mx, my-80), taille=(300, 50),
                                   ancrage=("centre", "centre"), taille_police=16))

        self.ajouter_widget(Bouton(a, self.retour, texte="Retour",
                                   position=(mx, my-160), taille=(300, 50),
                                   ancrage=("centre", "centre"), taille_police=16))

    def heberger(self):
        self.jeu.initialiser_menu_heberger()

    def rejoindre(self):
        self.jeu.initialiser_menu_rejoindre()

    def retour(self):
        self.jeu.initialiser_menu_principal()


class MenuHeberger(Menu):
    def creer(self):
        super().creer()

        a = self.jeu.affichage
        l, h = a.obtenir_taille()

        mx = l // 2
        my = h // 2
        mmy = h - my // 2

        self.ajouter_widget(Image(a, constantes.General.IMAGE_TITRE,
                                  position=(mx, mmy), taille=(400, 80),
                                  ancrage=("centre", "centre")))

        self.ajouter_widget(Texte(a, "Héberger",
                                  position=(mx, h*0.6), ancrage=("centre", "centre"),
                                  taille_police=18))

        self.ajouter_widget(Texte(a, "Port",
                                  position=(mx-20, my), ancrage=("droite", "centre"),
                                  taille_police=16))

        self.ajouter_widget(TexteEditable(a, "20092",
                                          position=(mx+20, my), ancrage=("gauche", "centre"),
                                          taille_police=16, couleur_curseur=(255, 255, 255, 255),
                                          largeur_min=50))

        self.ajouter_widget(Bouton(a, self.retour, texte="Retour",
                                   position=(mx-10, my-160), taille=(140, 50),
                                   ancrage=("droite", "centre"), taille_police=16))

        self.ajouter_widget(Bouton(a, self.confirmer, texte="Se connecter",
                                   position=(mx+10, my-160), taille=(140, 50),
                                   ancrage=("gauche", "centre"), taille_police=16))

    def confirmer(self):
        edittexte = self.widgets[3]

        if edittexte.texte.isdigit() \
                and "." not in edittexte.texte:
            self.jeu.initialiser_partie_serveur(int(edittexte.texte))
            self.jeu.lancer_boucle()
        else:
            self.afficher_message("Port invalide")

    def retour(self):
        self.jeu.initialiser_menu_multijoueur()


class MenuRejoindre(Menu):
    def creer(self):
        super().creer()

        a = self.jeu.affichage
        l, h = a.obtenir_taille()

        mx = l // 2
        my = h // 2
        mmy = h - my // 2

        self.ajouter_widget(Image(a, constantes.General.IMAGE_TITRE,
                                  position=(mx, mmy), taille=(400, 80),
                                  ancrage=("centre", "centre")))

        self.ajouter_widget(Texte(a, "Rejoindre",
                                  position=(mx, h*0.6), ancrage=("centre", "centre"),
                                  taille_police=18))

        self.ajouter_widget(Texte(a, "Adresse",
                                  position=(mx-20, my), ancrage=("droite", "centre"),
                                  taille_police=16))

        self.ajouter_widget(TexteEditable(a, "localhost",
                                          position=(mx+20, my), ancrage=("gauche", "centre"),
                                          taille_police=16, couleur_curseur=(255, 255, 255),
                                          largeur_min=50))

        self.ajouter_widget(Texte(a, "Port",
                                  position=(mx-20, my-40), ancrage=("droite", "centre"),
                                  taille_police=16))

        self.ajouter_widget(TexteEditable(a, "20092",
                                          position=(mx+20, my-40), ancrage=("gauche", "centre"),
                                          taille_police=16, couleur_curseur=(255, 255, 255),
                                          largeur_min=50))

        self.ajouter_widget(Bouton(a, self.retour, texte="Retour",
                                   position=(mx-10, my-160), taille=(140, 50),
                                   ancrage=("droite", "centre"), taille_police=16))

        self.ajouter_widget(Bouton(a, self.confirmer, texte="Se connecter",
                                   position=(mx+10, my-160), taille=(140, 50),
                                   ancrage=("gauche", "centre"), taille_police=16))

    def confirmer(self):
        edittexte_adresse = self.widgets[3]
        edittexte_port = self.widgets[5]

        if edittexte_port.texte.isdigit() \
                and "." not in edittexte_port.texte:
            self.jeu.initialiser_partie_client(edittexte_adresse.texte,
                                               int(edittexte_port.texte))
        else:
            self.afficher_message("Port invalide")

    def retour(self):
        self.jeu.initialiser_menu_multijoueur()


class MenuPause(Menu):
    def creer(self):
        super().creer()

        a = self.jeu.affichage
        l, h = a.obtenir_taille()

        mx = l // 2
        my = h // 2
        mmy = h - my // 2

        self.ajouter_widget(Image(a, constantes.General.IMAGE_TITRE,
                                  position=(mx, mmy), taille=(400, 80),
                                  ancrage=("centre", "centre")))

        self.ajouter_widget(Texte(a, "Pause", position=(mx, h*0.6),
                                  ancrage=("centre", "centre"), taille_police=18))

        self.ajouter_widget(Bouton(a, self.continuer, texte="Continuer",
                                   position=(mx, my), taille=(300, 50),
                                   ancrage=("centre", "centre"), taille_police=16))

        self.ajouter_widget(Bouton(a, self.retour,
                                   texte="Retour au menu principal", position=(mx, my-80),
                                   taille=(300, 50), ancrage=("centre", "centre"), taille_police=16))

    def continuer(self):
        self.jeu.geler_partie(False)

    def retour(self):
        self.jeu.arreter_partie()
        self.jeu.initialiser_menu_principal()


class MenuFin(Menu):
    def creer(self):
        super().creer()

        a = self.jeu.affichage
        niveau = self.jeu.niveau
        l, h = a.obtenir_taille()

        mx = l // 2
        my = h // 2
        mmy = h - my // 2

        self.ajouter_widget(Image(a, constantes.General.IMAGE_TITRE,
                                  position=(mx, mmy), taille=(400, 80),
                                  ancrage=("centre", "centre")))

        self.ajouter_widget(Texte(a, "Partie terminée",
                                  position=(mx, h*0.6), ancrage=("centre", "centre"),
                                  taille_police=18))

        self.ajouter_widget(Texte(a, "Pièces: {} | Temps: {}s"
                                  .format(niveau.pieces, round(niveau.temps_total)),
                                  position=(mx, my), ancrage=(
                                      "centre", "centre"),
                                  taille_police=16))

        self.ajouter_widget(Bouton(a, self.retour,
                                   texte="Retour au menu principal", position=(mx, my-80),
                                   taille=(300, 50), ancrage=("centre", "centre"), taille_police=16))

    def retour(self):
        self.jeu.arreter_partie()
        self.jeu.initialiser_menu_principal()
