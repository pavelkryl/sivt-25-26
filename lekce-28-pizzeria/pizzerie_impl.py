"""
Interni API pizzerie - business logika.

Tato vrstva NIC nevi o HTTP, REST, JSON, FastAPI. Stara se jen o data
a pravidla pizzerie:
- vytvor objednavku
- pridej polozku
- zaplat objednavku
- ziskej objednavku

Vyhody oddeleni:
- jde testovat bez HTTP serveru
- jde nad tim postavit RPC API, REST API, GraphQL, CLI nastroj... cokoliv
- HTTP vrstva (main.py) je pak tenka a jednoducha
"""

from datetime import datetime
from models import CENIK, Objednavka, Platba, Polozka, StavObjednavky, VelikostPolozky, ZpusobPlatby


# Vyjimky, ktere tahle vrstva muze vyhodit.
# REST vrstva (main.py) je odchyti a prelozi na HTTP status kody.

class ObjednavkaNeexistuje(Exception):
    """Pokus o operaci nad neexistujici objednavkou."""
    pass


class ObjednavkaJizZaplacena(Exception):
    """Nelze pridat polozku/platbu do uz zaplacene objednavky."""
    pass


class NeznamaPolozka(Exception):
    """Pizza/velikost neni v ceniku."""
    pass


class CastkaNizka(Exception):
    """Zaplacena castka je nizsi nez suma objednavky."""
    pass


class Pizzerie:
    """
    Interni API pizzerie. In-memory store.

    Stav po restartu serveru zanikne - perzistenci budeme resit jindy.
    """

    def __init__(self) -> None:
        self._objednavky: dict[int, Objednavka] = {}
        self._dalsi_id: int = 1

    def vytvor_objednavku(self, zakaznik: str) -> Objednavka:
        """Zalozi novou objednavku. Zacina prazdna ve stavu 'nova'."""
        objednavka = Objednavka(
            id=self._dalsi_id,
            zakaznik=zakaznik,
            polozky=[],
            platby=[],
            suma=0.0,
            stav=StavObjednavky.nova,
        )
        self._objednavky[self._dalsi_id] = objednavka
        self._dalsi_id += 1
        return objednavka

    def pridej_polozku(self, id_objednavky: int, nazev: str, velikost: VelikostPolozky) -> Polozka:
        """
        Prida polozku do existujici objednavky.

        Vyhodi:
        - ObjednavkaNeexistuje pokud objednavka s timto id neni
        - ObjednavkaJizZaplacena pokud uz je zaplacena
        - NeznamaPizza pokud kombinace pizza/velikost neni v ceniku
        """
        objednavka = self._najdi_objednavku(id_objednavky)

        if objednavka.stav == StavObjednavky.zaplaceno:
            raise ObjednavkaJizZaplacena()

        cena = CENIK.get((nazev, velikost))
        if cena is None:
            raise NeznamaPolozka(f"{nazev} ({velikost}) neni v nasi pizzerii")

        polozka = Polozka(nazev=nazev, velikost=velikost, cena=cena)
        objednavka.polozky.append(polozka)
        objednavka.suma += cena

        return polozka

    def zaplat(self, id_objednavky: int, castka: float, zpusob: ZpusobPlatby) -> Platba:
        """
        Zaplati objednavku.

        Vyhodi:
        - ObjednavkaNeexistuje pokud objednavka neni
        - ObjednavkaJizZaplacena pokud uz je zaplacena
        - CastkaNizka pokud zakaznik dal mene nez je suma
        """
        objednavka = self._najdi_objednavku(id_objednavky)

        if objednavka.stav == StavObjednavky.zaplaceno:
            raise ObjednavkaJizZaplacena()

        if castka < objednavka.suma:
            raise CastkaNizka(f"castka {castka} < suma {objednavka.suma}")

        platba = Platba(
            castka=castka,
            zpusob=zpusob,
            zaplaceno_v=datetime.now(),
        )
        objednavka.platby.append(platba)
        objednavka.stav = StavObjednavky.zaplaceno

        return platba

    def ziskej_objednavku(self, id_objednavky: int) -> Objednavka:
        """
        Vrati detail objednavky.

        Vyhodi ObjednavkaNeexistuje pokud objednavka neni.
        """
        return self._najdi_objednavku(id_objednavky)

    def seznam_objednavek(self) -> list[Objednavka]:
        """Vrati vsechny objednavky (i hotove i nove)."""
        return list(self._objednavky.values())

    def _najdi_objednavku(self, id_objednavky: int) -> Objednavka:
        """Internal helper. Vyhodi ObjednavkaNeexistuje pokud neni."""
        objednavka = self._objednavky.get(id_objednavky)
        if objednavka is None:
            raise ObjednavkaNeexistuje(f"objednavka {id_objednavky} neexistuje")
        return objednavka
