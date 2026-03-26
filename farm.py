from cow import Cow
from production import ProductionWorkshop

class Farm:
    def __init__(self, adress: str):
        self.adress = adress
        self.cows = []

    def buy_cow(self, name):
        self.cows.append(Cow(name))

    def milking(self, workshop: ProductionWorkshop):
        for cow in self.cows:
            try:
                milk = cow.give_milk()
                workshop.fill(milk)
                print(f"{cow._name} подоена")
            except ValueError:
                cow.rest()   

    def check(self):
        for cow in self.cows:
            cow.info()
