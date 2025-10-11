from goods import *
from constants import *
import pygame

class City(pygame.sprite.Sprite):
    def __init__(self, name, coords: pygame.Vector2, landmarks: list, products: list[Product] = []):
        super().__init__()
        self.name = name
        self.coords = pygame.Vector2(*coords)
        self.image = pygame.Surface((CITY_RADIUS*2,CITY_RADIUS*2), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]
        self.landmarks = landmarks
        self.products = products

        self.draw(self.image)

    def get_products(self):
        '''
        Returns list of products available in the city
        '''
        return self.products.keys()    
    
    def get_selling_price(self, product: Product):
        '''
        Returns the selling price of a product in the city
        '''
        if product.name in self.products.keys():
            return int(self.products[product.name].value * IN_STOCK_VALUE_MODIFIER)
        return int(product.value * OUT_OF_STOCK_VALUE_MODIFIER)

    def draw(self, screen):
        return pygame.draw.circle(screen, 'black', (CITY_RADIUS//2, CITY_RADIUS//2), CITY_RADIUS)

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
Velmore.cities['Seville'] = City("Seville", 
                    SEVILLE, 
                    ["The Great Library", "Seville Castle", "The Crystal Lake"],
                    {'Magical Tome': Product(name='Magical Tome', category=Category.MAGICAL_ITEMS, value=90, qty=19),
                     'Enchanted Artifacts': Product(name='Enchanted Artifacts', category=Category.MAGICAL_ITEMS, value=70, qty=8),
                     'Silk Fabrics': Product(name='Silk Fabrics', category=Category.TEXTILES, value=30, qty=15),
                     'Fine Jewelry': Product(name='Fine Jewelry', category=Category.JEWELRY, value=60, qty=12)})
Velmore.cities['Serathorne'] = City("Serathorne", 
                    (0, 98),
                    ["The Serpent's Fountain", "Serathorne Cathedral", "The Whispering Woods"],
                    {'Rare Minerals': Product(name='Rare Minerals', category=Category.MINERALS, value=50, qty=12),
                     'Dark Crystals': Product(name='Dark Crystals', category=Category.MINERALS, value=80, qty=5),
                     'Crystalised Fruits': Product(name='Crystalised Fruits', category=Category.MINERALS, value=20, qty=20)})
Velmore.cities['Draymoor'] = City("Draymoor", 
                    (-32, 50),
                    ["The Draymoor Keep", "The Misty Marshes", "The Ancient Oak"],
                    {'Enchanted Artifacts': Product(name='Enchanted Artifacts', category=Category.MAGICAL_ITEMS, value=70, qty=8),
                     'Elven Jewelry': Product(name='Elven Jewelry', category=Category.JEWELRY, value=100, qty=10),
                     'Shadowy Potions': Product(name='Shadowy Potions', category=Category.HERBS_AND_POTIONS, value=60, qty=15)})
Velmore.cities['Caldrith Vale'] = City("Caldrith Vale", 
                    (-16, 75),
                    ["The Caldrith Falls", "The Enchanted Glade", "The Ancient Ruins"],
                    {'Exotic Spice': Product(name='Exotic Spice', category=Category.SPICES, value=25, qty=25),
                     'Crystalised Fruits': Product(name='Crystalised Fruits', category=Category.MINERALS, value=20, qty=20),
                     'Mystic Herbs': Product(name='Mystic Herbs', category=Category.SPICES, value=30, qty=30),
                     'Herbal Remedies': Product(name='Herbal Remedies', category=Category.HERBS_AND_POTIONS, value=15, qty=15)})
Velmore.cities['Nex Hollow'] = City("Nex Hollow", 
                    (-86, 42),
                    ["The Shadowed Glade", "Nex Hollow Caverns", "The Whispering Falls"],
                    {'Silk Fabrics': Product(name='Silk Fabrics', category=Category.TEXTILES, value=30, qty=4),
                     'Shadowy Potions': Product(name='Shadowy Potions', category=Category.HERBS_AND_POTIONS, value=60, qty=15),
                     'Dark Crystals': Product(name='Dark Crystals', category=Category.MINERALS, value=80, qty=5),
                     'Rare Minerals': Product(name='Rare Minerals', category=Category.MINERALS, value=50, qty=12)})