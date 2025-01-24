import random
import time
import json
from typing import Dict, List

class Personnage:
    def __init__(self, nom: str, classe: str):
        self.nom = nom
        self.classe = classe
        self.niveau = 1
        self.pv = 100
        self.pv_max = 100
        self.force = 10
        self.defense = 5
        self.experience = 0
        self.inventaire = []
        self.or_ = 50
        self.equipement = {
            "arme": None,
            "armure": None
        }
        
        # Bonus de classe
        if classe == "guerrier":
            self.force += 5
            self.defense += 3
        elif classe == "mage":
            self.pv -= 20
            self.force += 8
        elif classe == "archer":
            self.defense -= 2
            self.force += 6

    def gagner_experience(self, montant: int):
        self.experience += montant
        while self.experience >= 100:
            self.monter_niveau()
            self.experience -= 100

    def monter_niveau(self):
        self.niveau += 1
        self.pv_max += 20
        self.pv = self.pv_max
        self.force += 2
        self.defense += 1
        print(f"\nFélicitations ! {self.nom} passe au niveau {self.niveau}!")
        print("Vos statistiques ont augmenté!")

class Item:
    def __init__(self, nom: str, type_: str, valeur: int, prix: int):
        self.nom = nom
        self.type = type_
        self.valeur = valeur
        self.prix = prix

class Monstre:
    def __init__(self, nom: str, niveau: int):
        self.nom = nom
        self.niveau = niveau
        self.pv = 50 + (niveau * 10)
        self.force = 5 + (niveau * 2)
        self.defense = 3 + niveau
        self.recompense_xp = 20 + (niveau * 5)
        self.recompense_or = 10 + (niveau * 3)

class Jeu:
    def __init__(self):
        self.items_disponibles = {
            "épée en fer": Item("épée en fer", "arme", 8, 100),
            "épée en acier": Item("épée en acier", "arme", 15, 250),
            "armure en cuir": Item("armure en cuir", "armure", 5, 80),
            "armure en acier": Item("armure en acier", "armure", 12, 200),
            "potion de vie": Item("potion de vie", "consommable", 30, 50)
        }
        
        self.monstres = [
            "Gobelin", "Orc", "Troll", "Squelette", "Loup", "Bandit"
        ]
        
        self.zones = [
            "Forêt Sombre", "Grotte Mystérieuse", "Marais Brumeux", 
            "Ruines Anciennes", "Mont Périlleux"
        ]
        
        print("Bienvenue dans l'Aventure Fantastique!")
        self.joueur = self.creer_personnage()
        self.boucle_principale()

    def creer_personnage(self) -> Personnage:
        nom = input("Entrez le nom de votre personnage: ")
        while True:
            print("\nChoisissez votre classe:")
            print("1. Guerrier (Plus de défense)")
            print("2. Mage (Plus de force mais moins de PV)")
            print("3. Archer (Plus de force mais moins de défense)")
            choix = input("Votre choix (1-3): ")
            
            if choix == "1":
                return Personnage(nom, "guerrier")
            elif choix == "2":
                return Personnage(nom, "mage")
            elif choix == "3":
                return Personnage(nom, "archer")
            else:
                print("Choix invalide, veuillez réessayer.")

    def afficher_stats(self):
        print(f"\nStats de {self.joueur.nom} - Niveau {self.joueur.niveau}")
        print(f"Classe: {self.joueur.classe}")
        print(f"PV: {self.joueur.pv}/{self.joueur.pv_max}")
        print(f"Force: {self.joueur.force}")
        print(f"Défense: {self.joueur.defense}")
        print(f"Expérience: {self.joueur.experience}/100")
        print(f"Or: {self.joueur.or_}")

    def combat(self, monstre: Monstre):
        print(f"\nUn {monstre.nom} niveau {monstre.niveau} apparaît!")
        
        while monstre.pv > 0 and self.joueur.pv > 0:
            print(f"\nVos PV: {self.joueur.pv}/{self.joueur.pv_max}")
            print(f"PV du {monstre.nom}: {monstre.pv}")
            print("\nQue voulez-vous faire?")
            print("1. Attaquer")
            print("2. Utiliser une potion de vie")
            print("3. Tenter de fuir")
            
            action = input("Votre choix (1-3): ")
            
            if action == "1":
                # Attaque du joueur
                degats = max(1, self.joueur.force - monstre.defense)
                monstre.pv -= degats
                print(f"Vous infligez {degats} points de dégâts!")
                
                if monstre.pv <= 0:
                    print(f"\nVous avez vaincu le {monstre.nom}!")
                    self.joueur.gagner_experience(monstre.recompense_xp)
                    self.joueur.or_ += monstre.recompense_or
                    print(f"Vous gagnez {monstre.recompense_xp} XP et {monstre.recompense_or} or!")
                    return True
                
                # Attaque du monstre
                degats = max(1, monstre.force - self.joueur.defense)
                self.joueur.pv -= degats
                print(f"Le {monstre.nom} vous inflige {degats} points de dégâts!")
                
            elif action == "2":
                if "potion de vie" in [item.nom for item in self.joueur.inventaire]:
                    potion = next(item for item in self.joueur.inventaire 
                                if item.nom == "potion de vie")
                    self.joueur.pv = min(self.joueur.pv_max, 
                                       self.joueur.pv + potion.valeur)
                    self.joueur.inventaire.remove(potion)
                    print(f"Vous utilisez une potion et récupérez {potion.valeur} PV!")
                else:
                    print("Vous n'avez pas de potion!")
                    continue
                    
            elif action == "3":
                if random.random() < 0.5:
                    print("Vous parvenez à fuir!")
                    return False
                else:
                    print("Vous ne parvenez pas à fuir!")
                    
            if self.joueur.pv <= 0:
                print("\nVous avez été vaincu...")
                print("GAME OVER")
                exit()

    def magasin(self):
        print("\nBienvenue au magasin!")
        print(f"Votre or: {self.joueur.or_}")
        print("\nArticles disponibles:")
        
        for i, (nom, item) in enumerate(self.items_disponibles.items(), 1):
            print(f"{i}. {item.nom} - {item.prix} or")
        print(f"{len(self.items_disponibles) + 1}. Quitter")
        
        choix = input("Que voulez-vous acheter? ")
        
        try:
            index = int(choix) - 1
            if index == len(self.items_disponibles):
                return
            
            item = list(self.items_disponibles.values())[index]
            if self.joueur.or_ >= item.prix:
                self.joueur.or_ -= item.prix
                self.joueur.inventaire.append(item)
                print(f"Vous avez acheté {item.nom}!")
            else:
                print("Vous n'avez pas assez d'or!")
        except (ValueError, IndexError):
            print("Choix invalide!")

    def gerer_equipement(self):
        print("\nGestion de l'équipement:")
        
        if not self.joueur.inventaire:
            print("Votre inventaire est vide!")
            return
            
        print("\nVotre inventaire:")
        for i, item in enumerate(self.joueur.inventaire, 1):
            print(f"{i}. {item.nom}")
        print(f"{len(self.joueur.inventaire) + 1}. Retour")
        
        choix = input("Quel objet voulez-vous équiper/utiliser? ")
        
        try:
            index = int(choix) - 1
            if index == len(self.joueur.inventaire):
                return
                
            item = self.joueur.inventaire[index]
            if item.type in ["arme", "armure"]:
                if self.joueur.equipement[item.type]:
                    ancien_item = self.joueur.equipement[item.type]
                    self.joueur.inventaire.append(ancien_item)
                    
                self.joueur.equipement[item.type] = item
                self.joueur.inventaire.remove(item)
                print(f"Vous vous équipez de {item.nom}!")
                
        except (ValueError, IndexError):
            print("Choix invalide!")

    def sauvegarder(self):
        donnees = {
            "nom": self.joueur.nom,
            "classe": self.joueur.classe,
            "niveau": self.joueur.niveau,
            "pv": self.joueur.pv,
            "pv_max": self.joueur.pv_max,
            "force": self.joueur.force,
            "defense": self.joueur.defense,
            "experience": self.joueur.experience,
            "or": self.joueur.or_,
            "inventaire": [(item.nom, item.type, item.valeur, item.prix) 
                          for item in self.joueur.inventaire],
            "equipement": {slot: (item.nom if item else None) 
                         for slot, item in self.joueur.equipement.items()}
        }
        
        with open("sauvegarde.json", "w") as f:
            json.dump(donnees, f)
        print("Partie sauvegardée!")

    def charger(self):
        try:
            with open("sauvegarde.json", "r") as f:
                donnees = json.load(f)
                
            self.joueur = Personnage(donnees["nom"], donnees["classe"])
            self.joueur.niveau = donnees["niveau"]
            self.joueur.pv = donnees["pv"]
            self.joueur.pv_max = donnees["pv_max"]
            self.joueur.force = donnees["force"]
            self.joueur.defense = donnees["defense"]
            self.joueur.experience = donnees["experience"]
            self.joueur.or_ = donnees["or"]
            
            self.joueur.inventaire = [
                Item(nom, type_, valeur, prix)
                for nom, type_, valeur, prix in donnees["inventaire"]
            ]
            
            for slot, nom_item in donnees["equipement"].items():
                if nom_item:
                    self.joueur.equipement[slot] = self.items_disponibles[nom_item]
                    
            print("Partie chargée!")
            return True
        except FileNotFoundError:
            print("Aucune sauvegarde trouvée!")
            return False

    def explorer_zone(self):
        zone = random.choice(self.zones)
        print(f"\nVous explorez {zone}...")
        time.sleep(1)
        
        if random.random() < 0.7:  # 70% de chance de rencontrer un monstre
            niveau_monstre = max(1, self.joueur.niveau + random.randint(-2, 2))
            monstre = Monstre(random.choice(self.monstres), niveau_monstre)
            self.combat(monstre)
        else:
            evenements = [
                "Vous trouvez un petit coffre contenant {0} or!",
                "Vous découvrez une potion de vie!",
                "Vous ne trouvez rien d'intéressant...",
                "Vous trouvez des traces étranges, mais rien de plus."
            ]
            evenement = random.choice(evenements)
            
            if "or" in evenement:
                montant = random.randint(10, 50)
                self.joueur.or_ += montant
                print(evenement.format(montant))
            elif "potion" in evenement:
                self.joueur.inventaire.append(self.items_disponibles["potion de vie"])
                print(evenement)
            else:
                print(evenement)

    def boucle_principale(self):
        while True:
            print("\nQue souhaitez-vous faire?")
            print("1. Explorer une zone")
            print("2. Visiter le magasin")
            print("3. Gérer l'équipement")
            print("4. Voir les statistiques")
            print("5. Sauvegarder")
            print("6. Charger")
            print("7. Quitter")
            
            choix = input("Votre choix (1-7): ")
            
            if choix == "1":
                self.explorer_zone()
            elif choix == "2":
                self.magasin()
            elif choix == "3":
                self.gerer_equipement()
            elif choix == "4":
                self.afficher_stats()
            elif choix == "5":
                self.sauvegarder()
            elif choix == "6":
                self.charger()
            elif choix == "7":
                print("Merci d'avoir joué!")
                break
            else:
                print("Choix invalide!")

if __name__ == "__main__":
    jeu = Jeu()
