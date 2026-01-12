from typing import Callable


def upravit_potom_prumer(cisla: list[int], funkce: Callable[[float], float]) -> float:
    """Upraví každé číslo v seznamu pomocí předané funkce a vrátí jejich průměr."""
    upravena_cisla = [funkce(x) for x in cisla]
    return sum(upravena_cisla) / len(upravena_cisla)


l = [1,2,3,4,5]
print(upravit_potom_prumer(l, lambda x: x + 10))  # průměr čísel zvýšených o 10
print(upravit_potom_prumer(l, lambda x: x * 2))  # průměr čísel vynásobených 2