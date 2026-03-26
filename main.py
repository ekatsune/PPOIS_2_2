import typer
import shlex
from farm import Farm
from storage import Warehouse, MilkTank
from production import ProductionWorkshop
from technological_process import TechnologicalProcess
from people import Player, Customer
from order import OrderQueue

app = typer.Typer()

farm = Farm("Семашко 35А")
warehouse = Warehouse("Держинского 91")
workshop = ProductionWorkshop("Савушкин", "Держинского 90", MilkTank(), warehouse)
tech_proc = TechnologicalProcess()
order_queue = OrderQueue()
player = Player("Катюха", workshop, warehouse, tech_proc)

customers = {}

def farm_buycow(args):
    name = " ".join(args)
    farm.buy_cow(name)
    print(f"Корова {name} куплена")

def farm_check(args):
    farm.check()

def techproc_milking(args):
    tech_proc.milking(workshop, farm)

def techproc_pasteurize(args):
    volume = float(args[0])
    tech_proc.make_pasteurize_milk(workshop, volume)
    
def techproc_yogurt(args):
    volume = float(args[0])
    flavour = " ".join(args[1:])
    tech_proc.make_yogurt(workshop, volume, flavour)

def workshop_check(args):
    workshop.check()

def warehouse_check(args):
    warehouse.check()

def customer_create(args):
    name = " ".join(args)
    customers[name] = Customer(name)
    print(f"Клиент {name} создан")

def customer_check(args):
    if not customers:
        print("Нет клиентов")
        return

    print("Список клиентов:")
    for i, name in enumerate(customers, start=1):
        print(f"{i}. {name}")

def customer_order(args):
    name = " ".join(args)

    if name not in customers:
        print("Клиент не найден")
        return

    print("Введите товары (пример: milk 3 или yogurt 5 strawberry)")
    print("Пустая строка — завершить")

    items = []

    while True:
        line = input("item> ").strip()
        if not line:
            break

        parts = line.split()

        if parts[0] == "milk":
            items.append({
                "type": "milk",
                "quantity": int(parts[1])
            })

        elif parts[0] == "yogurt":
            items.append({
                "type": "yogurt",
                "quantity": int(parts[1]),
                "flavour": parts[2]
            })

    customers[name].make_order(order_queue, items)
    print("Заказ добавлен")

def orders_check(args):
    order_queue.print_info()

def player_take(args):
    player.take_order(order_queue)

commands = {
    "farm": {
        "--buycow": {
            "func": farm_buycow,
            "args": "<name>",
            "description": "Купить корову"
        },
        "--check": {
            "func": farm_check,
            "args": "",
            "description": "Узнать, какие коровы есть на ферме"
        }
    },

    "techproc": {
        "--milking": {
            "func": techproc_milking,
            "args": "",
            "description": "Подоить коров на ферме"
        },
        "--pasteurize": {
            "func": techproc_pasteurize,
            "args": "<liters>",
            "description": "Произвести партию пастерилизованного молока"
        },
        "--yogurt": {
            "func": techproc_yogurt,
            "args": "<liters> <flover>",
            "description": "Произвести партию йогурта определённого вкуса"
        }
    },

    "workshop": {
        "--check": {
            "func": workshop_check,
            "args": "",
            "description": "Узнать, сколько молока для производства есть в цеху"
        }
    },

    "warehouse": {
        "--check": {
            "func": warehouse_check,
            "args": "",
            "description": "Узнать, какая продукция лежит на складе"
        }
    },

    "customer": {
        "--create": {
            "func": customer_create,
            "args": "<name>",
            "description": "Создать клиента"
        },
        "--order": {
            "func": customer_order,
            "args": "<name>",
            "description": "Создать заказ от лица клиента"
        },
        "--check": {
            "func": customer_check,
            "args": "",
            "description": "Показать всех клиентов"
        }
    },

    "orders": {
        "--check": {
            "func": orders_check,
            "args": "",
            "description": "Просмотреть очередь заказов"
        }
    },

    "player": {
        "--take": {
            "func": player_take,
            "args": "",
            "description": "Выполнить первый по очереди заказ"
        }
    }
}

@app.command()
def interactive():

    print("Симулятор молочной фермы")
    print("Введите команду или 'exit'")

    while True:

        cmd = input("> ").strip()

        if cmd == "exit":
            break
        if cmd == "help":
            print("Доступные команды:\n")

            for module in commands:
                print(f"[{module}]")
                for command, info in commands[module].items():
                    args = info["args"]
                    desc = info["description"]

                    print(f"  {module} {command} {args}")
                    print(f"    -> {desc}")
            print("\n Подсказка : йогурт делается из необработанного молока!")
            print("\nexit — выход из программы")
            continue
        parts = shlex.split(cmd)

        if len(parts) < 2:
            print("Формат: <модуль> <команда> [аргументы]")
            continue

        module = parts[0]
        command = parts[1]
        args = parts[2:]

        try:
            if module in commands and command in commands[module]:
                info = commands[module][command]

                if not args and info["args"]:
                    print(f"Использование: {module} {command} {info['args']}")
                    continue

                info["func"](args)

            else:
                print("Неизвестная команда")
                print("Введите 'help', чтобы увидеть список команд")

        except Exception as e:
            print("Ошибка:", e)

if __name__ == "__main__":
    app()