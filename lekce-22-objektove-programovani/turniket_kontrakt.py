from abc import ABC, abstractmethod
from datetime import datetime

from pydantic import BaseModel


class Pristup(BaseModel):
    rfid: str
    cas_pristupu: datetime
    povoleno: bool


class ATurniket(ABC):

    @abstractmethod
    def vpustit(self, rfid: str) -> int:
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