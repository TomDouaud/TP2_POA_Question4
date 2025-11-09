"""
TP2Q4A.py
Ce fichier illuste les concepts de POO suivants en Python :
- Polymorphisme (héritage + duck typing)
- Surcharge des méthodes (overloading) -> annotations + singledispatch / singledispatchmethod
- Redéfinition des méthodes (overriding) avec super()
- Généricité (typing.TypeVar + Generic)
- Modularité (fonctions réutilisables pour import)
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List

""" Import de la classe Animal depuis module.py pour l'exemple 5 : modularité """
from module import Animal  

# ===========================
# 1) Polymorphisme
# On crée une interface abstraite Forme avec une méthode aire()
# Les classes dérivées (Cercle, Carre) implémentent aire()
# On montre aussi le duck typing avec Hexagone (pas d'héritage)
# Le duck typing permet d'utiliser des objets non dérivés tant qu'ils fournissent la méthode requise.
# ===========================
class Forme(ABC):
    """Interface abstraite : toute Forme doit fournir une méthode aire()."""
    @abstractmethod
    def aire(self) -> float:
        ...

class Cercle(Forme):
    def __init__(self, rayon: float) -> None:
        self.rayon = rayon

    def aire(self) -> float:  # overriding
        return 3.141592653589793 * self.rayon * self.rayon

class Carre(Forme):
    def __init__(self, cote: float) -> None:
        self.cote = cote

    def aire(self) -> float:  # overriding
        return self.cote * self.cote

# ===========================
# Duck typing (pas d'héritage requis)
# ===========================
class Hexagone:
    """N'hérite pas de Forme, mais fournit aire() : duck typing."""
    def __init__(self, cote: float) -> None:
        self.cote = cote

    def aire(self) -> float:
        # aire d'un hexagone régulier : (3 * sqrt(3) / 2) * cote^2
        return (3 * 3**0.5 / 2) * self.cote * self.cote

def afficher_aire(une_forme: Forme) -> str:
    """Fonction qui montre le polymorphisme par héritage : accepte toute Forme."""
    return f"{type(une_forme).__name__} -> aire = {une_forme.aire()}"

def demo_polymorphisme() -> None:
    print("\n--- Démonstration du polymorphisme par héritage ---")
    print("Création de différentes formes et affichage de leur aire :")
    print("Il y a un Cercle de rayon 3, un Carré de côté 4, et un Hexagone (qui n'hérite pas de forme, mais qui implémente aire()) de côté 2.5")
    formes: List[Forme] = [Cercle(3), Carre(4), Hexagone(2.5)]
    for f in formes:
        print(type(f).__name__, "-> aire :", afficher_aire(f))

# ===========================
# 2) Surcharge des méthodes 
# la surcharge d'une méthode n'existe pas nativement en Python.
# On peut simuler la surcharge via une méthode avec des arguments optionnels
# En Java, cela donnerait :
# public class Operation {
#     // Méthode addition avec 2 paramètres
#     public int addition(int x, int y) {
#         return x + y;
#     }

#     // Surcharge avec 3 paramètres
#     public int addition(int x, int y, int z) {
#         return x + y + z;
#     }

#     // Surcharge avec types différents
#     public double addition(double x, double y) {
#         return x + y;
#     }

#     public static void main(String[] args) {
#         Operation op = new Operation();
#         System.out.println(op.addition(3, 5));         // 8
#         System.out.println(op.addition(3, 5, 2));      // 10
#         System.out.println(op.addition(3.0, 5.0));     // 8.0
#     }
# }
# ===========================
class Calculatrice:
    def addition(self, a, b=None, c=None): # pseudo-surcharge
        if b is not None and c is not None:
            return a + b + c
        elif b is not None:
            return a + b
        else:
            return a

def demo_surcharge() -> None:
    print("\n--- Démonstration de la surcharge via arguments optionnels ---")
    print("Utilisation de la classe Calculatrice avec méthode addition, avec un, deux ou trois arguments :")
    calc = Calculatrice()
    print("Addition avec un argument (5) :", calc.addition(5))         # Affiche 5
    print("Addition avec deux arguments (5, 10) :", calc.addition(5, 10))     # Affiche 15
    print("Addition avec trois arguments (5, 10, 20) :", calc.addition(5, 10, 20)) # Affiche 35

# ===========================
# 3) Overriding (redéfinition) 
# ===========================
class Vehicule:
    def avancer(self):
        print("Le véhicule avance sur la route.")

class Avion(Vehicule):
    def avancer(self):
        print("L'avion prend son envol dans le ciel.")

    def avancer_parent(self):
        super().avancer()  # Appelle la méthode de la classe parente

def demo_redefinition() -> None:
    """Démonstration de la surcharge via overriding."""
    v = Vehicule()
    v.avancer()   # Affiche : Le véhicule avance sur la route.

    a = Avion()
    a.avancer()   # Affiche : L'avion prend son envol dans le ciel.

    a.avancer_parent()  # Appelle la méthode de la classe parente


# ===========================
# 4) Généricité (typing.Generic)
# ===========================

T = TypeVar('T')  # T peut représenter n'importe quel type

class Boite(Generic[T]):
    def __init__(self, objet: T):
        self.objet = objet

    def get(self) -> T:
        return self.objet

# Utilisation
def demo_genericitee() -> None:
    print("\n--- Démonstration de la généricité avec Boite[T] ---")
    print("Création de Boite[int] et Boite[str] :")
    boite_int = Boite[int](42)
    boite_str = Boite[str]("bonjour")
    print("Affichage du Contenu des boîtes (sans que le type pose problème) :")
    print(boite_int.get())  # Affiche : 42
    print(boite_str.get())  # Affiche : bonjour

# ===========================
# 5) Modularité
# ===========================
def demo_modularite() -> None:
    print("\n--- Démonstration de la modularité avec la classe Animal importée ---")
    print("On a importé la classe Animal depuis module.py et on utilise la fonction parler :")
    animal = Animal()
    animal.parler()  # Affiche : L'animal fait un bruit.



# =====================================
# MAIN
# =====================================

def main():
    while True:
        print("\n===== Démonstration TP2 Question 4 A =====")
        print("1) Polymorphisme")
        print("2) Surcharge des méthodes (overloading)")
        print("3) Redéfinition des méthodes (overriding) ")
        print("4) Généricité")
        print("5) Modularité")
        print("0) Quitter")
        
        choice = input("Votre choix > ").strip()
        
        if choice == "1":
            demo_polymorphisme()
        elif choice == "2":
            demo_surcharge()
        elif choice == "3":
            demo_redefinition()
        elif choice == "4":
            demo_genericitee()
        elif choice == "5":
            demo_modularite()
        elif choice == "0":
            print("Fin du programme.")
            break
        else:
            print("Choix invalide.")


if __name__ == "__main__":
    main()
