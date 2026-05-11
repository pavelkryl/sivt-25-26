"""
Datovy model pizzerie - verze 2.

ZMENA OPROTI V1:
- Polozka misto `list[Platba] platby` ma `Platba | None platba`
- Duvod: na objednavku pripada vzdy maximalne JEDNA platba
  (singleton, ne kolekce)
- Dusledek: v REST API misto POST /platby budeme mit PUT /platba
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
    """Platba za objednavku. Maximalne jedna na objednavku."""
    castka: float
    zpusob: ZpusobPlatby
    zaplaceno_v: datetime


class Objednavka(BaseModel):
    """Objednavka pizzy. Drzi seznam polozek a (volitelne) platbu."""
    id: int
    zakaznik: str
    polozky: list[Polozka]
    platba: Platba | None = None    # singleton: 0..1 platba
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
