import turtle
import random

# Liste de mots à deviner
words = ["routeur", "objectif", "exclure", "utilisation", "rouler", "hamburger", "sauterelle", "brouillard", "milkshake", "perplexe", "force", "hésiter", "causer", "baleine", "absent", "table", "mousse", "formater", "obtenir", "transpercer", "coccinelle", "pente", "réexaminer"]

# Choisir un mot aléatoire
word_to_guess = random.choice(words)
guessed_letters = []
attempts_remaining = 6

# Configuration de la fenêtre Turtle
screen = turtle.Screen()
screen.title("Jeu du Pendu")
screen.setup(width=600, height=400)

# Fonctions pour dessiner le bonhomme pendu
def draw_hangman(attempts):
    turtle.reset()
    turtle.penup()
    turtle.goto(-100, 100)
    turtle.pendown()
    turtle.forward(150)  # Base
    turtle.right(90)
    turtle.forward(300)  # Poteau
    turtle.right(90)
    turtle.forward(50)    # Travers
    turtle.right(90)
    turtle.forward(50)    # Support au dessus
    turtle.right(90)
    turtle.forward(50)    # Haut de la tête
    
    if attempts < 6:
        turtle.penup()
        turtle.goto(-75, 215)
        turtle.pendown()
        turtle.circle(15)  # Tête
    if attempts < 5:
        turtle.penup()
        turtle.goto(-75, 200)
        turtle.pendown()
        turtle.right(90)
        turtle.forward(50)  # Corps
    if attempts < 4:
        turtle.penup()
        turtle.goto(-75, 175)
        turtle.pendown()
        turtle.left(45)
        turtle.forward(30)  # Bras gauche
        turtle.penup()
        turtle.goto(-75, 175)
        turtle.right(90)
        turtle.pendown()
        turtle.forward(30)  # Bras droit
    if attempts < 3:
        turtle.penup()
        turtle.goto(-75, 125)
        turtle.pendown()
        turtle.left(135)
        turtle.forward(30)  # Jambe gauche
        turtle.penup()
        turtle.goto(-75, 125)
        turtle.right(90)
        turtle.pendown()
        turtle.forward(30)  # Jambe droite

def display_word():
    turtle.penup()
    turtle.goto(50, 150)
    turtle.pendown()
    output = ''
    for letter in word_to_guess:
        if letter in guessed_letters:
            output += letter + ' '
        else:
            output += '_ '
    turtle.write(output, font=("Arial", 24, "normal"))

# Boucle principale du jeu
while attempts_remaining > 0:
    draw_hangman(attempts_remaining)
    display_word()
    
    guess = screen.textinput("Devinez une lettre", "Entrez une lettre:")
    if guess is not None and len(guess) == 1 and guess.isalpha():
        guess = guess.lower()
        
        if guess in guessed_letters:
            turtle.write("Vous avez déjà deviné cette lettre.", font=("Arial", 16, "normal"))
        elif guess in word_to_guess:
            guessed_letters.append(guess)
            turtle.write("Correct !", font=("Arial", 16, "normal"))
        else:
            guessed_letters.append(guess)
            attempts_remaining -= 1
            turtle.write("Incorrect !", font=("Arial", 16, "normal"))
    else:
        turtle.write("Input invalide. Essayez encore.", font=("Arial", 16, "normal"))

    # Vérifiez si le mot a été complété
    if all(letter in guessed_letters for letter in word_to_guess):
        turtle.penup()
        turtle.goto(50, -50)
        turtle.write("Vous avez gagné ! Le mot était : " + word_to_guess, font=("Arial", 24, "normal"))
        break

if attempts_remaining == 0:
    draw_hangman(attempts_remaining)
    turtle.penup()
    turtle.goto(50, -50)
    turtle.write("Vous avez perdu ! Le mot était : " + word_to_guess, font=("Arial", 24, "normal"))

turtle.done()
