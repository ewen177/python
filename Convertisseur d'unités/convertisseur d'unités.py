def convertir_longueur(valeur, unite_source, unite_cible):
    # Dictionnaire pour les conversions en mètres
    conversions = {
        'm': 1,
        'km': 1000,
        'cm': 0.01,
        'mm': 0.001
    }
    
    # Vérifier que les unités sont valides
    if unite_source not in conversions or unite_cible not in conversions:
        raise ValueError("Unités non valides. Utilisez 'm', 'km', 'cm', 'mm'.")

    # Convertir la valeur dans l'unité de base (mètres)
    valeur_en_metres = valeur * conversions[unite_source]
    
    # Convertir en l'unité cible
    resultat = valeur_en_metres / conversions[unite_cible]
    
    return resultat

# Exemple d'utilisation
if __name__ == "__main__":
    valeur = float(input("Entrez la valeur à convertir : "))
    unite_source = input("Entrez l'unité source (m, km, cm, mm) : ")
    unite_cible = input("Entrez l'unité cible (m, km, cm, mm) : ")
    
    try:
        resultat = convertir_longueur(valeur, unite_source, unite_cible)
        print(f"{valeur} {unite_source} = {resultat} {unite_cible}")
    except ValueError as e:
        print(e)
