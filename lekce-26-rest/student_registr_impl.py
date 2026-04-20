# --- Implementace kontraktu (in-memory) ---
from student_registr_kontrakt import StudentRegistr, Student


class StudentRegistrImpl(StudentRegistr):

    def __init__(self):
        self._studenti: dict[int, Student] = {}

    def pridej_studenta(self, student_id: int, jmeno: str, vek: int) -> None:
        if student_id in self._studenti:
            raise ValueError(f"Student s ID {student_id} jiz existuje.")
        self._studenti[student_id] = Student(id=student_id, jmeno=jmeno, vek=vek)

    def odeber_studenta(self, student_id: int) -> None:
        if student_id not in self._studenti:
            raise ValueError(f"Student s ID {student_id} neexistuje.")
        del self._studenti[student_id]

    def najdi_studenta(self, student_id: int) -> Student | None:
        return self._studenti.get(student_id)

    def pocet_studentu(self) -> int:
        return len(self._studenti)

    def vsichni_studenti(self) -> list[Student]:
        return list(self._studenti.values())


