from typing import Callable


def uprav_cisla(cisla: list[int], funkce: Callable[[int], int]) -> list[int]:
    """Upraví každé číslo v seznamu pomocí předané funkce."""
    return [funkce(x) for x in cisla]

t1 = uprav_cisla([1, 2, 3, 4, 5], lambda x: x * 2)  # [2, 4, 6, 8, 10]
t2 = uprav_cisla([1, 2, 3, 4, 5], lambda x: x ** 2)  # [1, 4, 9, 16, 25]

print(t1)
print(t2)