import turtle
import random

# Configuration de la fenêtre
screen = turtle.Screen()
screen.title("Escape Game")
screen.bgcolor("lightblue")

# Création de l'agent du joueur
player = turtle.Turtle()
player.shape("turtle")
player.color("green")
player.penup()
player.speed(0)
player.goto(0, 0)

# Obstacle (la sortie)
exit = turtle.Turtle()
exit.shape("square")
exit.color("red")
exit.penup()
exit.goto(250, 250)

# Indices
indexes = ["Utilise la clé pour ouvrir la porte", "Trouve le mot de passe", "Résous l'énigme pour sortir"]
current_index = 0

# Fonction pour afficher l'énigme
def show_hint():
    global current_index
    if current_index < len(indexes):
        print(indexes[current_index])
        current_index += 1
    else:
        print("Félicitations ! Vous avez résolu toutes les énigmes.")

# Déplacement du joueur
def move_up():
    player.setheading(90)  # Haut
    player.forward(20)
    check_exit()

def move_down():
    player.setheading(270)  # Bas
    player.forward(20)
    check_exit()

def move_left():
    player.setheading(180)  # Gauche
    player.forward(20)
    check_exit()

def move_right():
    player.setheading(0)  # Droite
    player.forward(20)
    check_exit()

def check_exit():
    if player.distance(exit) < 20:
        print("Vous avez trouvé la sortie !")
        screen.bye()

# Écoute des touches
screen.listen()
screen.onkey(move_up, "Up")
screen.onkey(move_down, "Down")
screen.onkey(move_left, "Left")
screen.onkey(move_right, "Right")
screen.onkey(show_hint, "h")

# Boucle principale
screen.mainloop()
