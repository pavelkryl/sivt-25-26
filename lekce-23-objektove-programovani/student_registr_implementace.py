from student_registr_kontrakt import Student, StudentRegistr


class StudentRegistrImpl(StudentRegistr):
	def __init__(self) -> None:
		self._studenti: dict[int, tuple[str, int]] = {}

	def pridej_studenta(self, student_id: int, jmeno: str, vek: int) -> None:
		if student_id in self._studenti:
			raise ValueError(f"Student s ID {student_id} uz existuje.")

		self._studenti[student_id] = (jmeno, vek)

	def odeber_studenta(self, student_id: int) -> None:
		if student_id not in self._studenti:
			raise ValueError(f"Student s ID {student_id} neexistuje.")

		del self._studenti[student_id]

	def najdi_studenta(self, student_id: int) -> Student | None:
		s = self._studenti.get(student_id)
		if s is None:
			return None
		return Student(id=student_id, jmeno=s[0], vek=s[1])

	def pocet_studentu(self) -> int:
		return len(self._studenti)

	def vsichni_studenti(self) -> list[Student]:
		return [Student(id=student_id, jmeno=jmeno, vek=_vek) for student_id, (jmeno, _vek) in self._studenti.items()]


