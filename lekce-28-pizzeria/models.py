"""
Datovy model pizzerie.

Pouziva se ve dvou vrstvach:
1. v interni vrstve (pizzerie_impl.py) - jako reprezentace stavu
2. v REST vrstve (main.py) - jako request a response modely

Stejny model pro obe vrstvy je vedome zjednoduseni - v realnem projektu
byvaji modely casto oddelene (interni model vs. API DTO). Pro vyukove
ucely je to ale spis matouci.
"""

from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class VelikostPolozky(str, Enum):
    mala = "mala"
    stredni = "stredni"
    velka = "velka"


class ZpusobPlatby(str, Enum):
    hotove = "hotove"
    karta = "karta"


class StavObjednavky(str, Enum):
    nova = "nova"
    zaplaceno = "zaplaceno"
    pece_se = "pece_se"
    hotovo = "hotovo"


class Polozka(BaseModel):
    """Jedna pizza v objednavce."""
    nazev: str       # "Margherita", "Hawai", "Funghi", ...
    velikost: VelikostPolozky
    cena: float


class Platba(BaseModel):
    """Platba za objednavku. Muze jich byt vic (cast kartou, cast hotove)."""
    castka: float
    zpusob: ZpusobPlatby
    zaplaceno_v: datetime


class Objednavka(BaseModel):
    """Objednavka pizzy. Drzi seznam polozek a seznam plateb."""
    id: int
    zakaznik: str
    polozky: list[Polozka]
    platby: list[Platba]
    suma: float
    stav: StavObjednavky


# Cenik - sdileny mezi vrstvami
CENIK = {
    ("Margherita", VelikostPolozky.mala): 130,
    ("Margherita", VelikostPolozky.stredni): 160,
    ("Margherita", VelikostPolozky.velka): 190,
    ("Hawai", VelikostPolozky.mala): 150,
    ("Hawai", VelikostPolozky.stredni): 180,
    ("Hawai", VelikostPolozky.velka): 220,
    ("Funghi", VelikostPolozky.mala): 140,
    ("Funghi", VelikostPolozky.stredni): 170,
    ("Funghi", VelikostPolozky.velka): 200,
}
