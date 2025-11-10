from dataclasses import dataclass
from enum import Enum


class Kategorie(Enum):
    ELEKTRONIKA = "elektronika"
    OBLECENI = "obleceni"
    NADOBI = "nadobi"


@dataclass
class Produkt:
    nazev: str
    cena: float
    kategorie: Kategorie

# interní seznam produktů, který není přímo přístupný zvenčí
_produkty : list[Produkt] = []


def init_produkty(moje_produkty: list[Produkt]) -> None:
    global _produkty    # je třeba deklarovat jako globalní, abychom mohli přiřadit novou hodnotu
    _produkty = moje_produkty

def pridej_produkt(produkt: Produkt) -> None:
    _produkty.append(produkt)

def vrat_produkty(kategorie: Kategorie) -> list[Produkt]:
    return [produkt for produkt in _produkty if produkt.kategorie == kategorie]

def vyhledej_produkt(nazev: str) -> Produkt | None:
    """
    neefektivni linearni vyhledavani produktu podle nazvu
    """
    for produkt in _produkty:
        if produkt.nazev == nazev:
            return produkt
    return None
