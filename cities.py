from goods import GoodsCatalog, trade_goods
from player import Player

class City():
    def __init__(self, name, location, index, population, landmarks):
        self.name = name
        self.location = location
        self.index = index
        self.population = population
        self.landmarks = landmarks
        self.products = {}

    def add_product(self, product, qty, cost_modifier):
        '''
        Used to add a product to the city's market.\n
        qty: The amount of the product available \n
        cost_modifier: A multiplier for the product's price
        '''
        if cost_modifier < 1:
            cost_modifier = 1
        if trade_goods.get_product(product) is None:
            return
        self.products[product] = trade_goods.get_product(product)
        self.products[product]["qty"] = qty
        self.products[product]["price"] *= cost_modifier

    def get_products(self):
        '''
        Returns list of products available in the city
        '''
        return self.products
    
    def sell_product(self, player: Player, product, qty):
        supply = self.products[product]['qty']
        price = self.products[product]['price']
        if supply >= qty:
            player.buy_cargo(product, price, qty)
            self.products[product]['qty'] -= qty
        else:
            player.buy_cargo(product, price, supply)
            self.products[product]['qty'] = 0
            print('Quantity was restricted to available stock')

    def buy_product(self, player: Player, product, qty):
        if product in player.cargo and qty <= player.cargo[product]['qty']:
            player.sell_cargo(product, price, qty)
        else:
            print(f'Insufficient {product} in cargo')
    

class Cities:
    def __init__(self):
        self.cities = []

    def add_city(self, city: City):
        self.cities.append(city)

    def get_city(self, name):
        for city in self.cities:
            if city.name == name:
                return city
        return None
    
    def all_cities(self):
        n = []
        for city in self.cities:
            n.append(city.name)
        return n
    
cities = []
cities.append(City("Viremontis", 
                    (0, 0),
                    0, 
                    120000, 
                    ["The Great Library", "Viremontis Castle", "The Crystal Lake"])
)
cities.append(City("Serathorne", 
                    (0, 98),
                    1, 
                    95000, 
                    ["The Serpent's Fountain", "Serathorne Cathedral", "The Whispering Woods"])
)
cities.append(City("Draymoor", 
                    (-32, 50),
                    2, 
                    80000, 
                    ["The Draymoor Keep", "The Misty Marshes", "The Ancient Oak"])
)
cities.append(City("Caldrith Vale", 
                    (-16, 75),
                    3, 
                    72000, 
                    ["The Caldrith Falls", "The Enchanted Glade", "The Ancient Ruins"])
)
cities.append(City("Nex Hollow", 
                    (-86, 42),
                    4, 
                    65000, 
                    ["The Shadowed Glade", "Nex Hollow Caverns", "The Whispering Falls"])
)