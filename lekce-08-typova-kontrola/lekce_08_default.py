from dataclasses import dataclass

@dataclass
class Produkt:
    nazev: str
    cena: float
    kategorie: str

def nacti_vsechny_produkty() -> list[Produkt]:
    # literál produktů
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

def vyber_produkty(produkty: list[Produkt], min_cena: float, kategorie: str | None = None) -> list[Produkt]:
    return [p for p in produkty if p.cena >= min_cena and (p.kategorie == kategorie or kategorie == None)]


# Ukázky použití:
seznam_produktu = nacti_vsechny_produkty()
print("Všechny produkty nad 500 Kč:")
for p in vyber_produkty(seznam_produktu, 500):
    print(f"  {p.nazev}: {p.cena} Kč ({p.kategorie})")

print("\nElektronika nad 1000 Kč:")
for p in vyber_produkty(seznam_produktu, 1000, "elektronika"):
    print(f"  {p.nazev}: {p.cena} Kč")

print("\nVšechny sportovní vybavení:")
for p in vyber_produkty(seznam_produktu, 0, "sport"):
    print(f"  {p.nazev}: {p.cena} Kč")

