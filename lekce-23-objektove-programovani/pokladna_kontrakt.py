from abc import ABC

from pydantic import BaseModel


class PolozkaUctenky(BaseModel):
    nazev: str
    cena: float
    mnozstvi: int


class Uctenka(BaseModel):
    polozky: list[PolozkaUctenky]
    suma: float


class Pokladna(ABC):
        
    def start(self) -> None:
        """Zacina novy nakup."""
        ...

    def pridej_polozku(self, nazev: str, cena: float, mnozstvi: int) -> float:
        """Prida polozku do nakupu a vraci aktualni cenu nakupu."""
        ...

    def secti(self) -> Uctenka:
        """Vraci shrnuti nakupu - polozky, jejich ceny, mnozstvi, celkovou cenu nakupu."""
        ...

    def zaplaceno(self, castka_od_zakaznika: float) -> float:
        """Zaplacen nakup. Vraci zbytek - kolik se zakaznikovi vraci, nebo 0 pokud je castka presna. Synonymum stop."""
        ...