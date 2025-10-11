from goods import *
from typing import Dict
from constants import *
import pygame

class Ship(pygame.sprite.Sprite):
    def __init__(self, name, hp, speed, crew, price, cargo_sz, coords = (0,0), cargo_slots=12):
        super().__init__()
        self.name = name
        self.coords = pygame.Vector2(*coords)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = PLAYER_RADIUS
        self.turn_speed = 25
        self.rotation = 0
        self.hp = hp
        self.speed = speed
        self.crew = crew
        self.price = price
        self.total_cargo = 0
        self.cargo_sz = cargo_sz
        self.cargo_slots = cargo_slots
        self.cargo: Dict[str, Product]
        self.width = 10
        self.height = 20
        self.timer = 0

    def move_speed(self):
        base = 500
        return int(base / self.speed)

    def icon(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.coords + forward * self.radius
        b = self.coords - forward * self.radius - right
        c = self.coords - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        return pygame.draw.polygon(screen, 'black', self.icon(), 2)
    
    def rotate(self, dt):
        self.rotation += self.turn_speed * dt       

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.timer -= dt

        if keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_UP]:
            self.move(dt)
        if keys[pygame.K_DOWN]:
            self.move(-dt)

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.coords += forward * self.speed * dt          

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
                        speed = 10, 
                        crew = 7, 
                        price = 2_000, 
                        cargo_sz = 25)
        self.coords = pygame.Vector2(*SEVILLE)
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