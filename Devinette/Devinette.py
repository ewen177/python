# guess the number game in Python by CodeSpeedy.com
import random
random_number = random.randint(1,100)
win = False
Turns =0
while win==False:
    Your_guess = input("Entre un nombre entre 1 et 100 : ")
    Turns +=1
    if random_number==int(Your_guess):
        print("Tu as gagné !")
        print("Nombre d'essais :",Turns)
        win == True
        break
    else:
     if random_number>int(Your_guess):
        print("Votre estimation était basse, veuillez saisir un nombre plus élevé")
     else:
        print("Votre estimation était trop haute, veuillez saisir un nombre plus faible")