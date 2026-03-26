from production import ProductionWorkshop
from technological_process import TechnologicalProcess
from storage import Warehouse
from order import Order, OrderQueue
from packaging_and_labeling import PackagedMilk, PackagedYogurt
import copy

class Customer:
    def __init__(self, name: str):
        self.name = name

    def make_order(self, order_queue: OrderQueue, items: list):
        order = Order(self, items)
        order_queue.add_order(order)

class Player:
    def __init__(self, name: str, workshop: ProductionWorkshop,
                warehouse: Warehouse, technology: TechnologicalProcess):
        self.name = name
        self.workshop = workshop
        self.warehouse = warehouse
        self.technology = technology

    def take_order(self, order_queue: OrderQueue):
        order = order_queue.get_next_order()
        if order is None:
            print("Нет заказов")
            return
        self.process_order(order, order_queue)
    
    def process_item(self, order: Order, item: dict):
        if item["type"] == "milk":
            self.handle_milk(order, item["quantity"])
        elif item["type"] == "yogurt":
            flavour = item.get("flavour", "plain")
            self.handle_yogurt(order, item["quantity"], flavour)

    def process_order(self, order: Order, order_queue : OrderQueue):
        # Создаём резервную копию состояния склада и заказанных товаров
        warehouse_backup = copy.deepcopy(self.warehouse.products_in_warehouse)
        order_backup = copy.deepcopy(order.ready_products)

        try:
            for item in order.items:
                self.process_item(order, item)
        except Exception as e:
            print(f"Ошибка при выполнении заказа для {order.customer.name}: {e}")
            # Откат: восстанавливаем склад и готовые продукты заказа
            self.warehouse.products_in_warehouse = warehouse_backup
            order.ready_products = order_backup
            order_queue.return_to_front(order)
            return

        print("Заказ выполнен для", order.customer.name)

    def handle_milk(self, order: Order, quantity: int):
        needed_quantity = quantity
        while needed_quantity > 0:
            product = self.warehouse.remove_product(PackagedMilk)
            if product is None:
                break
            order.ready_products.append(product)
            needed_quantity -= 1 

        if needed_quantity > 0:
            self.technology.make_pasteurize_milk(self.workshop, 1*needed_quantity)
            while needed_quantity > 0:
                product = self.warehouse.remove_product(PackagedMilk)
                if product is None:
                    break
                order.ready_products.append(product)
                needed_quantity -= 1
    
    def handle_yogurt(self, order: Order, quantity: int, flavour: str):
        needed_quantity = quantity

        while needed_quantity > 0:
            product = self.take_yogurt_from_warehouse(flavour)
            if product is None:
                break

            order.ready_products.append(product)
            needed_quantity -= 1  

        if needed_quantity > 0:
            self.technology.make_yogurt(self.workshop, 0.2*needed_quantity, flavour)

            while needed_quantity > 0:
                product = self.take_yogurt_from_warehouse(flavour)
                if product is None:
                    break

                order.ready_products.append(product)
                needed_quantity -= 1

    def take_yogurt_from_warehouse(self, flavour: str):
        return self.warehouse.take_yogurt(flavour,1)
    
    def check(self, order_que: OrderQueue):
        order_que.print_info()
        

    

    