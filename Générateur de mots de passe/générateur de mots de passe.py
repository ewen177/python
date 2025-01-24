import random
import string

def generate_password(length):
    # Définir les caractères à utiliser dans le mot de passe
    characters = string.ascii_letters + string.digits + string.punctuation
    # Générer le mot de passe en choisissant des caractères au hasard
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def main():
    try:
        length = int(input("Entrez la longueur souhaitée du mot de passe : "))
        if length <= 0:
            print("Veuillez entrer un nombre positif.")
            return
        
        password = generate_password(length)
        print("Votre mot de passe généré est :", password)
    
    except ValueError:
        print("Veuillez entrer un nombre valide.")

if __name__ == "__main__":
    main()