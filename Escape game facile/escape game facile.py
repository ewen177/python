class EscapeGame:
    def __init__(self):
        self.is_escaped = False
        self.has_key = False
        self.has_code = False

    def start_game(self):
        print("Bienvenue dans l'Escape Game!")
        print("Vous êtes coincé dans une pièce sombre. Trouvez un moyen de vous échapper.")
        
        while not self.is_escaped:
            self.show_options()
            choice = input("Que voulez-vous faire? (taper 'aide' pour des options) ").lower()
            self.process_choice(choice)

    def show_options(self):
        if not self.has_key and not self.has_code:
            print("\nOptions:")
            print("1. Explorer la pièce")
            print("2. Regarder sous le tapis")
            print("3. Essayer la porte")
            print("4. Aide")
        elif self.has_key and not self.has_code:
            print("\nOptions:")
            print("1. Utiliser la clé sur la porte")
            print("2. Regarder sous le tapis")
            print("3. Essayer la porte")
            print("4. Aide")
        else:
            print("\nOptions:")
            print("1. Utiliser le code sur la porte")
            print("2. Regarder sous le tapis")
            print("3. Essayer la porte")
            print("4. Aide")

    def process_choice(self, choice):
        if choice == '1' or choice == 'explorer la pièce':
            self.explore()
        elif choice == '2' or choice == 'regarder sous le tapis':
            self.look_under_rug()
        elif choice == '3' or choice == 'essayer la porte':
            self.try_door()
        elif choice == 'aide':
            self.show_help()
        else:
            print("Choix non valide, veuillez réessayer.")

    def explore(self):
        print("Vous explorez la pièce et trouvez une clé cachée!")
        self.has_key = True

    def look_under_rug(self):
        if not self.has_code:
            print("Sous le tapis, vous trouvez un code à 4 chiffres: 6187")
            self.has_code = True
        else:
            print("Il n'y a rien d'autre sous le tapis.")

    def try_door(self):
        if self.has_key and not self.has_code:
            print("Vous utilisez la clé, mais la porte est toujours verrouillée.")
            print("Vous devez trouver un code.")
        elif self.has_code:
            code_input = input("Entrez le code pour ouvrir la porte: ")
            if code_input == "6187":
                print("La porte s'ouvre. Vous êtes libre! Vous avez gagné!")
                self.is_escaped = True
            else:
                print("Code incorrect. Essayez encore.")
        else:
            print("La porte est verrouillée. Vous avez besoin d'une clé et d'un code.")

    def show_help(self):
        print("\nAide:")
        print("Vous êtes dans une pièce sombre. Essayez d'explorer la pièce, de regarder sous le tapis ou d'essayer la porte.")
        print("Vous devez trouver une clé et un code pour vous échapper.")

if __name__ == "__main__":
    game = EscapeGame()
    game.start_game()
