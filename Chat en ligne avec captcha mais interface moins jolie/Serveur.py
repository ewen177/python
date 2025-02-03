import socket
import threading

# Liste des clients connectés
clients = []

def broadcast(message, client):
    """Envoie un message à tous les clients sauf celui qui a envoyé le message"""
    for c in clients:
        if c != client:
            try:
                c.send(message)
            except:
                # Si le client ne répond plus, on le retire de la liste
                clients.remove(c)

def handle_client(client):
    """Gère les messages reçus d'un client"""
    while True:
        try:
            message = client.recv(1024)
            if message:
                broadcast(message, client)
            else:
                break
        except:
            break
    clients.remove(client)
    client.close()

def start_server():
    """Démarre le serveur de chat"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 5555))
    server.listen(5)
    print("Le serveur est en ligne...")
    
    while True:
        client, address = server.accept()
        print(f"Connexion de {address}")
        clients.append(client)
        
        # Crée un nouveau thread pour gérer le client
        client_thread = threading.Thread(target=handle_client, args=(client,))
        client_thread.start()

if __name__ == "__main__":
    start_server()