from rich.pretty import pprint
import numpy as np
import os
import random
import platform


life = 1

sprite = '◊'

def gen_map(lignes=6, colonnes=20, proba_ennemi=0.5):
    return np.random.choice([0, 1], size=(lignes, colonnes), p=[proba_ennemi, 1 - proba_ennemi]).astype(object)

carte = gen_map()

carte[0, 0] = sprite

print(carte)

def deplacer_joueur(carte, direction):
    # Localisation actuelle du joueur
    global life
    position = np.argwhere(carte == sprite)
    if position.size == 0:
        print("Le joueur n'est pas présent sur la carte.")
        return carte
    x, y = position[0]

    # Efface l'ancienne position du joueur
    carte[x, y] = 0

    # Calcul de la nouvelle position en fonction de la direction
    if direction == 'Z':  # Haut
        x = max(0, x - 1)
    elif direction == 'S':  # Bas
        x = min(carte.shape[0] - 1, x + 1)
    elif direction == 'Q':  # Gauche
        y = max(0, y - 1)
    elif direction == 'D':  # Droite
        y = min(carte.shape[1] - 1, y + 1)
    # Place le joueur dans la nouvelle position
    if carte[x, y] == 1:
        dice = random.randint(1, 6)
        if dice <= 3:
            life -= 1
    carte[x, y] = sprite
    return carte, x, y, life



def combat():
    dice = random.randint(1, 6)
    if dice <= 3:
        life = life - 1

def jouer():
    global carte, life
    while life >= 1:

        os.system('cls' if os.name == 'nt' else 'clear')

        print("Bienvenue dans le jeu de déplacement !")
        print("Utilisez Z pour monter, S pour descendre, Q pour aller à gauche, D pour aller à droite")
        print("Appuyez sur 'X' pour quitter le jeu.\n")
        # Affiche la carte actuelle
        # print(carte)
        for ligne in carte :
            print(*ligne)

        # Demande la direction à l'utilisateur
        direction = input("Direction (Z/Q/S/D) : ").upper()

        # Quitte si l'utilisateur entre 'X'
        if direction == 'X':
            print("Merci d'avoir joué !")
            break

        # Vérifie si la direction est valide
        if direction in ['Z', 'Q', 'S', 'D']:
            carte, x, y, life = deplacer_joueur(carte, direction)
            print(f"Position actuelle du joueur : x = {x}, y = {y}")
        else:
            print("Direction invalide. Utilisez Z, Q, S, D pour vous déplacer.")
    print("perdu, gros tas.")
# Lancer le jeu
jouer()