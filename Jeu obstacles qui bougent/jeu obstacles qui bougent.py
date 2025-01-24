import turtle
import random
import time

# Configuration de l'écran
wn = turtle.Screen()
wn.title("Jeu de Dodger de Tortue")
wn.bgcolor("black")
wn.setup(width=600, height=600)

# Tortue du joueur
player = turtle.Turtle()
player.shape("turtle")
player.color("green")
player.penup()
player.speed(0)
player.goto(0, -250)
player.setheading(90)

# Liste pour stocker les objets tombants
falling_objects = []
num_objects = 5  # Nombre d'objets tombants
for _ in range(num_objects):
    obj = turtle.Turtle()
    obj.shape("circle")
    obj.color("red")
    obj.penup()
    obj.speed(0)
    obj.goto(random.randint(-290, 290), random.randint(100, 300))
    falling_objects.append(obj)

# Variables du jeu
score = 0
game_over = False

# Fonctions de mouvement
def move_left():
    x = player.xcor()
    if x > -290:  # Limite gauche
        x -= 20
    player.setx(x)

def move_right():
    x = player.xcor()
    if x < 290:  # Limite droite
        x += 20
    player.setx(x)

# Lier les touches
wn.listen()
wn.onkeypress(move_left, "Left")
wn.onkeypress(move_right, "Right")

# Boucle principale du jeu
while not game_over:
    for obj in falling_objects:
        obj.sety(obj.ycor() - 15)  # Descendre l'objet
        # Réinitialiser l'objet en haut de l'écran
        if obj.ycor() < -300:
            obj.goto(random.randint(-290, 290), random.randint(100, 300))
            score += 1  # Augmenter le score
        
        # Vérifier les collisions
        if player.distance(obj) < 20:
            game_over = True
            break

    wn.update()  # Mettre à jour l'écran
    time.sleep(0.05)  # Réduire la vitesse du jeu

# Afficher le score final
player.goto(0, 0)
player.write("Game Over! Score: {}".format(score), align="center", font=("Courier", 24, "normal"))

# Fermeture de la fenêtre après un clic
wn.exitonclick()
