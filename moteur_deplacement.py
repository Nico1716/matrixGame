from rich.pretty import pprint
import numpy as np
import os
import random
import platform

# map details
lignes=6
colonnes=20


health = 1
message = "C'est votre Baptême du Sang ! Tuez un \x1b[1;31mBoss\x1b[0m et devenez un vrai guerrier !" # toutes les fonctions chelous comme ça sont pour la couleur + gras
power = 6
luck = 1

hero = "\x1b[1;36m◊\x1b[0m" 
enemy = 'ŏ'
boss = "\x1b[1;31mŎ\x1b[0m"  
health_char = "\x1b[1;35m+\x1b[0m"  
exit_char = "\x1b[1;32m→\x1b[0m" 
treasure_char = "\x1b[1;33m�\x1b[0m"
boss_killed = False  # Variable pour savoir si le boss a été tué

def spawn_boss(x=0, y=0):
    global carte, lignes, colonnes
    boss_x, boss_y = random.randint(0, lignes - 1), random.randint(0, colonnes - 1)
    while carte[boss_x, boss_y] == exit_char or carte[boss_x, boss_y] == hero:  # Assure que le boss ne soit pas sur une sortie
        boss_x, boss_y = random.randint(0, lignes - 1), random.randint(0, colonnes - 1)
    carte[boss_x, boss_y] = boss
    return carte, (boss_x, boss_y)

def gen_map(lignes=6, colonnes=20, proba_ennemi=0.5, proba_sante=0.01, proba_tresor=0.05):
    # On génère la carte avec des ennemis, des trésors, etc.
    carte = np.random.choice([' ', health_char, enemy, treasure_char], size=(lignes, colonnes), 
    p=[proba_ennemi, proba_sante, 1 - proba_ennemi - proba_sante - proba_tresor, proba_tresor]).astype(object)
    
    # Ajoute les deux sorties à des positions fixes
    carte[lignes - 1, colonnes - 1] = exit_char  # Sortie 1 (en bas à droite)
    carte[0, colonnes - 1] = exit_char  # Sortie 2 (en haut à droite)

    # Ajout du boss sur la carte à une position aléatoire
    

    return carte

carte = gen_map(lignes, colonnes)

carte, boss_position = spawn_boss()
carte[0, 0] = hero

print(carte)

def loot(luck, chest=False):
    global power, message
    dice = random.randint(1, max(1, 11 - luck)) # au cas où quelqu'un vaincrait plus de 10 boss
    if dice <= 3 or chest:
        bonus = 1 + random.randint(0, luck)
        power += bonus
        message += " Vous récupérez une meilleure arme. + " + f"{bonus} \x1b[1;33mpuissance\x1b[0m !"

def combat(power):
    global message
    dice = random.randint(1, power)
    if dice <= 3:
        message = "Combat perdu. -1 \x1b[1;35mvie\x1b[0m."
        return False  # Défini que le combat est perdu
    else:
        message = "Combat remporté !"
        return True  # Défini que le combat est gagné

def boss_combat(power):
    global message, boss_killed, luck
    dice = random.randint(1, power)
    if dice <= 4:  # Moins de chance de gagner contre le boss
        message = "Vous avez perdu contre le \x1b[1;31mBoss\x1b[0m."
        return False
    else:
        message = "Vous avez vaincu le \x1b[1;31mBoss\x1b[0m !"
        luck += 1
        loot(luck)  # Récompense après avoir tué le boss
        boss_killed = True  # Le boss a été tué
        return True

def move(carte, direction):
    global power, health, message, boss_killed, boss_position, luck
    position = np.argwhere(carte == hero)
    if position.size == 0:
        print("Le joueur n'est pas présent sur la carte.")
        return carte
    x, y = position[0]

    # Efface l'ancienne position du joueur
    carte[x, y] = ' '

    # Calcul de la nouvelle position en fonction de la direction
    if direction == 'Z':  
        x = max(0, x - 1) # Collisions de bord de carte
    elif direction == 'S': 
        x = min(carte.shape[0] - 1, x + 1)
    elif direction == 'Q':
        y = max(0, y - 1)
    elif direction == 'D':
        y = min(carte.shape[1] - 1, y + 1)
        
    # Gestion de la case cible
    if carte[x, y] == enemy:
        message = "Vous avez rencontré un ennemi ! Préparez-vous à combattre."
        # Lancement du combat
        win = combat(power)
        if win:
            loot(luck)
        else:
            health -= 1  # Si perdu, on diminue la santé
            if health <= 0:
                message = "Vous avez perdu toutes vos \x1b[1;35mvies\x1b[0m ! Fin de la partie."
                return carte, x, y, health
    elif carte[x, y] == health_char:
        bonus = random.randint(1, luck)
        health += bonus
        message = "Vous trouvez un bonus de santé ! + " + f"{bonus} \x1b[1;35mvie\x1b[0m."
    elif carte[x, y] == treasure_char:
        message = "Vous trouvez un coffre !"
        loot(luck, True)
    elif carte[x, y] == exit_char:
        # Condition de victoire : avoir 15 de puissance et avoir tué le boss
        if power >= 15 and boss_killed:
            message = "Félicitations ! Vous avez atteint la \x1b[1;32msortie\x1b[0m avec une \x1b[1;33mpuissance\x1b[0m suffisante et tué le \x1b[1;31mBoss\x1b[0m. Vous avez gagné !"
            health = 0  # Met fin au jeu
        elif power >= 15:
            message = "Vous avez trouvé la \x1b[1;32msortie\x1b[0m, mais vous n'avez pas accompli votre objectif. Revenez quand vous le mériterez."
        else:
            message = "Vous avez trouvé la \x1b[1;32msortie\x1b[0m, mais vous n'êtes pas assez puissant pour l'ouvrir. \x1b[1;33mPuissance\x1b[0m requise : 15."
        carte[carte.shape[0] - 1 - x, y] = exit_char # s'assure que l'autre sortie existe
    elif carte[x, y] == boss:
        # Si le joueur rencontre le boss, on lance le combat spécial
        win = boss_combat(power)
        if not win:
            health -= 1  # Si perdu, on diminue la santé
            if health <= 0:
                message = "Vous avez perdu contre le \x1b[1;31mBoss\x1b[0m et perdu toutes vos \x1b[1;35mvies\x1b[0m ! Fin de la partie."
                return carte, x, y, health
        
        # Génère un nouveau boss après un combat
        carte, boss_position = spawn_boss(x, y)

    else:
        message = "Continuez à avancer !"
        
    # Mise à jour de la nouvelle position du joueur
    carte[x, y] = hero
    return carte, x, y, health

def jouer():
    global carte, health, message, power, boss_killed, luck
    while True:
        while health >= 1:
            os.system('cls' if os.name == 'nt' else 'clear')

            print("Appuyez sur 'X' pour quitter le jeu.\n")
            print(f"\x1b[1;33mPuissance\x1b[0m" + f" : {power}")
            print(f"\x1b[1;35mVie\x1b[0m" + f" : {health}")
            if boss_killed:
                print(f"\x1b[1;31mBoss\x1b[0m vaincu ! Plus qu'à \x1b[1;32msortir\x1b[0m...")
            else: 
                print(f"Vous devez prouver votre valeur...")
            
            # Affiche la carte actuelle (sans les '')
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
            luck = 1
            boss_killed = False  # Réinitialiser la condition du boss tué
            message = "C'est votre Baptême du Sang ! Tuez un \x1b[1;31mBoss\x1b[0m et devenez un vrai \x1b[1;36mHéros\x1b[0m !"
            carte = gen_map()
            carte, boss_position = spawn_boss()
            carte[0, 0] = hero
        else:
            print("Merci d'avoir joué ! À bientôt.")
            break

jouer()