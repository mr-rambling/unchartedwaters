from cities import City, Region
from goods import *

# How can I treat a player as a sprite?
# Need to look at this

class Player:
    def __init__(self, name, region: Region, city: City):
        self.name = name
        self.location = city
        self.region = region
        self.currency = 10_000
        self.health = 87
        self.energy = 92
        self.max_health = 100
        self.max_energy = 100
        self.inventory = {
            'Starting Dagger': {'value':100, 'dmg': 5, 'qty': 1}
            }
        self.cargo = {
            'Magical Tome': Product(name='Magical Tome', category=Category.MAGICAL_ITEMS, qty=100),
            'Fine Jewelry': Product(name='Fine Jewelry', category=Category.JEWELRY, qty=12),
            'Dark Crystals': Product(name='Dark Crystals', category=Category.MINERALS, qty=27)
        }

    def add_item(self, item):
        self.inventory.append(item)

    def remove_item(self, item):
        self.inventory.remove(item)

    def sell_cargo(self, product, price, qty):
        if product in self.cargo.keys():
            if qty < self.cargo[product].qty:
                self.cargo[product].qty -= qty
            elif self.cargo[product].qty == qty or qty > self.cargo[product].qty:
                qty = self.cargo[product].qty
                del self.cargo[product]
        self.currency += price * qty
        print(f"{self.name} sold {qty} of {product} for a total of {price * qty}.")

    def buy_cargo(self, product: Product, price: int, qty: int):
        '''
        Returns number of product purchased
        '''
        if self.currency < price * qty:
            print(f"{self.name} does not have enough currency to buy {qty} of {product}.")
            return 0
        if product.name in self.cargo:
            self.cargo[product.name].qty += qty
        else:
            self.cargo[product.name] = product
        self.currency -= price * qty
        print(f"{self.name} bought {qty} of {product} for a total of {price * qty}.")
        return qty

    def get_inventory(self):
        return self.inventory

    def get_cargo(self):
        return self.cargo
