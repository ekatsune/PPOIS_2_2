from storage import Warehouse, MilkTank
from milk_production import Milk, Yogurt
from packaging_and_labeling import Bottle, YogurtCup, PackagedProduct, ProductLabel, PackagedMilk, PackagedYogurt

class ProductionWorkshop:
    def __init__(self, name: str, adress: str, milk_tank: MilkTank, warehouse: Warehouse):
        self.name = name
        self.adress = adress
        self.milk_tank = milk_tank
        self.warehouse = warehouse

    def pasteurize_milk(self, volume: float):
        milk = self.milk_tank.get_milk(volume)
        milk.pasteurize()
        return milk

    def fill(self, milk):
        self.milk_tank.fill(milk)

    def make_yogurt(self, volume: float, flavour: str):
        milk_needed = volume * 1.1
        milk = self.milk_tank.get_milk(milk_needed)
        return Yogurt(volume, flavour, milk.fat_content)

    def pack_milk(self, milk: Milk):
        package = Bottle()
        quantity = package.pack(milk)
        label = ProductLabel(self.name, self.adress, "milk")
        packaged = PackagedMilk(milk, package, quantity, label)
        self.warehouse.add_product(packaged)
        
    def pack_yogurt(self, yogurt: Yogurt):
        package = YogurtCup()
        quantity = package.pack(yogurt)
        label = ProductLabel(self.name, self.adress, "yogurt")
        packaged = PackagedYogurt(yogurt, package, quantity, label)
        self.warehouse.add_product(packaged)

    def check(self):
        self.milk_tank.get_info()

