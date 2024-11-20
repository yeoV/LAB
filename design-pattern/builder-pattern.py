from typing import List
from dataclasses import dataclass


@dataclass
class Pizza:
    dough: str = None
    sauce: str = None
    toppings: List[str] = None


class PizzaBuilder:
    pizza: Pizza = None

    # 비어있는 객체 받음
    def __init__(self, pizza):
        self.pizza = pizza

    def set_dough(self, dough: str):
        self.pizza.dough = dough

    def set_source(self, source: str):
        self.pizza.source = source

    def set_toppings(self, toppings: List[str]):
        self.pizza.toppings = toppings

    def get_result(self) -> Pizza:
        return self.pizza


class PizzaDirector:
    def __init__(self, builder: PizzaBuilder):
        self.builder = builder

    def chnage_builder(self, builder: PizzaBuilder):
        self.builder = builder

    def make_good_pizza(self):
        self.builder.set_dough("thin crust")
        self.builder.set_source("tomato")
        self.builder.set_toppings(["hello", "world"])

    def get_result(self):
        return self.builder.get_result()


def main():

    # empty obj
    builder = PizzaBuilder(Pizza())
    director = PizzaDirector(builder=builder)

    director.make_good_pizza()

    print(director.get_result())


if __name__ == "__main__":
    main()
