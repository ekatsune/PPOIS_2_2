from __future__ import annotations

class Order:
    def __init__(self, customer: Customer, items: list):
        self.customer = customer
        self.items = items
        self.ready_products = []

    def print_info(self):
        print("Покупатель:", self.customer.name)
        print("Товары:")
        for item in self.items:
            if item["type"] == "milk":
                print(f"  - Молоко {item['quantity']} шт")
            elif item["type"] == "yogurt":
                print(f"  - Йогурт {item['flavour']} {item['quantity']} шт")

class OrderQueue:
    def __init__(self):
        self.orders = []

    def add_order(self, order: Order):
        self.orders.append(order)

    def get_next_order(self):
        if not self.orders:
            return None
        return self.orders.pop(0)
    
    def return_to_front(self, order: Order):
        self.orders.insert(0, order)
    
    def print_info(self):
        if not self.orders:
            print("Очередь заказов пуста")
            return

        for i, order in enumerate(self.orders, start=1):
            print(f"\nЗаказ №{i}")
            order.print_info()
             