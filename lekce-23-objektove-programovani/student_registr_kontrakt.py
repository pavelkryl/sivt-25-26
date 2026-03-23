from abc import ABC, abstractmethod
from typing import Tuple


class StudentRegistr(ABC):
    """Kontrakt pro správu studentů ve třídě."""

    @abstractmethod
    def pridej_studenta(self, student_id: int, jmeno: str, vek: int) -> None:
        """Přidá studenta do registru. Vyhodí ValueError pokud ID již existuje."""
        ...

    @abstractmethod
    def odeber_studenta(self, student_id: int) -> None:
        """Odebere studenta podle ID. Vyhodí ValueError pokud neexistuje."""
        ...

    @abstractmethod
    def najdi_studenta(self, student_id: int) -> Tuple[int,str] | None:
        """Vrátí slovník s údaji o studentovi, nebo None pokud neexistuje."""
        ...

    @abstractmethod
    def pocet_studentu(self) -> int:
        """Vrátí počet studentů v registru."""
        ...

    @abstractmethod
    def vsichni_studenti(self) -> dict[int,str]:
        """Vrátí seznam všech studentů."""
        ...
