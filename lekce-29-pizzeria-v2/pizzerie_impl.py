"""
Interni API pizzerie - verze 2.

ZMENA OPROTI V1:
- zaplat() je nyni IDEMPOTENTNI:
  * pokud platba neexistuje, vytvori ji (jako predtim)
  * pokud platba existuje a klient posila STEJNA data, vrati existujici (no-op)
  * pokud platba existuje a klient posila JINA data, vyhodi 409
- ObjednavkaJizZaplacena se nahrazuje za PlatbaSeLisi (jen pri lisicich datech)
"""

from datetime import datetime
from typing import Optional

from models import (
    CENIK,
    Objednavka,
    Platba,
    Polozka,
    StavObjednavky,
    VelikostPolozky,
    ZpusobPlatby,
)


# Vyjimky, ktere tahle vrstva muze vyhodit.

class ObjednavkaNeexistuje(Exception):
    """Pokus o operaci nad neexistujici objednavkou."""
    pass


class ObjednavkaJizZaplacena(Exception):
    """Nelze pridavat polozky do uz zaplacene objednavky."""
    pass


class PlatbaSeLisi(Exception):
    """Platba uz existuje a nove poslana data se lisi - nemuzeme to brat jako idempotentni retry."""
    pass


class NeznamaPolozka(Exception):
    """Pizza/velikost neni v ceniku."""
    pass


class CastkaNizka(Exception):
    """Zaplacena castka je nizsi nez suma objednavky."""
    pass


class Pizzerie:
    """In-memory store. Stav po restartu serveru zanikne."""

    def __init__(self) -> None:
        self._objednavky: dict[int, Objednavka] = {}
        self._dalsi_id: int = 1

    def vytvor_objednavku(self, zakaznik: str) -> Objednavka:
        """Zalozi novou objednavku."""
        objednavka = Objednavka(
            id=self._dalsi_id,
            zakaznik=zakaznik,
            polozky=[],
            platba=None,
            suma=0.0,
            stav=StavObjednavky.nova,
        )
        self._objednavky[self._dalsi_id] = objednavka
        self._dalsi_id += 1
        return objednavka

    def pridej_polozku(self, id_objednavky: int, nazev: str, velikost: VelikostPolozky) -> Polozka:
        """Prida polozku do existujici objednavky."""
        objednavka = self._najdi_objednavku(id_objednavky)

        if objednavka.stav == StavObjednavky.zaplaceno:
            raise ObjednavkaJizZaplacena()

        cena = CENIK.get((nazev, velikost))
        if cena is None:
            raise NeznamaPolozka(f"{nazev} ({velikost.value}) neni v naseji pizzerii")

        polozka = Polozka(nazev=nazev, velikost=velikost, cena=cena)
        objednavka.polozky.append(polozka)
        objednavka.suma += cena

        return polozka

    def zaplat(
        self,
        id_objednavky: int,
        castka: float,
        zpusob: ZpusobPlatby,
    ) -> Platba:
        """
        Zaplati objednavku - IDEMPOTENTNI.

        Vraci Platbu - at uz prave vznikla nebo existovala drive.
        Z hlediska klienta je vysledek stejny: na danem URI je dana platba.

        Vyhodi:
        - ObjednavkaNeexistuje: objednavka s timto id neni
        - CastkaNizka: castka je nizsi nez suma
        - PlatbaSeLisi: platba uz existuje, ale nove poslana data jsou jina
                       (uz to neni idempotentni retry, je to pokus o zmenu)
        """
        objednavka = self._najdi_objednavku(id_objednavky)

        # Pripad 1: platba uz existuje
        if objednavka.platba is not None:
            existujici = objednavka.platba
            # Stejna data? -> idempotentni no-op
            if existujici.castka == castka and existujici.zpusob == zpusob:
                return existujici
            # Jina data -> pokus o zmenu, odmitame
            raise PlatbaSeLisi(
                f"platba uz existuje (castka={existujici.castka}, zpusob={existujici.zpusob.value})"
            )

        # Pripad 2: platba jeste neexistuje, validujeme a vytvarime
        if castka < objednavka.suma:
            raise CastkaNizka(f"castka {castka} < suma {objednavka.suma}")

        platba = Platba(
            castka=castka,
            zpusob=zpusob,
            zaplaceno_v=datetime.now(),
        )
        objednavka.platba = platba
        objednavka.stav = StavObjednavky.zaplaceno

        return platba

    def ziskej_objednavku(self, id_objednavky: int) -> Objednavka:
        """Vrati detail objednavky."""
        return self._najdi_objednavku(id_objednavky)

    def ziskej_platbu(self, id_objednavky: int) -> Optional[Platba]:
        """Vrati platbu objednavky, nebo None pokud jeste nebyla zaplacena."""
        objednavka = self._najdi_objednavku(id_objednavky)
        return objednavka.platba

    def seznam_objednavek(self) -> list[Objednavka]:
        return list(self._objednavky.values())

    def _najdi_objednavku(self, id_objednavky: int) -> Objednavka:
        objednavka = self._objednavky.get(id_objednavky)
        if objednavka is None:
            raise ObjednavkaNeexistuje(f"objednavka {id_objednavky} neexistuje")
        return objednavka