from abc import abstractmethod
from milk_production import MilkProduction, Milk, Yogurt
import math

class Package:
    def __init__(self, type_name: str, volume: float, price_per_liter: float):
        self.type_name = type_name
        self.volume = volume
        self.price_per_liter = price_per_liter

    def pack(self, product: MilkProduction):
        quantity = math.floor(product.volume / self.volume)

        if quantity == 0:
            raise ValueError("Недостаточно объёма для фасовки")

        product.volume -= quantity * self.volume
        return quantity

class Bottle(Package):
    def __init__(self):
        super().__init__("Бутылка молока", 1.0, 3.2)
class YogurtCup(Package):
    def __init__(self):
        super().__init__("Стаканчик йогурта", 0.2, 6) 

class ProductLabel:
    def __init__(self, workshop_name, workshop_address, product_name):
        self.workshop_name = workshop_name
        self.workshop_address = workshop_address
        self.product_name = product_name

class PackagedProduct:
    def __init__(self, product, package: Package, quantity: int, label: ProductLabel):
        self.product = product
        self.package = package
        self.quantity = quantity
        self.label = label

    def total_volume(self):
        return round(self.quantity * self.package.volume, 2)

    def total_price(self):
        return round(self.total_volume() * self.package.price_per_liter, 2)
    
    @abstractmethod
    def get_info(self):
        pass

    @abstractmethod
    def get_group_key(self):
        pass

class PackagedMilk(PackagedProduct):
    def __init__(self, product: Milk, package: Package, quantity: int, label: ProductLabel):
        super().__init__(product, package, quantity, label) 

    def get_info(self):
        print("Тип тары:", self.package.type_name)
        print("Количество:", self.quantity)
        print("Общий объём:", self.total_volume())
        print("Общая стоимость:", self.total_price())

    def get_group_key(self):
        return (
            self.label.product_name,
            self.package.type_name
        )

class PackagedYogurt(PackagedProduct):
    def __init__(self, product: Yogurt, package: Package, quantity: int, label: ProductLabel):
        super().__init__(product, package, quantity, label) 

    def get_info(self):
        print("Тип тары:", self.package.type_name)
        print("Вкус:", self.product.flavour)
        print("Количество:", self.quantity)
        print("Общий объём:", self.total_volume())
        print("Общая стоимость:", self.total_price())

    def get_group_key(self):
        return (
            self.label.product_name,
            self.package.type_name,
            self.product.flavour
        )