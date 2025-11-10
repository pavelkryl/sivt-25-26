from enum import Enum
from attr import dataclass


class Obor(Enum):
    INFORMATIKA = "informatika"
    MATEMATIKA = "matematika"
    FYZIKA = "fyzika"
    EKONOMIE = "ekonomie"

@dataclass
class Student:
    jmeno: str
    vek: int
    obor: Obor


STUDENTI = [
    Student("Jan Novák", 20, Obor.INFORMATIKA),
    Student("Marie Svobodová", 22, Obor.MATEMATIKA),
    Student("Petr Dvořák", 19, Obor.FYZIKA),
    Student("Lucie Němcová", 21, Obor.EKONOMIE),
    Student("Tomáš Černý", 23, Obor.INFORMATIKA),
    Student("Karolína Procházková", 20, Obor.MATEMATIKA),
    Student("Jakub Kučera", 18, Obor.INFORMATIKA),
    Student("Tereza Veselá", 22, Obor.FYZIKA),
    Student("Martin Horák", 21, Obor.EKONOMIE),
    Student("Veronika Marková", 19, Obor.INFORMATIKA),
    Student("Filip Pospíšil", 24, Obor.MATEMATIKA),
    Student("Anna Králová", 20, Obor.FYZIKA),
    Student("David Beneš", 22, Obor.EKONOMIE),
    Student("Kristýna Růžičková", 19, Obor.INFORMATIKA),
    Student("Ondřej Fiala", 21, Obor.MATEMATIKA),
    Student("Barbora Malinová", 23, Obor.FYZIKA),
    Student("Michal Sedláček", 20, Obor.EKONOMIE),
    Student("Nikola Doležalová", 18, Obor.INFORMATIKA),
    Student("Adam Nguyen", 22, Obor.FYZIKA),
    Student("Eliška Krejčí", 21, Obor.MATEMATIKA),
]

def seznam_studentu_jako_mapa():
    m : dict[str, Student] = {}
    for student in STUDENTI:
        m[student.jmeno] = student
    return m