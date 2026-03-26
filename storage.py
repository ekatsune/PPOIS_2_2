from packaging_and_labeling import PackagedProduct, PackagedYogurt, PackagedMilk
from milk_production import Milk
from decimal import Decimal, ROUND_HALF_UP


class Warehouse:
    def __init__(self, adress: str):
        self.adress = adress
        self.products_in_warehouse: list[PackagedProduct] = []

    def add_product(self, product: PackagedProduct):
        self.products_in_warehouse.append(product)

    def remove_product(self, product_type):
        for product in self.products_in_warehouse:
            if isinstance(product, product_type):
                taken = product.__class__(
                    product.product,
                    product.package,
                    1,
                    product.label
                )
                product.quantity -= 1
                if product.quantity == 0:
                    self.products_in_warehouse.remove(product)
                return taken
        return None
    
    def check(self):
        self.group_products()
        for product in self.products_in_warehouse:
            product.get_info()   

    def group_products(self):
        grouped = {}

        for product in self.products_in_warehouse:
            key = product.get_group_key()

            if key not in grouped:
                grouped[key] = product
            else:
                grouped[key].quantity += product.quantity

        self.products_in_warehouse = list(grouped.values())

    def take_yogurt(self, flavour: str, quantity: int) -> PackagedYogurt | None:
        for product in self.products_in_warehouse:
            if isinstance(product, PackagedYogurt):
                if product.product.flavour == flavour and product.quantity >= quantity:
                    taken = PackagedYogurt(
                        product.product,
                        product.package,
                        quantity,
                        product.label
                    )
                    product.quantity -= quantity

                    if product.quantity == 0:
                        self.products_in_warehouse.remove(product)

                    return taken
        return None

class MilkTank:
    def __init__(self):
        self.milk = None

    def fill(self, milk):
        if self.milk is None:
            self.milk = milk
        else:
            if self.milk.fat_content != milk.fat_content:
                raise ValueError("Нельзя смешивать молоко разной жирности")

            if self.milk.is_pasteurized != milk.is_pasteurized:
                raise ValueError("Нельзя смешивать пастеризованное и сырое молоко")

            self.milk.volume += milk.volume

    def get_milk(self, volume: float):
        if self.milk is None:
            raise ValueError("Цистерна пуста")
        elif self.milk.volume < volume:
            raise ValueError("В цистерне недостаточно молока")
        
        rounded_volume = float(Decimal(volume).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

        taken_milk = Milk(
        volume=rounded_volume,
        fat_content=self.milk.fat_content,
        is_pasteurized=self.milk.is_pasteurized
        )
        self.milk.volume -= rounded_volume
        self.milk.volume = float(Decimal(self.milk.volume).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
        return taken_milk
    
    def get_info(self):
        if(self.milk == None):
            raise ValueError("Цистерна пуста")
        else: print("В цистерне ", self.milk.volume, " литров")