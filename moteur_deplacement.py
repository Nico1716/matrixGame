from rich.pretty import pprint
import numpy as np
import os
import random
import platform


health = 1
message = "Bienvenue dans le jeu de déplacement !"
power = 6

sprite = '◊'

def gen_map(lignes=6, colonnes=20, proba_ennemi=0.5, proba_sante=0.01):
    return np.random.choice([' ', '+', 'ŏ'], size=(lignes, colonnes), p=[proba_ennemi, proba_sante, 1 - proba_ennemi - proba_sante]).astype(object)

carte = gen_map()

carte[0, 0] = sprite

print(carte)

def loot():
    global power, message
    dice = random.randint(1, 10)
    if dice >= 3:
        power += 1
        message += " Vous récupérez une meilleure arme. + 1 puissance !"

def combat(power):
    global message
    dice = random.randint(1, power)
    if dice <= 3:
        message = "Perdu, gros tas."
        return False  # Défini que le combat est perdu
    else:
        message = "Combat remporté !"
        return True  # Défini que le combat est gagné

def move(carte, direction):
    global power, health, message
    position = np.argwhere(carte == sprite)
    if position.size == 0:
        print("Le joueur n'est pas présent sur la carte.")
        return carte
    x, y = position[0]

    # Efface l'ancienne position du joueur
    carte[x, y] = ' '

    # Calcul de la nouvelle position en fonction de la direction
    if direction == 'Z':  # Haut
        x = max(0, x - 1)
    elif direction == 'S':  # Bas
        x = min(carte.shape[0] - 1, x + 1)
    elif direction == 'Q':  # Gauche
        y = max(0, y - 1)
    elif direction == 'D':  # Droite
        y = min(carte.shape[1] - 1, y + 1)
        
    # Gestion de la case cible
    if carte[x, y] == 'ŏ':
        # Lancement du combat
        win = combat(power)
        if win:
            loot()
        else:
            health -= 1  # Si perdu, on diminue la santé
            if health <= 0:
                message = "Vous avez perdu toutes vos vies ! Fin de la partie."
                return carte, x, y, health
    elif carte[x, y] == '+':
        health += 1
        message = "Vous trouvez un bonus de santé ! +1 vie."
    else:
        message = "Bienvenue dans le jeu de déplacement !"
        
    # Mise à jour de la nouvelle position du joueur
    carte[x, y] = sprite
    return carte, x, y, health

def jouer():
    global carte, health, message, power
    while health >= 1:

        os.system('cls' if os.name == 'nt' else 'clear')

        print(message)
        print("Utilisez Z pour monter, S pour descendre, Q pour aller à gauche, D pour aller à droite")
        print("Appuyez sur 'X' pour quitter le jeu.\n")
        print(f"Puissance : {power}")
        print(f"Vie : {health}")
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
            carte, x, y, health = move(carte, direction)
        else:
            print("Direction invalide. Utilisez Z, Q, S, D pour vous déplacer.")
    print(message)
# Lancer le jeu
jouer()