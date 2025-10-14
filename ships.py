from goods import *
from typing import Dict
from constants import *
import pygame, pickle, os
import landcheck

# Create landcheck list
if not os.path.exists('data/landcheck.pkl'):
    landcheck.create()

with open('data/landcheck.pkl', 'rb') as file:
    land = pickle.load(file)

class Ship(pygame.sprite.Sprite):
    def __init__(self, name, hp, speed, crew, price, cargo_sz, coords = (0,0), cargo_slots=12):
        super().__init__()
        self.name = name

        # Position
        self.coords = pygame.Vector2(*coords)
        self.direction = pygame.Vector2((0, -1))
        self.rotation = 0
        self.radius = SHIP_RADIUS

        # Image
        self.image = pygame.Surface((self.radius,self.radius), pygame.SRCALPHA)
        self.image.fill('white')
        self.image.set_colorkey('white')
        self.icon(self.image)
        self.image_org = self.image.copy()
        self.rect = self.image.get_rect(center=self.coords)

        self.interact_radius = PLAYER_INTERACT_RADIUS
        self.turn_speed = 25 # turn speed in degrees per second

        # Stats
        self.health_capacity = hp
        self.current_health = hp
        self.speed = speed
        self.crew = crew
        self.price = price
        self.total_cargo = 0
        self.cargo_sz = cargo_sz
        self.cargo_slots = cargo_slots
        self.cargo: Dict[str, Product]

        self.timer = 0
        self.last_grounded = 0

    def icon(self, screen):
        # adjust for indexing from 0
        adj_radius = self.radius -1
        a = (adj_radius/2, 0)
        b = (adj_radius/4, adj_radius)
        c = (self.radius - adj_radius/4, adj_radius)
        return pygame.draw.polygon(screen, 'black', (a,b,c), 2)
    
    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.timer += dt
        self.last_grounded += dt
        movement = 0

        if keys[pygame.K_LEFT]:
            self.direction.rotate_ip(dt*-self.turn_speed)
            self.rotation += dt*-self.turn_speed
        if keys[pygame.K_RIGHT]:
            self.direction.rotate_ip(dt*self.turn_speed)
            self.rotation += dt*self.turn_speed
        if keys[pygame.K_UP]:
            movement = 1
        if keys[pygame.K_DOWN]:
            movement = -1

        velocity = self.direction * movement
        if velocity.length() > 0:
            velocity.normalize_ip()
            self.coords += velocity * dt * self.speed

        self.image = pygame.transform.rotate(self.image_org, self.direction.angle_to((0,-1)))
        self.rect = self.image.get_rect(center=self.coords)  

        if land[round(self.coords.x)][round(self.coords.y)]:
            if self.last_grounded > GROUNDED_TIMER:
                self.current_health -= self.health_capacity * 0.2
                self.last_grounded = 0

    def reset_angle(self, angle):
        self.direction.rotate_ip(-self.rotation)
        # account for drawn angle
        self.rotation = angle+90
        self.direction.rotate_ip(angle+90)

    def collision(self, other):
        if self.coords.distance_to(other.coords) <= (self.interact_radius + other.interact_radius):
            return True
        return False

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