from abc import ABC, abstractmethod


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
    def najdi_studenta(self, student_id: int) -> dict | None:
        """Vrátí slovník s údaji o studentovi, nebo None pokud neexistuje."""
        ...

    @abstractmethod
    def pocet_studentu(self) -> int:
        """Vrátí počet studentů v registru."""
        ...

    @abstractmethod
    def vsichni_studenti(self) -> list[dict]:
        """Vrátí seznam všech studentů seřazený podle jména."""
        ...
