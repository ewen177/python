import time
import random
import string
import webbrowser
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Fonction pour générer un CAPTCHA sous forme d'image avec tkinter
def generate_captcha():
    captcha_text = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    # Créer une image blanche de fond
    canvas_width, canvas_height = 200, 60
    captcha_image = tk.Canvas(width=canvas_width, height=canvas_height, bg='white')
    
    # Ajouter du bruit à l'image (lignes et points)
    for _ in range(random.randint(5, 10)):  # Ajouter des lignes
        x1, y1 = random.randint(0, canvas_width), random.randint(0, canvas_height)
        x2, y2 = random.randint(0, canvas_width), random.randint(0, canvas_height)
        captcha_image.create_line(x1, y1, x2, y2, fill=random.choice(['red', 'blue', 'green', 'black']), width=1)

    for _ in range(random.randint(50, 100)):  # Ajouter des points
        x, y = random.randint(0, canvas_width), random.randint(0, canvas_height)
        captcha_image.create_oval(x, y, x+2, y+2, fill=random.choice(['red', 'blue', 'green', 'black']))

    # Ajouter le texte du CAPTCHA avec une rotation aléatoire
    for i, char in enumerate(captcha_text):
        font_size = random.randint(20, 30)
        angle = random.randint(-30, 30)  # Rotation aléatoire pour chaque caractère
        x = (i + 1) * (canvas_width // 7)
        y = canvas_height // 2

        captcha_image.create_text(x, y, text=char, font=("Arial", font_size), angle=angle)

    return captcha_text, captcha_image

# Fonction pour vérifier le CAPTCHA
def verifier_captcha(captcha, saisie_utilisateur):
    return captcha == saisie_utilisateur

# Fonction pour afficher la barre de progression fluide avec le message "Veuillez patienter"
def afficher_barre_progression():
    # Créer la fenêtre pour la barre de progression
    root = tk.Tk()
    root.title("Barre de Progression")

    # Créer la barre de progression
    barre_progression = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
    barre_progression.pack(pady=20)

    # Créer un label pour afficher le pourcentage
    label = tk.Label(root, text="0%", font=("Arial", 12))
    label.pack()

    # Créer un label pour afficher le message "Veuillez patienter"
    message_label = tk.Label(root, text="Veuillez patienter...", font=("Arial", 12))
    message_label.pack(pady=10)

    # Mettre à jour la barre de progression et le message
    for i in range(101):
        time.sleep(0.05)  # Ralentir la progression pour la rendre plus fluide
        barre_progression["value"] = i  # Mettre à jour la valeur de la barre
        label.config(text=f"{i}%")  # Mettre à jour le label
        message_label.config(text=f"Veuillez patienter... {i}%")
        root.update_idletasks()  # Mettre à jour l'interface graphique

    # Fermer la fenêtre après la fin de la barre de progression
    root.destroy()

    # Ouvrir une fenêtre dans le navigateur
    webbrowser.open("https://www.example.com")

# Fonction pour afficher la fenêtre CAPTCHA
def afficher_fenetre_captcha(captcha_text):
    # Créer une fenêtre secondaire juste pour le CAPTCHA
    captcha_window = tk.Toplevel()
    captcha_window.title("Vérification CAPTCHA")

    # Créer un frame pour contenir la saisie de l'utilisateur et l'image du CAPTCHA
    frame = tk.Frame(captcha_window)
    frame.pack(padx=20, pady=20)

    # Champ de texte pour la saisie de l'utilisateur
    captcha_entry = tk.Entry(frame, font=("Arial", 15))
    captcha_entry.grid(row=0, column=1, padx=10)

    # Créer un frame pour afficher l'image du CAPTCHA
    captcha_frame = tk.Frame(captcha_window)
    captcha_frame.pack(side="left", padx=20)

    # Ajouter un label pour l'image CAPTCHA
    captcha_label = tk.Label(captcha_frame, text="Veuillez entrer le code suivant :", font=("Arial", 12))
    captcha_label.pack(pady=10)

    # Afficher l'image du CAPTCHA dans un Canvas
    captcha_image = tk.Canvas(captcha_window, width=200, height=60, bg="white")
    for i, char in enumerate(captcha_text):
        font_size = random.randint(20, 30)
        angle = random.randint(-30, 30)  # Rotation aléatoire pour chaque caractère
        x = (i + 1) * 30
        y = 30
        captcha_image.create_text(x, y, text=char, font=("Arial", font_size), angle=angle)

    captcha_image.pack(pady=10)

    # Fonction pour vérifier la saisie et lancer la barre de progression
    def verifier_et_lancer():
        saisie_utilisateur = captcha_entry.get()
        if verifier_captcha(captcha_text, saisie_utilisateur):
            captcha_window.destroy()  # Fermer la fenêtre CAPTCHA
            afficher_barre_progression()  # Lancer la barre de progression
        else:
            messagebox.showerror("Erreur CAPTCHA", "Le code saisi est incorrect. Essayez à nouveau.")
            captcha_entry.delete(0, tk.END)  # Effacer le champ de saisie

    # Bouton pour vérifier le CAPTCHA
    valider_button = tk.Button(frame, text="Valider", command=verifier_et_lancer)
    valider_button.grid(row=1, column=1, pady=10)

    captcha_window.mainloop()

# Fonction principale
def programme_principal():
    # Générer un CAPTCHA
    captcha_text, _ = generate_captcha()

    # Lancer la fenêtre du CAPTCHA
    afficher_fenetre_captcha(captcha_text)

# Lancer le programme principal
programme_principal()