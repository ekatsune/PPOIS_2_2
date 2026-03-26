from milk_production import Milk 

class Cow:
    def __init__(self, name: str):
        self._name = name
        self._milk_productivity = 3
        self._fat_content = 4

        self._milking_count = 0
        self._max_milking_before_rest = 3
        self._is_tired = False

    def give_milk(self):
        if self._is_tired:
            raise ValueError(f"Корова {self._name} устала и должна отдохнуть")

        milk = Milk(
            volume=self._milk_productivity,
            fat_content=self._fat_content,
            is_pasteurized=False
        )

        self._milking_count += 1

        if self._milking_count >= self._max_milking_before_rest:
            self._is_tired = True

        return milk

    def rest(self):
        print(f"Корова {self._name} отдыхает")
        self._milking_count = 0
        self._is_tired = False

    def info(self):
        print("\nИмя:", self._name)
        print("Продуктивность дойки:", self._milk_productivity)
        print("Жирность молока:", self._fat_content)
        print("Количество доек:", self._milking_count)
        print("Усталость:", self._is_tired)
