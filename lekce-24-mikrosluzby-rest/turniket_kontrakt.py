
from abc import ABC, abstractmethod
from datetime import datetime

from pydantic import BaseModel


class Pristup(BaseModel):
    rfid: str
    cas_pristupu: datetime
    povoleno: bool

# Extrahovany kontrakt pro turniket, z lekce 19

class ATurniket(ABC):

    # kontrakt neobsahuje konstruktor, pouze metody, ktere musi implementovat konkretni turniket

    @abstractmethod
    def vpustit(self, rfid: str) -> bool:
        ...

    @abstractmethod
    def reset(self) -> None:
        ...

    @abstractmethod
    def iniciace(self, skipasy: list[str]) -> None:
        ...

    @abstractmethod
    def pridej_skipas(self, zakoupeny_skipas_rfid: str) -> None:
        ...

    @abstractmethod
    def log_vstupu(self) -> list[Pristup]:
        ...