# client.py
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
import logging

class Client:
    def __init__(self, host='localhost', port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        
        # Configuration du logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("ChatClient")
        
        # Interface graphique
        self.window = tk.Tk()
        self.window.title("Chat")
        self.window.geometry("500x600")
        
        # Zone de chat
        self.chat_area = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, width=50, height=30)
        self.chat_area.pack(padx=10, pady=10)
        
        # Zone de saisie
        self.input_area = tk.Text(self.window, height=3)
        self.input_area.pack(padx=10, pady=5)
        
        # Bouton d'envoi
        self.send_button = tk.Button(self.window, text="Envoyer", command=self.send_message)
        self.send_button.pack(pady=5)
        
        # Bind la touche Enter
        self.input_area.bind("<Return>", self.send_message)
        
    def start(self):
        try:
            # Connexion au serveur
            self.client.connect((self.host, self.port))
            self.logger.info("Connecté au serveur")
            
            # Attendre la demande de nom d'utilisateur
            message = self.client.recv(1024).decode()
            if message == "USERNAME":
                username = input("Entrez votre nom d'utilisateur: ")
                self.client.send(username.encode())
            
            # Thread pour recevoir les messages
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            # Démarrer l'interface graphique
            self.window.mainloop()
            
        except Exception as e:
            self.logger.error(f"Erreur de connexion: {e}")
            self.window.destroy()
            
    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode()
                self.chat_area.insert(tk.END, message + '\n')
                self.chat_area.see(tk.END)
            except Exception as e:
                self.logger.error(f"Erreur de réception: {e}")
                break
                
    def send_message(self, event=None):
        message = self.input_area.get("1.0", tk.END).strip()
        if message:
            try:
                self.client.send(message.encode())
                self.input_area.delete("1.0", tk.END)
            except Exception as e:
                self.logger.error(f"Erreur d'envoi: {e}")
                self.chat_area.insert(tk.END, "Erreur d'envoi du message\n")
        
        if event is not None:
            return "break"  # Empêche le saut de ligne après Enter

if __name__ == "__main__":
    client = Client()
    client.start()
