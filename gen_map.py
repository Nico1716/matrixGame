import random


def generer_niveau():
    return random.choices([0, 1], k=20)


def traverse_niveau(niveau):
    vie = 1
    return all(vie := vie - (salle and random.randint(1, 6) <= 3) for salle in niveau)


def main():
    nb_niveau = 0

    while not traverse_niveau(generer_niveau()):
        nb_niveau += 1

    print(f"Nombre de niveaux travsersés: {nb_niveau}")


if __name__ == "__main__":
    main()

