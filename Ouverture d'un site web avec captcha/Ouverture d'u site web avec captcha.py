import time
import random
import string
import webbrowser
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Fonction pour générer un CAPTCHA aléatoire
def generate_captcha():
    # Générer un texte aléatoire de 6 caractères
    captcha = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    return captcha

# Fonction pour vérifier le CAPTCHA
def verifier_captcha(captcha, saisie_utilisateur):
    if captcha == saisie_utilisateur:
        return True
    else:
        return False

# Fonction pour afficher la barre de progression avec le message "Veuillez patienter"
def afficher_barre_progression():
    # Créer la fenêtre principale
    root = tk.Tk()
    root.title("Barre de Progression")
    
    # Créer la barre de progression
    barre_progression = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
    barre_progression.pack(pady=20)
    
    # Créer un label pour afficher le pourcentage
    label = tk.Label(root, text="0%")
    label.pack()
    
    # Créer un label pour afficher le message "Veuillez patienter"
    message_label = tk.Label(root, text="Veuillez patienter...", font=("Arial", 12))
    message_label.pack(pady=10)
    
    # Mettre à jour la barre de progression et le message
    for i in range(101):
        time.sleep(0.1)  # Ralentir la progression
        barre_progression["value"] = i  # Mettre à jour la valeur de la barre
        label.config(text=f"{i}%")  # Mettre à jour le label
        root.update_idletasks()  # Mettre à jour l'interface graphique
    
    # Fermer la fenêtre après la fin de la barre de progression
    root.destroy()
    
    # Ouvrir une fenêtre dans le navigateur
    webbrowser.open("https://www.example.com")

# Fonction principale
def programme_principal():
    # Générer un CAPTCHA
    captcha = generate_captcha()
    
    # Créer la fenêtre pour le CAPTCHA
    captcha_window = tk.Tk()
    captcha_window.title("Vérification CAPTCHA")
    
    # Afficher l'énigme CAPTCHA
    captcha_label = tk.Label(captcha_window, text="Veuillez entrer le code suivant :")
    captcha_label.pack(pady=10)
    
    captcha_display = tk.Label(captcha_window, text=captcha, font=("Arial", 20))
    captcha_display.pack(pady=10)
    
    # Champ de texte pour la saisie de l'utilisateur
    captcha_entry = tk.Entry(captcha_window, font=("Arial", 15))
    captcha_entry.pack(pady=10)
    
    # Fonction pour vérifier la saisie et lancer la barre de progression
    def verifier_et_lancer():
        saisie_utilisateur = captcha_entry.get()
        if verifier_captcha(captcha, saisie_utilisateur):
            captcha_window.destroy()  # Fermer la fenêtre CAPTCHA
            afficher_barre_progression()  # Lancer la barre de progression
        else:
            messagebox.showerror("Erreur CAPTCHA", "Le code saisi est incorrect. Essayez à nouveau.")
            captcha_entry.delete(0, tk.END)  # Effacer le champ de saisie
    
    # Bouton pour vérifier le CAPTCHA
    valider_button = tk.Button(captcha_window, text="Valider", command=verifier_et_lancer)
    valider_button.pack(pady=10)
    
    captcha_window.mainloop()

# Lancer le programme principal
programme_principal()