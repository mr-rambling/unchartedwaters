from goods import *
from typing import Dict
from constants import *
import pygame


class Ship:
    def __init__(self, name, hp, speed, crew, price, cargo_sz, coords = (0,0), cargo_slots=12):
        self.name = name
        self.coords = coords
        self.hp = hp
        self.speed = speed
        self.crew = crew
        self.price = price
        self.total_cargo = 0
        self.cargo_sz = cargo_sz
        self.cargo_slots = cargo_slots
        self.cargo: Dict[str, Product]

    def move_speed(self):
        base = 500
        return int(base / self.speed)

    def draw_ship(self, direction, coords: tuple, surface:pygame.Surface):
        centre_x = coords[0]
        centre_y = coords[1]
        point1 = (centre_x, centre_y+10)
        point2 = (centre_x-5,centre_y-10)
        point3 = (centre_x+5,centre_y-10)
        points = [point1, point2, point3]
        
        pygame.draw.polygon(surface, 'black', points)

    def is_cargo_full(self):
        if len(self.cargo.keys()) < self.cargo_slots:
            return False
        return True
    
    def remove_cargo(self, product: Product, qty: int):
        '''
        Returns the quantity removed.

        Removes a specified quantity of a Product from cargo.
        If the quantity is greater then what is currently in cargo,
        the quantity is limited.
        '''
        if product in self.cargo.keys():
            if qty < self.cargo[product].qty:
                self.cargo[product].qty -= qty
            elif self.cargo[product].qty == qty or qty > self.cargo[product].qty:
                qty = self.cargo[product].qty
                del self.cargo[product]
        self.total_cargo -= qty
        return qty
    
    def add_cargo(self, product: Product, price: int, qty: int):
        '''
        Returns the quantity added.

        Adds a specified quantity of a Product from cargo.
        If the quantity is greater then the available cargo space,
        the quantity is limited.
        '''
        qty = min(qty, self.empty_cargo_space())
        if qty != 0:
            if product in self.cargo.keys():
                self.cargo[product].qty += qty
                self.cargo[product].cost = (self.cargo[product].cost * self.cargo[product].qty + price * qty) / (self.ship.cargo[product.name].qty + qty)
            else:
                self.cargo[product] = Product(name=product, category=product.category, qty=qty)
                self.cargo[product].cost = price  
            self.total_cargo += qty      
        return qty
    
    def empty_cargo_space(self):
        return self.cargo_sz - self.total_cargo

class Barca(Ship):
    def __init__(self):
        super().__init__(name = 'Barca',
                        hp = 15, 
                        speed = 5, 
                        crew = 7, 
                        price = 2_000, 
                        cargo_sz = 25)
        self.coords = SEVILLE
        self.cargo = {
            'Magical Tome': Product(name='Magical Tome', category=Category.MAGICAL_ITEMS, qty=8, value=90),
            'Fine Jewelry': Product(name='Fine Jewelry', category=Category.JEWELRY, qty=12, value=60),
            'Dark Crystals': Product(name='Dark Crystals', category=Category.MINERALS, qty=5, value=80)
        }
        self.cargo['Magical Tome'].cost = 30
        self.cargo['Fine Jewelry'].cost = 80
        self.cargo['Dark Crystals'].cost = 50
        self.total_cargo = 25

class Frigate(Ship):
    def __init__(self):
        super().__init__(name = 'Frigate', 
                       hp = 50, 
                       speed = 15, 
                       crew = 55, 
                       price = 500_000, 
                       cargo_sz = 60)