from enum import Enum

class Category(Enum):
    MAGICAL_ITEMS = "Magical Items"
    TEXTILES = "Textiles"
    HERBS_AND_POTIONS = "Herbs and Potions"
    JEWELRY = "Jewelry"
    MINERALS = "Minerals"
    SPICES = 'Spices'
    NONE = 'None'

class Item():
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Product(Item):
    def __init__(self, name, category:Category, value:int=0, qty:int=0):
        super().__init__(name, value)
        self.qty = qty
        self.cost = 0
        self.category: Category = category
        self.max_qty = qty

class Equipment(Item):
    def __init__(self, name, value, durability):
        super().__init__(name, value)
        self.durability = durability