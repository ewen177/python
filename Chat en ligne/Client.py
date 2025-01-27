import socket
import random
import threading

def ask_captcha():
    """Génère un captcha simple avec un nombre aléatoire"""
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    captcha = num1 + num2
    print(f"Captcha : {num1} + {num2} = ?")
    user_input = int(input("Répondez au captcha pour continuer : "))
    
    if user_input == captcha:
        print("Captcha validé !")
        return True
    else:
        print("Captcha incorrect. Essayez à nouveau.")
        return False

def receive_messages(client):
    """Recevoir et afficher les messages du chat"""
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                print(message)
        except:
            break

def start_client():
    """Démarre le client de chat"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 5555))

    print("Bienvenue dans le chat en ligne !")

    # Demander le nom d'utilisateur
    username = input("Entrez votre nom d'utilisateur : ")

    # Demander et valider le captcha
    while not ask_captcha():
        pass

    # Lancer un thread pour recevoir les messages du serveur
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    # Envoyer des messages au serveur
    while True:
        message = input()
        if message:
            full_message = f"{username}: {message}"
            client.send(full_message.encode('utf-8'))

if __name__ == "__main__":
    start_client()