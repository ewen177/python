import turtle
import random

# Configuration de la fenêtre
screen = turtle.Screen()
screen.title("Escape Game avec Sauts")
screen.bgcolor("black")
screen.setup(width=700, height=700)

# Désactivation des animations pour des performances plus fluides
screen.tracer(0)

# Variables globales
cell_size = 24
walls = []
exit_position = (0, 0)

# Création du joueur
player = turtle.Turtle()
player.shape("turtle")
player.color("green")
player.penup()
player.speed(0)

# Classe pour le labyrinthe
class Labyrinth(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)

    def build_walls(self, maze):
        global exit_position
        for y in range(len(maze)):
            for x in range(len(maze[y])):
                character = maze[y][x]
                screen_x = -300 + (x * cell_size)
                screen_y = 300 - (y * cell_size)

                if character == "X":
                    self.goto(screen_x, screen_y)
                    self.stamp()
                    walls.append((screen_x, screen_y))

                if character == "P":
                    player.goto(screen_x, screen_y)

                if character == "E":
                    exit_position = (screen_x, screen_y)
                    self.goto(screen_x, screen_y)
                    self.color("gold")
                    self.stamp()
                    self.color("white")

# Labyrinthe avec des obstacles (X = mur, P = position de départ, E = sortie)
maze = [
    "XXXXXXXXXXXXXXXXXXXXX",
    "XP        X     X   X",
    "X  XXXX   X  X  X   X",
    "X  X      X  X  XXXX",
    "X  X   X  X  X     XX",
    "X  XXX X  XXXXX  X  X",
    "X     X     X    X  X",
    "X XXXX XXXXX X XXXXXE",
    "X     X      X      X",
    "XXXXXXXXXXXXXXXXXXXXX"
]

# Création et affichage du labyrinthe
labyrinth = Labyrinth()
labyrinth.build_walls(maze)

# Mouvements du joueur
def move_up():
    move_player(0, cell_size)

def move_down():
    move_player(0, -cell_size)

def move_left():
    move_player(-cell_size, 0)

def move_right():
    move_player(cell_size, 0)

# Saut du joueur par-dessus un obstacle
def jump():
    dx = 0
    dy = 0
    if player.heading() == 90:  # Haut
        dy = cell_size * 2
    elif player.heading() == 270:  # Bas
        dy = -cell_size * 2
    elif player.heading() == 180:  # Gauche
        dx = -cell_size * 2
    elif player.heading() == 0:  # Droite
        dx = cell_size * 2
    move_player(dx, dy)

# Fonction pour déplacer le joueur
def move_player(dx, dy):
    new_x = player.xcor() + dx
    new_y = player.ycor() + dy

    if (new_x, new_y) not in walls:  # Vérification pour ne pas traverser un mur
        player.goto(new_x, new_y)
        check_for_exit()

# Vérifier si le joueur a atteint la sortie
def check_for_exit():
    if player.distance(exit_position) < 20:
        display_message("Félicitations, vous avez échappé !")
        screen.bye()  # Ferme le jeu

# Texte pour afficher des messages
message_writer = turtle.Turtle()
message_writer.penup()
message_writer.hideturtle()
message_writer.color("white")
message_writer.goto(0, 320)

# Fonction pour afficher des messages
def display_message(message):
    message_writer.clear()
    message_writer.write(message, align="center", font=("Arial", 16, "normal"))

# Ajouter les touches pour déplacer et sauter
screen.listen()
screen.onkey(move_up, "Up")
screen.onkey(move_down, "Down")
screen.onkey(move_left, "Left")
screen.onkey(move_right, "Right")
screen.onkey(jump, "space")  # La barre d'espace permet de sauter

# Boucle principale
while True:
    screen.update()
