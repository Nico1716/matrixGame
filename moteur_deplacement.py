from rich.pretty import pprint
import numpy as np
import os
import random
import platform

health = 1
message = "Bienvenue dans le jeu de déplacement !"
power = 6
sprite = '◊'
exit_symbol = 'X'

def gen_map(lignes=6, colonnes=20, proba_ennemi=0.5, proba_sante=0.01):
    carte = np.random.choice([' ', '+', 'ŏ'], size=(lignes, colonnes), p=[proba_ennemi, proba_sante, 1 - proba_ennemi - proba_sante]).astype(object)
    carte[lignes-1, colonnes-1] = exit_symbol 
    return carte

def loot():
    global power, message
    dice = random.randint(1, 10)
    if dice >= 3:
        power += 1
        message += " Vous récupérez une meilleure arme. +1 puissance !"

def combat(power):
    global message
    dice = random.randint(1, power)
    if dice <= 3:
        message = "Perdu, gros tas."
        return False
    else:
        message = "Combat remporté !"
        return True

def move(carte, direction):
    global power, health, message
    position = np.argwhere(carte == sprite)
    if position.size == 0:
        print("Le joueur n'est pas présent sur la carte.")
        return carte, health
    x, y = position[0]

    carte[x, y] = ' '

    if direction == 'Z':  
        x = max(0, x - 1)
    elif direction == 'S':  
        x = min(carte.shape[0] - 1, x + 1)
    elif direction == 'Q':  
        y = max(0, y - 1)
    elif direction == 'D':  
        y = min(carte.shape[1] - 1, y + 1)

    if carte[x, y] == 'ŏ':
        win = combat(power)
        if win:
            loot()
        else:
            health -= 1
            if health <= 0:
                message = "Vous avez perdu toutes vos vies ! Fin de la partie."
                return carte, health
    elif carte[x, y] == '+':
        health += 1
        message = "Vous trouvez un bonus de santé ! +1 vie."
    elif carte[x, y] == exit_symbol:
        if power >= 10:
            message = "Félicitations ! Vous avez atteint la sortie avec suffisamment de puissance. Vous avez gagné !"
            health = 0
        else:
            message = "Vous avez trouvé la sortie, mais il vous faut au moins 10 de puissance pour gagner !"

    carte[x, y] = sprite
    return carte, health

def jouer():
    global carte, health, message, power
    rejouer = True
    while rejouer:
        health = 1
        power = 6
        carte = gen_map()
        carte[0, 0] = sprite
        message = "Bienvenue dans le jeu de déplacement !"
        
        while health >= 1:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(message)
            print("Utilisez Z pour monter, S pour descendre, Q pour aller à gauche, D pour aller à droite")
            print("Appuyez sur 'X' pour quitter le jeu.\n")
            print(f"Puissance : {power}")
            print(f"Vie : {health}")

            for ligne in carte:
                print(*ligne)

            direction = input("Direction (Z/Q/S/D) : ").upper()
            if direction == 'X':
                print("Merci d'avoir joué !")
                break

            if direction in ['Z', 'Q', 'S', 'D']:
                carte, health = move(carte, direction)
            else:
                print("Direction invalide. Utilisez Z, Q, S, D pour vous déplacer.")
        
        print(message)
        rejouer = input("Voulez-vous rejouer ? (O/N) : ").upper() == 'O'

jouer()
