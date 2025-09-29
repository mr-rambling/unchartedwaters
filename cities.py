from goods import *

class City():
    def __init__(self, name, location, landmarks, products: list[Product] = []):
        self.name = name
        self.location = location
        self.landmarks = landmarks
        self.products = products

    def get_products(self):
        '''
        Returns list of products available in the city
        '''
        return self.products.keys()    

class Region:
    def __init__(self, name):
        self.name = name
        self.cities = {}

    def add_city(self, city: City, name):
        self.cities[name] = city

    def get_city(self, name):
        return self.cities[name]
    
    def all_cities(self):
        return self.cities.keys()
    
Velmore = Region('Velmore')
Velmore.cities['Viremontis'] = City("Viremontis", 
                    (0, 0), 
                    ["The Great Library", "Viremontis Castle", "The Crystal Lake"],
                    {'Magical Tome': Product(name='Magical Tome', category=Category.MAGICAL_ITEMS, qty=19),
                     'Enchanted Artifacts': Product(name='Enchanted Artifacts', category=Category.MAGICAL_ITEMS)}
                    [magical_tome, enchanted_artifacts, silk_fabrics])
Velmore.cities['Serathorne'] = City("Serathorne", 
                    (0, 98),
                    ["The Serpent's Fountain", "Serathorne Cathedral", "The Whispering Woods"],
                    [rare_minerals, dark_crystals, crystalised_fruits])
Velmore.cities['Draymoor'] = City("Draymoor", 
                    (-32, 50),
                    ["The Draymoor Keep", "The Misty Marshes", "The Ancient Oak"],
                    [enchanted_artifacts, elven_jewelry, shadowy_potions])
Velmore.cities['Caldrith Vale'] = City("Caldrith Vale", 
                    (-16, 75),
                    ["The Caldrith Falls", "The Enchanted Glade", "The Ancient Ruins"],
                    [exotic_spice, crystalised_fruits, mystic_herbs, herbal_remedies])
Velmore.cities['Nex Hollow'] = City("Nex Hollow", 
                    (-86, 42),
                    ["The Shadowed Glade", "Nex Hollow Caverns", "The Whispering Falls"],
                    [silk_fabrics, shadowy_potions, dark_crystals, rare_minerals])