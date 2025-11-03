from dataclasses import dataclass
from enum import Enum


class KategorieProduktu(Enum):
    ELEKTRONIKA = "elektronika"
    KNIHY = "knihy"
    OBLECENI = "obleceni"
    SPORT = "sport"


@dataclass
class Produkt:
    nazev: str
    cena: float
    kategorie: KategorieProduktu

def nacti_vsechny_produkty() -> list[Produkt]:
    # literál produktů
    return [
        # Elektronika
        Produkt("Notebook Dell", 25000, KategorieProduktu.ELEKTRONIKA),
        Produkt("Myš Logitech", 450, KategorieProduktu.ELEKTRONIKA),
        Produkt("Klávesnice", 890, KategorieProduktu.ELEKTRONIKA),
        Produkt("Monitor 24\"", 4500, KategorieProduktu.ELEKTRONIKA),

        # Knihy
        Produkt("Python pro začátečníky", 599, KategorieProduktu.KNIHY),
        Produkt("Čistý kód", 749, KategorieProduktu.KNIHY),
        Produkt("Design Patterns", 899, KategorieProduktu.KNIHY),

        # Oblečení
        Produkt("Tričko", 299, KategorieProduktu.OBLECENI),
        Produkt("Mikina", 799, KategorieProduktu.OBLECENI),
        Produkt("Džíny", 1200, KategorieProduktu.OBLECENI),
        Produkt("Boty", 1850, KategorieProduktu.OBLECENI),
        
        # Sport
        Produkt("Fotbalový míč", 450, KategorieProduktu.SPORT),
        Produkt("Fitness láhev", 199, KategorieProduktu.SPORT),
        Produkt("Jóga podložka", 350, KategorieProduktu.SPORT),
        Produkt("Činky 2kg", 599, KategorieProduktu.SPORT),
    ]


def vyber_produkty(produkty: list[Produkt], min_cena: float, kategorie: KategorieProduktu | None = None) -> list[Produkt]:
    return [p for p in produkty if p.cena >= min_cena and (p.kategorie == kategorie or kategorie == None)]


# Ukázky použití:
seznam_produktu = nacti_vsechny_produkty()
print("Všechny produkty nad 500 Kč:")
for p in vyber_produkty(seznam_produktu, 500):
    print(f"  {p.nazev}: {p.cena} Kč ({p.kategorie})")

print("\nElektronika nad 1000 Kč:")
for p in vyber_produkty(seznam_produktu, 1000, KategorieProduktu.ELEKTRONIKA):
    print(f"  {p.nazev}: {p.cena} Kč")

print("\nVšechny sportovní vybavení:")
for p in vyber_produkty(seznam_produktu, 0, KategorieProduktu.SPORT):
    print(f"  {p.nazev}: {p.cena} Kč")


