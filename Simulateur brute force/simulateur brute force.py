#!/usr/bin/env python3
"""
simulateur_bruteforce.py

Simulateur éducatif d'attaque par force brute sur un mot de passe défini localement.
Ne teste aucun mot de passe externe.
"""

import itertools
import string
import time

def brute_force_simulator(password: str, charset: str):
    """
    Simule une attaque brute force pour trouver le mot de passe.
    Affiche le nombre de tentatives et le temps estimé.
    """
    start_time = time.time()
    attempts = 0
    max_len = len(password)
    
    print(f"Simulation de brute force pour le mot de passe de longueur {max_len}")
    print(f"Charset utilisé : {charset}")
    print("Début de la simulation...\n")

    # Boucle sur les longueurs possibles
    for length in range(1, max_len + 1):
        # Génère toutes les combinaisons possibles pour cette longueur
        for attempt_tuple in itertools.product(charset, repeat=length):
            attempt = ''.join(attempt_tuple)
            attempts += 1
            # Affichage toutes les 1000 tentatives
            if attempts % 1000 == 0:
                print(f"Tentatives : {attempts}, dernier essai : {attempt}")
            if attempt == password:
                elapsed = time.time() - start_time
                print(f"\nMot de passe trouvé : {attempt}")
                print(f"Nombre de tentatives : {attempts}")
                print(f"Temps écoulé : {elapsed:.2f} secondes")
                return
    print("Simulation terminée : mot de passe non trouvé (ceci ne devrait jamais arriver).")

def main():
    # Mot de passe à simuler
    password = "goodluck"  # Modifiez ici pour tester un autre mot
    # Charset utilisé pour l'attaque (modifiable)
    charset = string.ascii_lowercase  # lettres minuscules uniquement
    # Pour inclure chiffres et symboles : string.ascii_letters + string.digits + string.punctuation

    brute_force_simulator(password, charset)

if __name__ == "__main__":
    main()
