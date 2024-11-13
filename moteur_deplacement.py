from rich.pretty import pprint
import numpy as np


carte = np.array([
    [0, 0, 0],
    [0, 9, 0],
    [0, 0, 0]
])
print(carte)

def deplacer_joueur(carte, direction):
    # Localisation actuelle du joueur
    position = np.argwhere(carte == 9)
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
    carte[x, y] = 9
    return carte, x, y

def jouer():
    print("Bienvenue dans le jeu de déplacement !")
    print("Utilisez Z pour monter, S pour descendre, Q pour aller à gauche, D pour aller à droite")
    print("Appuyez sur 'X' pour quitter le jeu.\n")
    global carte
    while True:
        # Affiche la carte actuelle
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print(carte)

        # Demande la direction à l'utilisateur
        direction = input("Direction (Z/Q/S/D) : ").upper()

        # Quitte si l'utilisateur entre 'X'
        if direction == 'X':
            print("Merci d'avoir joué !")
            break

        # Vérifie si la direction est valide
        if direction in ['Z', 'Q', 'S', 'D']:
            carte, x, y = deplacer_joueur(carte, direction)
            print(f"Position actuelle du joueur : x = {x}, y = {y}")
        else:
            print("Direction invalide. Utilisez Z, Q, S, D pour vous déplacer.")

# Lancer le jeu
jouer()