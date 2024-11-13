import numpy as np
import os
import random
import platform

life = 1
sprite = '◊'

def gen_map(lignes=6, colonnes=20, proba_ennemi=0.5):
    return np.random.choice([0, 1], size=(lignes, colonnes), p=[proba_ennemi, 1 - proba_ennemi]).astype(object)

def deplacer_joueur(carte, direction, compteur_ennemis):
    global life
    position = np.argwhere(carte == sprite)
    if position.size == 0:
        print("Le joueur n'est pas présent sur la carte.")
        return carte, compteur_ennemis
    x, y = position[0]

    carte[x, y] = 0

    if direction == 'Z':  
        x = max(0, x - 1)
    elif direction == 'S': 
        x = min(carte.shape[0] - 1, x + 1)
    elif direction == 'Q':  
        y = max(0, y - 1)
    elif direction == 'D':
        y = min(carte.shape[1] - 1, y + 1)

    if carte[x, y] == 1:
        dice = random.randint(1, 6)
        if dice <= 3:
            life -= 1
            print("Vous avez perdu une vie !")
        else:
            compteur_ennemis += 1

    carte[x, y] = sprite
    return carte, x, y, life, compteur_ennemis

def jouer():
    global carte, life
    while True:
        carte = gen_map()
        carte[0, 0] = sprite
        life = 1
        compteur_ennemis = 0  

        while life >= 1:
            os.system('cls' if os.name == 'nt' else 'clear')

            print("Bienvenue dans le jeu de déplacement !")
            print("Utilisez Z pour monter, S pour descendre, Q pour aller à gauche, D pour aller à droite")
            print("Appuyez sur 'X' pour quitter le jeu.\n")
            for ligne in carte:
                print(*ligne)

            direction = input("Direction (Z/Q/S/D) : ").upper()

            if direction == 'X':
                print("Merci d'avoir joué !")
                return

            if direction in ['Z', 'Q', 'S', 'D']:
                carte, x, y, life, compteur_ennemis = deplacer_joueur(carte, direction, compteur_ennemis)
                print(f"Position actuelle du joueur : x = {x}, y = {y}")
            else:
                print("Direction invalide. Utilisez Z, Q, S, D pour vous déplacer.")
        print(f"Vous avez tué {compteur_ennemis} ennemis.")
        print("Vous avez perdu !")
        relancer = input("Relancer la partie ? (o/n) : ").lower()

        if relancer == 'o':
            continue 
        else:
            print("Merci d'avoir joué !")
            break 

jouer()
