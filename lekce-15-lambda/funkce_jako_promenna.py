from typing import Callable


def vynasob_dvema(x: int) -> int:
    """Vynásobí číslo dvěma."""
    return x * 2

def umocni_dvema(x: int) -> int:
    """Umocní číslo na druhou."""
    return x ** 2

def uprav_cisla(cisla: list[int], funkce: Callable[[int], int]) -> list[int]:
    """Upraví každé číslo v seznamu pomocí předané funkce."""
    return [funkce(x) for x in cisla]

t1 = uprav_cisla([1, 2, 3, 4, 5], vynasob_dvema)  # [2, 4, 6, 8, 10]
t2 = uprav_cisla([1, 2, 3, 4, 5], umocni_dvema)  # [1, 4, 9, 16, 25]

print(t1)
print(t2)