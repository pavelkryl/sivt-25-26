from typing import Optional
from dataclasses import dataclass

@dataclass
class Produkt:
    nazev: str
    cena: float
    kategorie: str

def nacti_vsechny_produkty() -> list[Produkt]:
    return [
        # Elektronika
        Produkt("Notebook Dell", 25000, "elektronika"),
        Produkt("Myš Logitech", 450, "elektronika"),
        Produkt("Klávesnice", 890, "elektronika"),
        Produkt("Monitor 24\"", 4500, "elektronika"),
        
        # Knihy
        Produkt("Python pro začátečníky", 599, "knihy"),
        Produkt("Čistý kód", 749, "knihy"),
        Produkt("Design Patterns", 899, "knihy"),
        
        # Oblečení
        Produkt("Tričko", 299, "obleceni"),
        Produkt("Mikina", 799, "obleceni"),
        Produkt("Džíny", 1200, "obleceni"),
        Produkt("Boty", 1850, "obleceni"),
        
        # Sport
        Produkt("Fotbalový míč", 450, "sport"),
        Produkt("Fitness láhev", 199, "sport"),
        Produkt("Jóga podložka", 350, "sport"),
        Produkt("Činky 2kg", 599, "sport"),
    ]

def zobraz_produkty(min_cena: float, kategorie: Optional[str] = None) -> list[Produkt]:
    produkty = nacti_vsechny_produkty()
    produkty = [p for p in produkty if p.cena >= min_cena]
    
    if kategorie is not None:
        produkty = [p for p in produkty if p.kategorie == kategorie]
    # None = ukaž všechny kategorie
    
    return produkty


# Ukázky použití:
print("Všechny produkty nad 500 Kč:")
for p in zobraz_produkty(500):
    print(f"  {p.nazev}: {p.cena} Kč ({p.kategorie})")

print("\nElektronika nad 1000 Kč:")
for p in zobraz_produkty(1000, "elektronika"):
    print(f"  {p.nazev}: {p.cena} Kč")

print("\nSportovní vybavení nad 0 Kč:")
for p in zobraz_produkty(0, "sport"):
    print(f"  {p.nazev}: {p.cena} Kč")
