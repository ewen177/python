import time

class Game:
    def __init__(self):
        self.current_room = 'entrée'
        self.inventory = []
        self.rooms = {
            'entrée': {
                'description': "Vous êtes dans l'entrée du château. Il y a des portes au nord et à l'est.",
                'exits': {
                    'nord': 'bibliothèque',
                    'est': 'salon',
                }
            },
            'bibliothèque': {
                'description': "Vous êtes dans une bibliothèque remplie de vieux livres. Une échelle mène à un étage supérieur.",
                'exits': {
                    'sud': 'entrée',
                    'haut': 'étage supérieur',
                },
                'items': ['clé']
            },
            'salon': {
                'description': "Le salon est richement décoré, mais une porte secrète semble se cacher derrière une tapisserie.",
                'exits': {
                    'ouest': 'entrée',
                    'sud': 'cuisine',
                },
                'puzzle': "Quel est le mot de passe pour ouvrir la porte secrète?",
                'answer': "abracadabra"
            },
            'cuisine': {
                'description': "La cuisine est sombre et froide. Il y a une grande table avec un plat mystérieux.",
                'exits': {
                    'nord': 'salon',
                },
                'items': ['plat']
            },
            'étage supérieur': {
                'description': "Vous êtes dans une salle d'étude. Il y a un bureau avec un coffre.",
                'exits': {
                    'bas': 'bibliothèque',
                },
                'puzzle': "Quel est le code à 4 chiffres pour ouvrir le coffre?",
                'answer': "1234"
            }
        }

    def start(self):
        print("Bienvenue dans l'Escape Game du Château Mystérieux !")
        time.sleep(1)
        while True:
            print("\n" + self.rooms[self.current_room]['description'])
            self.process_command(input("> ").lower())

    def process_command(self, command):
        if command in ['nord', 'sud', 'est', 'ouest', 'haut', 'bas']:
            self.move(command)
        elif command.startswith('prendre '):
            self.take_item(command[7:])
        elif command.startswith('résoudre '):
            self.solve_puzzle(command[8:])
        elif command == 'inventaire':
            print("Vous avez: ", ", ".join(self.inventory))
        elif command == 'quitter':
            print("Merci d'avoir joué !")
            exit()
        else:
            print("Commande non reconnue.")

    def move(self, direction):
        if direction in self.rooms[self.current_room]['exits']:
            self.current_room = self.rooms[self.current_room]['exits'][direction]
            if 'items' in self.rooms[self.current_room]:
                print("Vous trouvez les objets suivants: ", ", ".join(self.rooms[self.current_room]['items']))
        else:
            print("Vous ne pouvez pas aller dans cette direction.")

    def take_item(self, item):
        if 'items' in self.rooms[self.current_room] and item in self.rooms[self.current_room]['items']:
            self.inventory.append(item)
            self.rooms[self.current_room]['items'].remove(item)
            print(f"Vous avez pris {item}.")
        else:
            print(f"Il n'y a pas de {item} ici.")

    def solve_puzzle(self, answer):
        if 'puzzle' in self.rooms[self.current_room]:
            if answer == self.rooms[self.current_room]['answer']:
                print("Vous avez résolu l'énigme !")
                del self.rooms[self.current_room]['puzzle']
                del self.rooms[self.current_room]['answer']
            else:
                print("Mauvaise réponse, essayez encore.")
        else:
            print("Il n'y a pas d'énigme à résoudre ici.")

# Lancer le jeu
if __name__ == "__main__":
    game = Game()
    game.start()
