from goods import GoodsCatalog, trade_goods

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
