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

class Equipment(Item):
    def __init__(self, name, value, durability):
        super().__init__(name, value)
        self.durability = durability

magical_tome = Product(name='Magical Tome', category=Category.MAGICAL_ITEMS)
enchanted_artifacts = Product(name='Enchanted Artifacts', category=Category.MAGICAL_ITEMS)
rare_minerals = Product(name="Rare Minerals", category=Category.MINERALS)
silk_fabrics = Product(name='Silk Fabrics', category=Category.TEXTILES)
exotic_spice = Product(name='Exotic Spices', category=Category.SPICES)
fine_jewelry = Product(name='Fine Jewelry', category=Category.JEWELRY)
herbal_remedies = Product(name='Herbal Remedies', category=Category.HERBS_AND_POTIONS)
crystalised_fruits = Product(name='Crystalised Fruits', category=Category.SPICES)
elven_jewelry = Product(name='Elven Jewelry', category=Category.JEWELRY)
mystic_herbs = Product(name='Mystic Herbs', category=Category.HERBS_AND_POTIONS)
dark_crystals = Product(name='Dark Crystals', category=Category.MINERALS)
shadowy_potions = Product(name='Shadowy Potions', category=Category.HERBS_AND_POTIONS)