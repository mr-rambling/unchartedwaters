from enum import Enum

class Category(Enum):
    MAGICAL_ITEMS = "Magical Items"
    TEXTILES = "Textiles"
    HERBS_AND_POTIONS = "Herbs and Potions"
    JEWELRY = "Jewelry"
    MINERALS = "Minerals"

class Product():
    def __init__(self, name, price, category: Category):
        self.name = name
        self.price = price
        self.category = category

goods_catalog = {
    "Magical Tomes": {"price": 100, "category": Category.MAGICAL_ITEMS},
    "Enchanted Artifacts": {"price": 200, "category": Category.MAGICAL_ITEMS},
    "Rare Minerals": {"price": 300, "category": Category.MINERALS},
    "Silk Fabrics": {"price": 150, "category": Category.TEXTILES},
    "Exotic Spices": {"price": 250, "category": Category.HERBS_AND_POTIONS},
    "Fine Jewelry": {"price": 350, "category": Category.JEWELRY},
    "Herbal Remedies": {"price": 120, "category": Category.HERBS_AND_POTIONS},
    "Crystalized Fruits": {"price": 180, "category": Category.HERBS_AND_POTIONS},
    "Elven Jewelry": {"price": 280, "category": Category.JEWELRY},
    "Mystic Herbs": {"price": 380, "category": Category.HERBS_AND_POTIONS},
    "Dark Crystals": {"price": 200, "category": Category.MINERALS},
    "Shadowy Potions": {"price": 300, "category": Category.HERBS_AND_POTIONS},
}

class GoodsCatalog:
    def __init__(self, goods = goods_catalog):
        self.goods = goods

    def add_product(self, product, price, category: Category):
        if product not in self.goods:
            self.goods[product] = {"price": price, "category": category}

    def get_product(self, product):
        if product in self.goods:
            return self.goods[product]
        return None

trade_goods = GoodsCatalog(goods_catalog)