import tkinter as tk
from tkinter import ttk, messagebox
import time
import webbrowser

# Fonction pour valider le nom d'utilisateur et le mot de passe
def validate(event=None):  # event=None permet d'utiliser cette fonction avec la touche Entrée
    username = username_entry.get()
    password = password_entry.get()

    # Vérifier si les informations sont correctes
    if username == "admin" and password == "1234":
        # Si les informations sont correctes, fermer la fenêtre de connexion
        login_window.destroy()
        show_progress()
    else:
        messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

# Fonction pour afficher la barre de progression
def show_progress():
    # Créer une nouvelle fenêtre pour afficher la barre de progression
    progress_window = tk.Tk()
    progress_window.title("Chargement")
    progress_window.geometry("300x100")

    progress_label = tk.Label(progress_window, text="Chargement en cours...")
    progress_label.pack(pady=10)

    progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=250, mode="determinate")
    progress_bar.pack(pady=10)

    # Simulation de la progression de la barre
    for i in range(101):
        progress_bar['value'] = i
        progress_window.update_idletasks()
        time.sleep(0.03)  # Temps pour simuler le chargement

    progress_window.destroy()  # Fermer la fenêtre de progression
    open_website()  # Ouvrir la page web

# Fonction pour ouvrir une page web
def open_website():
    url = "https://www.google.com"  # Remplacez par l'URL de votre choix
    webbrowser.open(url)

# Création de la fenêtre de connexion
login_window = tk.Tk()
login_window.title("Connexion")
login_window.geometry("300x200")

# Widgets pour entrer le nom d'utilisateur et le mot de passe
username_label = tk.Label(login_window, text="Nom d'utilisateur:")
username_label.pack(pady=5)
username_entry = tk.Entry(login_window)
username_entry.pack(pady=5)

password_label = tk.Label(login_window, text="Mot de passe:")
password_label.pack(pady=5)
password_entry = tk.Entry(login_window, show="*")
password_entry.pack(pady=5)

# Associer la touche Entrée à la fonction validate
login_window.bind('<Return>', validate)

# Bouton pour valider les informations
login_button = tk.Button(login_window, text="Se connecter", command=validate)
login_button.pack(pady=20)

# Lancement de l'application
login_window.mainloop()