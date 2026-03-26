from farm import Farm
from production import ProductionWorkshop

class TechnologicalProcess:
    def milking(self, workshop: ProductionWorkshop, farm : Farm):
        farm.milking(workshop)

    def make_pasteurize_milk(self, workshop: ProductionWorkshop, volume: float):
        past_milk = workshop.pasteurize_milk(volume)
        workshop.pack_milk(past_milk)

    def make_yogurt(self, workshop: ProductionWorkshop, volume: float, flavour: str):
        yogurt = workshop.make_yogurt(volume, flavour)
        workshop.pack_yogurt(yogurt)