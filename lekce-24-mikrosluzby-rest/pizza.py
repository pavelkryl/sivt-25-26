from enum import Enum

from pydantic import BaseModel


class Velikost(Enum):
    VELKA = 1
    STREDNI = 2
    MALA = 3

class StavObjednavky(Enum):
    ROZPRACOVANA = 1
    DOKONCENA = 2
    STORNOVANA = 3

class Polozka(BaseModel):
    jmeno: str
    velikost: Velikost | None
    cena: float


class Objednavka(BaseModel):
    polozky: list[Polozka] = []
    celkova_cena: float = 0.0
    stav: StavObjednavky = StavObjednavky.ROZPRACOVANA

o : Objednavka = Objednavka()

o.polozky.append(Polozka(jmeno = "Margherita", velikost = Velikost.VELKA, cena = 23))

# zaplacena objednavka:

    