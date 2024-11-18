from rich.pretty import pprint
import numpy as np
import os
import random

health = 1
message = "Bienvenue dans le jeu de déplacement !"
power = 6
sprite = '◊'
exit_char = '→'  # Flèche pour la sortie
treasure_char = '♦'  # Carré pour le coffre
boss_sprite = '☠'  # Sprite pour le boss
boss_killed = False  # Variable pour savoir si le boss a été tué

def gen_map(lignes=6, colonnes=20, proba_ennemi=0.5, proba_sante=0.01, proba_tresor=0.05):
    # On génère la carte avec des ennemis, des trésors, etc.
    carte = np.random.choice([' ', '+', 'ŏ', treasure_char], size=(lignes, colonnes), 
                             p=[proba_ennemi, proba_sante, 1 - proba_ennemi - proba_sante - proba_tresor, proba_tresor]).astype(object)
    
    # Ajoute les deux sorties à des positions fixes
    carte[lignes - 1, colonnes - 1] = exit_char  # Sortie 1 (en bas à droite)
    carte[0, colonnes - 1] = exit_char  # Sortie 2 (en haut à droite)

    # Ajout du boss sur la carte à une position aléatoire
    boss_x, boss_y = random.randint(0, lignes - 1), random.randint(0, colonnes - 1)
    while carte[boss_x, boss_y] == exit_char:  # Assure que le boss ne soit pas sur une sortie
        boss_x, boss_y = random.randint(0, lignes - 1), random.randint(0, colonnes - 1)
    carte[boss_x, boss_y] = boss_sprite

    return carte, (boss_x, boss_y)

carte, boss_position = gen_map()
carte[0, 0] = sprite

def loot():
    global power, message
    dice = random.randint(1, 10)
    if dice >= 3:
        power += 1
        message += "\nVous récupérez une meilleure arme. +1 puissance !"

def combat(power):
    global message
    dice = random.randint(1, power)
    if dice <= 3:
        message = "Vous avez perdu le combat contre l'ennemi."
        return False  # Défini que le combat est perdu
    else:
        message = "Combat remporté ! Vous avez vaincu l'ennemi."
        return True  # Défini que le combat est gagné

def boss_combat():
    global message, boss_killed
    message = "\nVous avez rencontré un boss ! Préparez-vous à un combat intense."
    dice = random.randint(1, power)
    if dice <= 4:  # Moins de chance de gagner contre le boss
        message = "Vous avez perdu contre le boss."
        return False  # Perdu contre le boss
    else:
        message = "Vous avez vaincu le boss !"
        loot()  # Récompense après avoir tué le boss
        boss_killed = True  # Le boss a été tué
        return True  # Gagné contre le boss

def move(carte, direction):
    global power, health, message, boss_killed, boss_position
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
        message = "\nVous avez rencontré un ennemi ! Préparez-vous à combattre."
        # Lancement du combat
        win = combat(power)
        if win:
            loot()  # Récupère un bonus de puissance après avoir gagné
        else:
            health -= 1  # Si perdu, on diminue la santé
            if health <= 0:
                message = "\nVous avez perdu toutes vos vies ! Fin de la partie."
                return carte, x, y, health
    elif carte[x, y] == '+':
        health += 1
        message = "\nVous trouvez un bonus de santé ! +1 vie."
    elif carte[x, y] == treasure_char:
        power += 2
        message = "\nVous trouvez un coffre ! +2 puissance."
    elif carte[x, y] == exit_char:
        # Condition de victoire : avoir 15 de puissance et avoir tué le boss
        if power >= 15 and boss_killed:
            message = "\nFélicitations ! Vous avez atteint la sortie avec une puissance suffisante et tué le boss. Vous avez gagné !"
            health = 0  # Met fin au jeu
        elif power >= 15:
            message = "\nVous avez trouvé la sortie, mais vous n'avez pas tué le boss. Vous devez tuer le boss pour sortir."
        else:
            message = "\nVous avez trouvé la sortie, mais vous n'êtes pas assez puissant pour l'ouvrir. Puissance requise : 15."
    elif carte[x, y] == boss_sprite:
        # Si le joueur rencontre le boss, on lance le combat spécial
        win = boss_combat()
        if not win:
            health -= 1  # Si perdu, on diminue la santé
            if health <= 0:
                message = "\nVous avez perdu contre le boss et perdu toutes vos vies ! Fin de la partie."
                return carte, x, y, health
        else:
            # Génère un nouveau boss si le joueur le tue
            boss_killed = False
            boss_x, boss_y = random.randint(0, carte.shape[0] - 1), random.randint(0, carte.shape[1] - 1)
            while carte[boss_x, boss_y] in [exit_char, sprite]:
                boss_x, boss_y = random.randint(0, carte.shape[0] - 1), random.randint(0, carte.shape[1] - 1)
            carte[boss_x, boss_y] = boss_sprite
            boss_position = (boss_x, boss_y)

    else:
        message = "Bienvenue dans le jeu de déplacement !"

    # Mise à jour de la nouvelle position du joueur
    carte[x, y] = sprite
    return carte, x, y, health

def jouer():
    global carte, health, message, power, boss_killed
    while True:
        while health >= 1:
            os.system('cls' if os.name == 'nt' else 'clear')

            print("Utilisez Z pour monter, S pour descendre, Q pour aller à gauche, D pour aller à droite")
            print("Appuyez sur 'X' pour quitter le jeu.\n")
            print(f"Puissance : {power}")
            print(f"Vie : {health}")
            # Affiche la carte actuelle
            for ligne in carte:
                print(*ligne)

            # Affiche le message en bas du jeu
            print("\n" + message)

            # Demande la direction à l'utilisateur
            direction = input("Direction (Z/Q/S/D) : ").upper()

            # Quitte si l'utilisateur entre 'X'
            if direction == 'X':
                print("Merci d'avoir joué !")
                return

            # Vérifie si la direction est valide
            if direction in ['Z', 'Q', 'S', 'D']:
                carte, x, y, health = move(carte, direction)
            else:
                message = "Direction invalide. Utilisez Z, Q, S, D pour vous déplacer."

        # Permet de rejouer si le joueur a perdu
        print("\n" + message)
        retry = input("Voulez-vous rejouer ? (O/N) : ").upper()
        if retry == 'O':
            # Réinitialise le jeu
            health = 1
            power = 6
            boss_killed = False  # Réinitialiser la condition du boss tué
            message = "Bienvenue dans le jeu de déplacement !"
            carte, boss_position = gen_map()
            carte[0, 0] = sprite
        else:
            print("Merci d'avoir joué ! À bientôt.")
            break

jouer()
