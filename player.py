from cities import City, Region
from goods import *
from statistics import mean
from ships import *

# How can I treat a player as a sprite?
# Need to look at this
class Player:
    def __init__(self, name, region: Region, city: City):
        self.name = name
        self.location: City = city
        self.region = region
        self.currency = 10_000
        self.ship = Barca()
        self.current_health = 87
        self.current_energy = 92
        self.health_capacity = 100
        self.energy_capacity = 100
        self.inventory_sz = 9
        self.inventory = {
            'Starting Dagger': {'value':100, 'dmg': 5, 'qty': 1}
            }
        self.prev_location = None

    def add_item(self, item):
        self.inventory.append(item)

    def remove_item(self, item):
        self.inventory.remove(item)

    def sell_cargo(self, product: Product, price: int, qty: int):
        price = round(price)
        qty = self.ship.remove_cargo(product, qty)
        self.currency += price * qty

    # Need to move the limiting based on available gold to the 
    # market screen to restrict the number that can be input
    def buy_cargo(self, product: Product, price: int, qty: int):
        '''
        Returns number of product purchased
        '''
        price = round(price)
        if self.currency < price * qty:
            qty = self.currency // price
            if qty == 0:
                return
        qty = self.ship.add_cargo(product, price, qty)
        self.currency -= price * qty
        return qty

    def get_inventory(self):
        return self.inventory
    
    def is_inventory_full(self):
        if len(self.inventory.keys()) < self.inventory_sz:
            return False
        return True
