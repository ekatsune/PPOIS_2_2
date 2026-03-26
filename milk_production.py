class MilkProduction:
    def __init__(self, volume: float, fat_content: float):
        self.volume = volume
        self.fat_content = fat_content

class Milk(MilkProduction):
    def __init__(self, volume: float, fat_content: float, is_pasteurized: bool):
        super().__init__(volume, fat_content)
        self.is_pasteurized = is_pasteurized
    
    def pasteurize(self):
        self.is_pasteurized = True
    
    def get_info(self):
        print("Молоко\n", "жирность: ", self.fat_content, "\n")
    
class Yogurt(MilkProduction):
    def __init__(self, volume: float, flavour: str, fat_content: float):
        super().__init__(volume, fat_content)
        self.flavour = flavour

    def get_info(self):
        print("Йогурт\n", "жирность: ", self.fat_content,"\n", "вкус: ", 
            self.flavour, "\n")
