# server.py
import socket
import threading
import logging

class Server:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.clients = {}  # {socket: username}
        
        # Configuration du logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("ChatServer")

    def start(self):
        self.server.listen()
        self.logger.info(f"Serveur démarré sur {self.host}:{self.port}")
        
        while True:
            try:
                client, address = self.server.accept()
                self.logger.info(f"Nouvelle connexion de {address}")
                
                # Demander le nom d'utilisateur
                client.send("USERNAME".encode())
                username = client.recv(1024).decode()
                
                # Stocker la connexion
                self.clients[client] = username
                
                # Annoncer la nouvelle connexion
                self.broadcast(f"{username} a rejoint le chat!")
                client.send("Connecté au serveur!".encode())
                
                # Démarrer un thread pour ce client
                thread = threading.Thread(target=self.handle_client, args=(client,))
                thread.start()
                
            except Exception as e:
                self.logger.error(f"Erreur lors de l'acceptation de la connexion: {e}")
                
    def handle_client(self, client):
        username = self.clients[client]
        
        while True:
            try:
                message = client.recv(1024).decode()
                if not message:
                    self.remove_client(client)
                    break
                
                self.broadcast(f"{username}: {message}")
                
            except Exception as e:
                self.logger.error(f"Erreur avec le client {username}: {e}")
                self.remove_client(client)
                break
                
    def broadcast(self, message):
        self.logger.info(f"Diffusion: {message}")
        for client in self.clients:
            try:
                client.send(message.encode())
            except Exception as e:
                self.logger.error(f"Erreur lors de l'envoi à {self.clients[client]}: {e}")
                
    def remove_client(self, client):
        if client in self.clients:
            username = self.clients[client]
            self.broadcast(f"{username} a quitté le chat!")
            del self.clients[client]
            try:
                client.close()
            except:
                pass

if __name__ == "__main__":
    server = Server()
    server.start()