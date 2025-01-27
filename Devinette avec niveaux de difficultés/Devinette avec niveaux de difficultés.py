import random

def choisir_difficulte():
    print("Choisissez un niveau de difficulté :")
    print("1 - Facile (10 tentatives)")
    print("2 - Moyen (7 tentatives)")
    print("3 - Difficile (5 tentatives)")

    while True:
        choix = input("Entrez votre choix (1, 2, ou 3) : ")
        if choix == '1':
            return 10  # Nombre de tentatives pour le niveau facile
        elif choix == '2':
            return 7   # Nombre de tentatives pour le niveau moyen
        elif choix == '3':
            return 5   # Nombre de tentatives pour le niveau difficile
        else:
            print("Choix invalide, veuillez entrer 1, 2, ou 3.")

def jouer():
    print("Bienvenue dans le jeu de devinette !")
    difficulte = choisir_difficulte()
    
    # Le programme génère un nombre entre 1 et 100
    nombre_a_deviner = random.randint(1, 100)
    
    print(f"\nVous devez deviner un nombre entre 1 et 100.")
    print(f"Vous avez {difficulte} tentatives.")
    
    tentatives = 0
    while tentatives < difficulte:
        tentatives += 1
        try:
            guess = int(input(f"Tentative {tentatives}/{difficulte} - Entrez votre supposition : "))
        except ValueError:
            print("Veuillez entrer un nombre valide.")
            continue
        
        if guess < nombre_a_deviner:
            print("Trop bas !")
        elif guess > nombre_a_deviner:
            print("Trop haut !")
        else:
            print(f"Bravo ! Vous avez deviné le bon nombre {nombre_a_deviner} en {tentatives} tentatives.")
            break
    else:
        print(f"Dommage, vous avez épuisé vos tentatives. Le nombre à deviner était {nombre_a_deviner}.")

if __name__ == "__main__":
    jouer()