def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Erreur : Division par zéro."
    return x / y

def calculator():
    print("Sélecteur d'opération :")
    print("1. Addition")
    print("2. Soustraction")
    print("3. Multiplication")
    print("4. Division")

    while True:
        choice = input("Choisissez une opération (1/2/3/4) ou 'q' pour quitter : ")

        if choice == 'q':
            print("Au revoir !")
            break

        if choice in ['1', '2', '3', '4']:
            try:
                num1 = float(input("Entrez le premier nombre : "))
                num2 = float(input("Entrez le deuxième nombre : "))
            except ValueError:
                print("Veuillez entrer des nombres valides.")
                continue

            if choice == '1':
                print(f"{num1} + {num2} = {add(num1, num2)}")
            elif choice == '2':
                print(f"{num1} - {num2} = {subtract(num1, num2)}")
            elif choice == '3':
                print(f"{num1} * {num2} = {multiply(num1, num2)}")
            elif choice == '4':
                print(f"{num1} / {num2} = {divide(num1, num2)}")
        else:
            print("Choix invalide. Veuillez choisir une opération valide.")

if __name__ == "__main__":
    calculator()
