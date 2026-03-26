import unittest
from decimal import Decimal, ROUND_HALF_UP
from abc import ABC
from unittest.mock import MagicMock
from milk_production import Milk, Yogurt, MilkProduction
from cow import Cow  
from packaging_and_labeling import Package, PackagedMilk, PackagedProduct, PackagedYogurt, ProductLabel, Bottle, YogurtCup
from farm import Farm
from production import ProductionWorkshop
from storage import Warehouse, MilkTank
from order import Order, OrderQueue
from people import Customer, Player
from technological_process import TechnologicalProcess

class TestMilkProduction(unittest.TestCase):
    def test_milk_initialization(self):
        milk = Milk(volume=5, fat_content=3.5, is_pasteurized=False)
        self.assertEqual(milk.volume, 5)
        self.assertEqual(milk.fat_content, 3.5)
        self.assertFalse(milk.is_pasteurized)

    def test_milk_pasteurize(self):
        milk = Milk(volume=5, fat_content=3.5, is_pasteurized=False)
        milk.pasteurize()
        self.assertTrue(milk.is_pasteurized)

    def test_yogurt_initialization(self):
        yogurt = Yogurt(volume=2, flavour="клубника", fat_content=4.0)
        self.assertEqual(yogurt.volume, 2)
        self.assertEqual(yogurt.fat_content, 4.0)
        self.assertEqual(yogurt.flavour, "клубника")

    def test_milkproduction_base(self):
        base = MilkProduction(volume=1.5, fat_content=2.5)
        self.assertEqual(base.volume, 1.5)
        self.assertEqual(base.fat_content, 2.5)

class TestCow(unittest.TestCase):
    def setUp(self):
        self.cow = Cow("Мурка")

    def test_initial_cow_state(self):
        self.assertEqual(self.cow._milking_count, 0)
        self.assertFalse(self.cow._is_tired)
        self.assertEqual(self.cow._milk_productivity, 3)
        self.assertEqual(self.cow._fat_content, 4)

    def test_give_milk_normal(self):
        milk = self.cow.give_milk()
        self.assertIsInstance(milk, Milk)
        self.assertEqual(milk.volume, self.cow._milk_productivity)
        self.assertEqual(milk.fat_content, self.cow._fat_content)
        self.assertFalse(milk.is_pasteurized)
        self.assertEqual(self.cow._milking_count, 1)
        self.assertFalse(self.cow._is_tired)

    def test_cow_gets_tired(self):
        self.cow.give_milk()
        self.cow.give_milk()
        self.assertFalse(self.cow._is_tired)
        self.cow.give_milk()
        self.assertTrue(self.cow._is_tired)

    def test_give_milk_when_tired_raises(self):
        for _ in range(3):
            self.cow.give_milk()
        with self.assertRaises(ValueError):
            self.cow.give_milk()

    def test_rest_resets_cow(self):
        for _ in range(3):
            self.cow.give_milk()
        self.assertTrue(self.cow._is_tired)
        self.cow.rest()
        self.assertFalse(self.cow._is_tired)
        self.assertEqual(self.cow._milking_count, 0)
        milk = self.cow.give_milk()
        self.assertEqual(self.cow._milking_count, 1)
        self.assertIsInstance(milk, Milk)

class DummyPackagedProduct(PackagedMilk, ABC):
    pass

class TestPackaging(unittest.TestCase):
    def test_package_pack_normal(self):
        milk = Milk(volume=5, fat_content=3.5, is_pasteurized=True)
        package = Package("Custom Package", 2, 10)
        qty = package.pack(milk)
        self.assertEqual(qty, 2)  
        self.assertAlmostEqual(milk.volume, 1) 

    def test_package_pack_insufficient_volume(self):
        milk = Milk(volume=1, fat_content=3.5, is_pasteurized=True)
        package = Package("Large Package", 2, 10)
        with self.assertRaises(ValueError):
            package.pack(milk)

    def test_bottle_and_yogurtcup_inheritance(self):
        milk = Milk(volume=3, fat_content=3.5, is_pasteurized=False)
        bottle = Bottle()
        qty = bottle.pack(milk)
        self.assertEqual(qty, 3)
        self.assertAlmostEqual(milk.volume, 0)

        yogurt = Yogurt(volume=1, flavour="клубника", fat_content=4)
        cup = YogurtCup()
        qty_y = cup.pack(yogurt)
        self.assertEqual(qty_y, 5)
        self.assertAlmostEqual(yogurt.volume, 0)

    def test_product_label(self):
        label = ProductLabel("Workshop1", "Address1", "milk")
        self.assertEqual(label.workshop_name, "Workshop1")
        self.assertEqual(label.workshop_address, "Address1")
        self.assertEqual(label.product_name, "milk")

    def test_packagedmilk_total_volume_and_price(self):
        milk = Milk(volume=5, fat_content=3.5, is_pasteurized=True)
        bottle = Bottle()
        label = ProductLabel("WS", "Addr", "milk")
        packaged = PackagedMilk(milk, bottle, 2, label)
        self.assertEqual(packaged.total_volume(), 2*1.0)
        self.assertEqual(packaged.total_price(), round(2*1.0*3.2,2))
        self.assertEqual(packaged.get_group_key(), ("milk", "Бутылка молока"))

    def test_packagedyogurt_total_volume_and_price(self):
        yogurt = Yogurt(volume=2, flavour="vanilla", fat_content=4)
        cup = YogurtCup()
        label = ProductLabel("WS", "Addr", "yogurt")
        packaged = PackagedYogurt(yogurt, cup, 5, label)
        self.assertEqual(packaged.total_volume(), 5*0.2)
        self.assertEqual(packaged.total_price(), round(5*0.2*6,2))
        self.assertEqual(packaged.get_group_key(), ("yogurt", "Стаканчик йогурта", "vanilla"))

    def test_packagedmilk_get_info_runs(self):
        milk = Milk(volume=5, fat_content=3.5, is_pasteurized=True)
        bottle = Bottle()
        label = ProductLabel("WS", "Addr", "milk")
        packaged = PackagedMilk(milk, bottle, 2, label)
        packaged.get_info()

    def test_packagedyogurt_get_info_runs(self):
        yogurt = Yogurt(volume=1, flavour="cherry", fat_content=4)
        cup = YogurtCup()
        label = ProductLabel("WS", "Addr", "yogurt")
        packaged = PackagedYogurt(yogurt, cup, 3, label)
        packaged.get_info()  

class TestMilkFarmSystem(unittest.TestCase):
    def setUp(self):
        self.farm = Farm("улица")
        self.warehouse = Warehouse("здесь")
        self.tank = MilkTank()
        self.workshop = ProductionWorkshop("Workshop1", "Workshop Address", self.tank, self.warehouse)

    def test_buy_cow(self):
        self.farm.buy_cow("Буба")
        self.assertEqual(len(self.farm.cows), 1)
        self.assertIsInstance(self.farm.cows[0], Cow)
        self.assertEqual(self.farm.cows[0]._name, "Буба")

    def test_milking_and_auto_rest(self):
        cow = Cow("Бублик")
        self.farm.cows.append(cow)
        self.farm.milking(self.workshop)
        self.farm.milking(self.workshop)
        self.farm.milking(self.workshop)
        self.farm.milking(self.workshop)
        self.assertFalse(cow._is_tired)
        self.assertEqual(cow._milking_count, 0)

class TestWorkShopAndStorageSystem(unittest.TestCase):
    def setUp(self):
        self.warehouse = Warehouse("здесь")
        self.tank = MilkTank()
        self.workshop = ProductionWorkshop("Workshop1", "Workshop Address", self.tank, self.warehouse)
    def test_fill_and_get_milk(self):
        milk = Milk(volume=10, fat_content=3.5, is_pasteurized=False)
        self.tank.fill(milk)
        assert self.tank.milk is not None
        self.assertEqual(self.tank.milk.volume, 10)
        taken = self.tank.get_milk(3)
        self.assertEqual(taken.volume, 3)
        self.assertEqual(self.tank.milk.volume, 7)

    def test_fill_mixed_milk_raises(self):
        milk1 = Milk(volume=5, fat_content=3.5, is_pasteurized=False)
        milk2 = Milk(volume=5, fat_content=4.0, is_pasteurized=False)
        milk3 = Milk(volume=5, fat_content=3.5, is_pasteurized=True)
        self.tank.fill(milk1)
        with self.assertRaises(ValueError):
            self.tank.fill(milk2)  
        with self.assertRaises(ValueError):
            self.tank.fill(milk3)

    def test_pasteurize_milk(self):
        milk = Milk(volume=5, fat_content=3.5, is_pasteurized=False)
        self.tank.fill(milk)
        milk_past = self.workshop.pasteurize_milk(5)
        self.assertTrue(milk_past.is_pasteurized)
        assert self.tank.milk is not None
        self.assertAlmostEqual(self.tank.milk.volume, 0)

    def test_make_yogurt(self):
        milk = Milk(volume=11, fat_content=4.0, is_pasteurized=True)
        self.tank.fill(milk)
        yogurt = self.workshop.make_yogurt(volume=10, flavour="strawberry")
        self.assertIsInstance(yogurt, Yogurt)
        self.assertEqual(yogurt.volume, 10)
        self.assertEqual(yogurt.flavour, "strawberry")
        self.assertEqual(yogurt.fat_content, 4.0)

    def test_pack_milk_and_yogurt(self):
        milk = Milk(volume=5, fat_content=3.5, is_pasteurized=True)
        self.workshop.pack_milk(milk)
        self.assertEqual(len(self.warehouse.products_in_warehouse), 1)
        yogurt = Yogurt(volume=2, flavour="vanilla", fat_content=3.5)
        self.workshop.pack_yogurt(yogurt)
        self.assertEqual(len(self.warehouse.products_in_warehouse), 2)

    def test_add_and_remove_product(self):
        milk = Milk(volume=5, fat_content=3.5, is_pasteurized=True)
        package = Bottle()
        label = ProductLabel("WS", "Addr", "milk")
        packaged = PackagedMilk(milk, package, 2, label)
        self.warehouse.add_product(packaged)
        self.assertEqual(len(self.warehouse.products_in_warehouse), 1)
        taken = self.warehouse.remove_product(PackagedMilk)
        self.assertIsInstance(taken, PackagedMilk)
        assert taken is not None
        self.assertEqual(taken.quantity, 1)
        self.assertEqual(self.warehouse.products_in_warehouse[0].quantity, 1)
        taken2 = self.warehouse.remove_product(PackagedMilk)
        self.assertEqual(len(self.warehouse.products_in_warehouse), 0)

    def test_take_yogurt(self):
        yogurt = Yogurt(volume=2, flavour="blueberry", fat_content=3.5)
        self.workshop.pack_yogurt(yogurt)
        taken = self.warehouse.take_yogurt("blueberry", 10)
        self.assertIsNotNone(taken)
        assert taken is not None    
        self.assertEqual(taken.quantity, 10)
        none_taken = self.warehouse.take_yogurt("blueberry", 5)
        self.assertIsNone(none_taken)

    def test_group_products(self):
        milk = Milk(volume=5, fat_content=3.5, is_pasteurized=True)
        package = Bottle()
        label = ProductLabel("WS", "Addr", "milk")
        packaged1 = PackagedMilk(milk, package, 2, label)
        packaged2 = PackagedMilk(milk, package, 3, label)
        self.warehouse.add_product(packaged1)
        self.warehouse.add_product(packaged2)
        self.assertEqual(len(self.warehouse.products_in_warehouse), 2)
        self.warehouse.group_products()
        self.assertEqual(len(self.warehouse.products_in_warehouse), 1)
        self.assertEqual(self.warehouse.products_in_warehouse[0].quantity, 5)

class TestOrderSystem(unittest.TestCase):
    def setUp(self):
        self.mock_workshop = MagicMock()
        self.mock_warehouse = MagicMock()
        self.mock_technology = MagicMock()
        self.player = Player("Катюха", self.mock_workshop, self.mock_warehouse, self.mock_technology)
        self.order_queue = OrderQueue()

    def test_customer_make_order(self):
        customer = Customer("Evroopt")
        items = [{"type": "milk", "quantity": 2}]
        customer.make_order(self.order_queue, items)
        self.assertEqual(len(self.order_queue.orders), 1)
        self.assertEqual(self.order_queue.orders[0].customer.name, "Evroopt")
        self.assertEqual(self.order_queue.orders[0].items, items)

    def test_order_queue_get_and_return(self):
        customer = Customer("Market")
        items = [{"type": "milk", "quantity": 1}]
        customer.make_order(self.order_queue, items)
        next_order = self.order_queue.get_next_order()
        assert next_order is not None 
        self.assertEqual(next_order.customer.name, "Market")
        self.assertIsNotNone(next_order)
        self.assertEqual(next_order.customer.name, "Market")
        self.assertEqual(next_order.items, items)
        self.assertEqual(len(self.order_queue.orders), 0)
        self.order_queue.return_to_front(next_order)
        self.assertEqual(len(self.order_queue.orders), 1)

    def test_process_order_milk_from_warehouse(self):
        milk_product = PackagedMilk(MagicMock(), Bottle(), 1, ProductLabel("WS","Addr","milk"))
        self.player.warehouse.remove_product = MagicMock(side_effect=[milk_product])
        customer = Customer("Миша")
        customer.make_order(self.order_queue, [{"type": "milk", "quantity": 1}])
        self.player.take_order(self.order_queue)
        self.player.warehouse.remove_product.assert_called_once()

    def test_process_order_milk_production_on_shortage(self):
        self.player.warehouse.remove_product = MagicMock(side_effect=[None, PackagedMilk(MagicMock(), Bottle(), 1, ProductLabel("WS","Addr","milk"))])
        self.player.technology.make_pasteurize_milk = MagicMock()
        customer = Customer("Гоша")
        customer.make_order(self.order_queue, [{"type": "milk", "quantity": 1}])
        self.player.take_order(self.order_queue)
        
        self.player.technology.make_pasteurize_milk.assert_called_once()

    def test_process_order_yogurt_from_warehouse(self):
        yogurt_product = PackagedYogurt(MagicMock(), YogurtCup(), 1, ProductLabel("WS","Addr","yogurt"))
        self.player.take_yogurt_from_warehouse = MagicMock(return_value=yogurt_product)
        customer = Customer("Стасянчееек")
        customer.make_order(self.order_queue, [{"type": "yogurt", "quantity": 1, "flavour": "strawberry"}])
        self.player.take_order(self.order_queue)
        self.player.take_yogurt_from_warehouse.assert_called_with("strawberry")

    def test_process_order_yogurt_production_on_shortage(self):
        yogurt_product = PackagedYogurt(MagicMock(), YogurtCup(), 1, ProductLabel("WS","Addr","yogurt"))
        self.player.take_yogurt_from_warehouse = MagicMock(side_effect=[None, yogurt_product])
        self.player.technology.make_yogurt = MagicMock()
        customer = Customer("УЛУЛУЛУ")
        customer.make_order(self.order_queue, [{"type": "yogurt", "quantity": 1, "flavour": "vanilla"}])
        self.player.take_order(self.order_queue)
        self.player.technology.make_yogurt.assert_called_once()

    def test_process_order_error_rollback(self):
        def raise_error(*args, **kwargs):
            raise Exception("Ошибка")
        self.player.warehouse.remove_product = MagicMock(side_effect=raise_error)
        self.player.technology.make_pasteurize_milk = MagicMock()
        customer = Customer("BSUIR")
        customer.make_order(self.order_queue, [{"type": "milk", "quantity": 1}])
        self.player.take_order(self.order_queue)
        self.assertEqual(len(self.order_queue.orders), 1)

class DummyCustomer:
    def __init__(self, name):
        self.name = name

class TestOrderCoverage(unittest.TestCase):
    def test_order_init(self):
        customer = DummyCustomer("BSUIR")
        items = [{"type": "milk", "quantity": 2}, {"type": "yogurt", "quantity": 3, "flavour": "cherry"}]
        order = Order(customer, items)
        # Проверяем, что поля инициализированы
        self.assertEqual(order.customer.name, "BSUIR")
        self.assertEqual(len(order.items), 2)
        self.assertEqual(order.ready_products, [])

    def test_order_print_info(self):
        customer = DummyCustomer("Bob")
        items = [{"type": "milk", "quantity": 1}, {"type": "yogurt", "quantity": 2, "flavour": "vanilla"}]
        order = Order(customer, items)
        order.print_info()

    def test_orderqueue_empty_get_next_order(self):
        queue = OrderQueue()
        self.assertIsNone(queue.get_next_order())

    def test_orderqueue_add_and_get_next(self):
        customer = DummyCustomer("U")
        order = Order(customer, [])
        queue = OrderQueue()
        queue.add_order(order)
        next_order = queue.get_next_order()
        self.assertIsNotNone(next_order)
        assert next_order.customer is not None    
        self.assertEqual(next_order.customer.name, "U")

    def test_orderqueue_return_to_front_and_print_info_empty(self):
        queue = OrderQueue()
        queue.print_info()  
        customer = DummyCustomer("Almi")
        order = Order(customer, [])
        queue.add_order(order)
        queue.return_to_front(order)
        self.assertEqual(queue.orders[0].customer.name, "Almi")

class TestTechnologicalProcess(unittest.TestCase):
    def setUp(self):
        self.farm = MagicMock()
        self.workshop = MagicMock()
        self.tp = TechnologicalProcess()

    def test_milking(self):
        self.tp.milking(self.workshop, self.farm)
        self.farm.milking.assert_called_once_with(self.workshop)

    def test_make_pasteurize_milk(self):
        fake_milk = MagicMock()
        self.workshop.pasteurize_milk.return_value = fake_milk
        self.tp.make_pasteurize_milk(self.workshop, 5)
        self.workshop.pasteurize_milk.assert_called_once_with(5)
        self.workshop.pack_milk.assert_called_once_with(fake_milk)

    def test_make_yogurt(self):
        fake_yogurt = MagicMock()
        self.workshop.make_yogurt.return_value = fake_yogurt
        self.tp.make_yogurt(self.workshop, 2, "strawberry")
        self.workshop.make_yogurt.assert_called_once_with(2, "strawberry")
        self.workshop.pack_yogurt.assert_called_once_with(fake_yogurt)

if __name__ == "__main__":
    unittest.main()