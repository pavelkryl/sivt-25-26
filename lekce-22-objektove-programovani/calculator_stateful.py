
class Calculator:

    def __init__(self):
        self._zasobnik : list[float] = []


    def set_op(self, op: float) -> None:
        self._zasobnik.append(op)

    def krat(self) -> float:
        op1 = self._zasobnik.pop()
        op2 = self._zasobnik.pop()
        return op1 * op2

    def plus(self) -> float:
        op1 = self._zasobnik.pop()
        op2 = self._zasobnik.pop()
        return op1 + op2


#
c = Calculator()
c.set_op(2)
c.set_op(1)
c.set_op(3)
vysledek = c.plus()
c.set_op(vysledek)
vysledek = c.krat()
print(vysledek)