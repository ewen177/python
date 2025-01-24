import random

def introduction():
    print("Bienvenue dans l'escape game !")
    print("Vous êtes piégé dans un mystérieux manoir et devez résoudre des énigmes pour vous échapper.")
    print("Soyez attentif aux indices et oubliez de faire des choix prudents.\n")

def choix_salle():
    print("Vous êtes dans le hall d'entrée. Vous pouvez aller dans les salles suivantes :")
    print("1. Salle de bibliothèque")
    print("2. Salle du trésor")
    print("3. Salle des potions")
    print("4. Sortie (fuir impossible sans résoudre les énigmes !)")
    return input("Dans quelle salle voulez-vous aller (tapez 1, 2, 3, ou 4) ? ")

def enigme_bibliotheque():
    print("\nVous entrez dans la bibliothèque.")
    print("Il y a des livres partout. Un livre est légèrement en dehors de l'étagère.")
    print("Pour avancer, vous devez répondre à cette question :")
    print("Quel est le nombre d'os dans un corps humain adulte ?")
    
    reponse = input("Votre réponse : ")
    if reponse.strip() == "206":
        print("Correct ! Vous trouvez une clé. Vous pouvez maintenant sortir de la bibliothèque.")
        return True
    else:
        print("Incorrect ! Vous êtes piégé ici jusqu'à ce que vous trouviez la bonne réponse.")
        return False

def enigme_tresor():
    print("\nVous entrez dans la salle du trésor.")
    print("Il y a un coffre fort. Pour l'ouvrir, vous devez résoudre cette énigme :")
    print("Je commence par E et je finis par E, mais je n'ai qu'une lettre. Qu'est-ce que c'est ?")
    
    reponse = input("Votre réponse : ")
    if reponse.strip().lower() == "enveloppe":
        print("Bien joué ! Le coffre est ouvert et vous trouvez des pièces d'or.")
        return True
    else:
        print("Mauvaise réponse ! Le coffre se referme avec un bruit sourd.")
        return False

def enigme_potions():
    print("\nVous entrez dans la salle des potions.")
    print("Il y a trois potions devant vous : rouge, bleue, et verte.")
    print("Vous devez choisir la bonne potion pour avancer. Quel choix ferez-vous ? (rouge, bleue, verte)")
    
    choix = input("Votre choix : ").strip().lower()
    bonne_choix = random.choice(['rouge', 'bleue', 'verte'])  # Randomly determine which potion is correct
    if choix == bonne_choix:
        print("Bravo ! Vous avez choisi la bonne potion. Vous pouvez avancer.")
        return True
    else:
        print(f"Oups ! La potion {choix} était toxique. Vous êtes paralysé !")
        return False

def main():
    introduction()
    while True:
        salle = choix_salle()
        
        if salle == '1':
            if enigme_bibliotheque():
                print("Vous êtes sorti de la bibliothèque.")
            else:
                continue
        
        elif salle == '2':
            if enigme_tresor():
                print("Vous avez découvert le trésor.")
            else:
                continue
        
        elif salle == '3':
            if enigme_potions():
                print("Vous avez survécu à la salle des potions.")
            else:
                continue
        
        elif salle == '4':
            print("Vous essayez de fuir, mais vous devez d'abord résoudre les énigmes.")
            continue
        
        else:
            print("Choix invalide. Veuillez essayer à nouveau.")

        if all([enigme_bibliotheque(), enigme_tresor(), enigme_potions()]):
            print("Félicitations ! Vous avez réussi à résoudre toutes les énigmes et vous êtes libre !")
            break

if __name__ == "__main__":
    main()
