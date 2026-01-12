from dataclasses import dataclass
from datetime import datetime

@dataclass
class Adresa:
    ulice: str
    mesto: str
    psc: str
    stat: str

@dataclass
class Zakaznik:
    id: int
    jmeno: str
    email: str
    adresa: Adresa

@dataclass
class Produkt:
    id: int
    nazev: str
    popis: str
    cena: float

@dataclass
class PolozkaObjednavky:
    id: int
    produkt: Produkt
    mnozstvi: int
    cena_za_kus: float

@dataclass
class Objednavka:
    id: int
    datum: datetime
    zakaznik: Zakaznik
    polozky: list[PolozkaObjednavky]
