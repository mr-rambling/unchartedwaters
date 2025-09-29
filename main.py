from cities import City, Region, Velmore
from player import Player
from constants import *
import pygame
import pygame_gui
import sys
from pygame_gui.elements.ui_window import UIWindow
from pygame_gui.elements.ui_label import UILabel
from pygame_gui.elements.ui_text_entry_line import UITextEntryLine
from typing import Dict

# placeholder player
player = Player('I was too lazy to change from Default', Velmore, Velmore.cities['Viremontis'])

# Contains base state of game options
class Options():
    def __init__(self):
        self.resolution = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.fullscreen = False

# Template for all further Screens
# Realistically just SettingsScreen and NewGameScreen screen as GameScreen rebuilds most of it
class Stage():
    def __init__(self, screen):
        self.pos = (0,0)
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill((60,25,60))

    def objects(self):
        pass

    def handle_event(self, event):
        pass

    def mainloop(self):
        self.is_running = True
        self.objects()

        while self.is_running:
            time_delta = self.clock.tick(60)/1000.0
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    self.is_running = False
                    pygame.quit()
                    sys.exit()
            
                self.handle_event(event)

                self.manager.process_events(event)

            self.manager.update(time_delta)

            self.screen.blit(self.background, self.pos)
            self.manager.draw_ui(self.screen)

            # updates the frames of the game
            pygame.display.update()            

# Need to figure out load mechanics. 
# Load is currently non-functional
class StartScreen(Stage):
    def __init__(self, screen):
        super().__init__(screen)

    def objects(self):
        self.welcome_text = pygame_gui.elements.UITextBox(html_text=f'Welcome to {GAME_NAME}!',
                                                    relative_rect=pygame.Rect(0, 100, 400, 100),
                                                    manager=self.manager,
                                                    anchors={'centerx': 'centerx'})
        self.new_game_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,275), (100, 50)),
                                                    text = 'New Game',
                                                    manager=self.manager,
                                                    anchors={'centerx': 'centerx'})    
        self.load_game_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,20), (100, 50)),
                                                    text = 'Load Game',
                                                    manager=self.manager,
                                                    anchors={'centerx': 'centerx',
                                                            'top_target': self.new_game_button})    
        self.settings_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,20), (100, 50)),
                                                    text = 'Settings',
                                                    manager=self.manager,
                                                    anchors={'centerx': 'centerx',
                                                            'top_target': self.load_game_button})
        self.exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,20), (100, 50)),
                                                    text = 'Exit',
                                                    manager=self.manager,
                                                    anchors={'centerx': 'centerx',
                                                            'top_target': self.settings_button})
        
    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.new_game_button:
                print('New Game')
                NewGameScreen(self.screen).mainloop()
            if event.ui_element == self.load_game_button:
                print('Load Game')
            if event.ui_element == self.settings_button:
                SettingsScreen(self.screen).mainloop()
            if event.ui_element == self.exit_button:
                self.is_running = False   
                pygame.quit()
                sys.quit()

# Could add an option here for starting city
class NewGameScreen(Stage):
    def __init__(self, screen):
        super().__init__(screen)

    def objects(self):
        self.welcome_text = pygame_gui.elements.UITextBox(html_text=f'Insert lore here',
                                                    relative_rect=pygame.Rect(0, 100, 400, 100),
                                                    manager=self.manager,
                                                    anchors={'centerx': 'centerx'})
        self.player_name = pygame_gui.elements.UITextEntryLine(placeholder_text='What is your name?',
                                                    relative_rect=pygame.Rect(0, 50, 400, 50),
                                                    manager=self.manager,
                                                    anchors={'centerx': 'centerx',
                                                             'top_target': self.welcome_text}) 
        self.confirm_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,20), (200, 50)),
                                                    text = 'Create Character',
                                                    manager=self.manager,
                                                    anchors={'centerx': 'centerx',
                                                            'top_target': self.player_name})
        self.exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,20), (100, 50)),
                                                    text = 'Back',
                                                    manager=self.manager,
                                                    anchors={'centerx': 'centerx',
                                                            'top_target': self.confirm_button})

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.confirm_button:
                self.is_running = False
                if self.player_name.text != '':
                    global player 
                    player = Player(f'{self.player_name.text}')
                CityScreen(self.screen, player.location).mainloop()
            if event.ui_element == self.exit_button:
                self.is_running = False   

class SettingsScreen(Stage):
    def __init__(self, screen):
        super().__init__(screen)

    def objects(self):
        self.resolution = pygame_gui.elements.UIDropDownMenu(options_list=['640x480', '800x600', '1024x768', '1280x720'],
                                                            starting_option='1280x720',
                                                            relative_rect=pygame.Rect((0,275),(200, 50)),
                                                            manager=self.manager,
                                                            anchors={'centerx': 'centerx'}) 
        self.exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,20), (100, 50)),
                                                        text = 'Exit',
                                                        manager=self.manager,
                                                        anchors={'centerx': 'centerx',
                                                        'top_target': self.resolution}) 
        
    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.exit_button:
                self.is_running = False

class GameScreen(Stage):
    def __init__(self, screen):
        super().__init__(screen)
        self.manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT)) # Need to add scaling here
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))        
        self.background.fill((60,25,60))
        self.inventory = None
        self.cargo = None
        self.char_sheet = None

    def objects(self):
        self.inventory_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-150,20), (100, 30)),
                                                    text = 'Inventory',
                                                    manager=self.manager,
                                                    anchors={'right':'right'})
        self.cargo_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-100,20), (100, 30)),
                                                    text = 'Cargo',
                                                    manager=self.manager,
                                                    anchors={'right':'right',
                                                             'right_target':self.inventory_button})
        self.character_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-100,20), (100, 30)),
                                                    text = 'Character',
                                                    manager=self.manager,
                                                    anchors={'right':'right',
                                                             'right_target':self.cargo_button})
        self.currency = pygame_gui.elements.UILabel(text=f'Gold: {player.currency}',
                                                    relative_rect=pygame.Rect((50, 25), (100, 25)),
                                                    manager=self.manager,
                                                    anchors={'left': 'left'})
        self.player_health = pygame_gui.elements.UIScreenSpaceHealthBar(relative_rect=pygame.Rect((50, 25), (200, 25)),
                                                                        manager=self.manager,
                                                                        anchors={'left': 'left',
                                                                        'top_target': self.currency})
        self.player_energy = pygame_gui.elements.UIScreenSpaceHealthBar(relative_rect=pygame.Rect((50, 25), (200, 25)),
                                                                        manager=self.manager,
                                                                        anchors={'left': 'left',
                                                                        'top_target': self.player_health})
        self.player_energy.bar_filled_colour = 'blue'

        
    def handle_event(self, event):
        if self.inventory and self.inventory.is_active:
            self.inventory.handle_event(event)
        if self.cargo and self.cargo.is_active:
            self.cargo.handle_event(event)   
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.inventory_button:
                self.inventory = InvScreen('Inventory', self.manager, INV_SCREEN)
                self.inventory.is_active = True
            if event.ui_element == self.cargo_button:
                self.cargo = CargoScreen('Cargo', self.manager, INV_SCREEN)
                self.cargo.is_active = True   
            if event.ui_element == self.character_button:         
                self.char_sheet = CharScreen('Character', self.manager, CHAR_SHEET_SIZE)   
                self.char_sheet.is_active = True

    def update_gold(self):
        self.currency.set_text(f'Gold: {player.currency}')

    def mainloop(self):
        self.is_running = True
        self.objects()

        while self.is_running:
            time_delta = self.clock.tick(60)/1000.0
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    self.is_running = False
                    pygame.quit()
                    sys.exit()
        
                self.handle_event(event)
                self.manager.process_events(event)    

            self.manager.update(time_delta)
            self.update_gold()
            self.screen.blit(self.background, (0,0))
            self.manager.draw_ui(self.screen)

            # updates the frames of the game
            pygame.display.update()   

# Save button is not linked to anything
class CityScreen(GameScreen):
    def __init__(self, screen, city: City):
        super().__init__(screen)
        self.city = city

    def objects(self):
        super().objects()
        self.NPC_speech = pygame_gui.elements.UITextBox(html_text=f'Welcome to {self.city.name}!',
                                                    relative_rect=pygame.Rect(0, 100, 400, 100),
                                                    manager=self.manager,
                                                    anchors={'centerx': 'centerx'})
        self.market_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,275), (300, 50)),
                                                    text = 'Market',
                                                    manager=self.manager,
                                                    anchors={'centerx': 'centerx'})    
        self.port_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,20), (300, 50)),
                                                    text = 'Port',
                                                    manager=self.manager,
                                                    anchors={'centerx': 'centerx',
                                                            'top_target': self.market_button})
        self.save_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,20), (300, 50)),
                                                    text = 'Save Game',
                                                    manager=self.manager,
                                                    anchors={'centerx': 'centerx',
                                                            'top_target': self.port_button})
        self.exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,20), (300, 50)),
                                                    text = 'Quit',
                                                    manager=self.manager,
                                                    anchors={'centerx': 'centerx',
                                                            'top_target': self.save_button})

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.market_button:
                ShopScreen(self.screen, self.city).mainloop()
            if event.ui_element == self.port_button:
                self.is_running = False
                PortScreen(self.screen).mainloop()    
            if event.ui_element == self.save_button:
                pass
            if event.ui_element == self.exit_button:
                self.is_running = False
                pygame.quit()
                sys.exit()

class ShopScreen(GameScreen):   
    def __init__(self, screen, city):
        super().__init__(screen)
        self.city = city

    def objects(self):
        super().objects()
        self.NPC_speech = pygame_gui.elements.UITextBox(html_text=f'Welcome to {GAME_NAME}!',
                                                    relative_rect=pygame.Rect(0, 100, 400, 100),
                                                    manager=self.manager,
                                                    anchors={'centerx': 'centerx'})
        self.buy_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,275), (100, 50)),
                                                    text = 'Buy',
                                                    manager=self.manager,
                                                    anchors={'centerx': 'centerx'})    
        self.sell_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,20), (100, 50)),
                                                    text = 'Sell',
                                                    manager=self.manager,
                                                    anchors={'centerx': 'centerx',
                                                            'top_target': self.buy_button})    
        self.exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,20), (100, 50)),
                                                    text = 'Leave',
                                                    manager=self.manager,
                                                    anchors={'centerx': 'centerx',
                                                            'top_target': self.sell_button})              

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.buy_button:
                BuyScreen(self.screen, self.city).mainloop()
            if event.ui_element == self.sell_button:
                SellScreen(self.screen, self.city).mainloop()
            if event.ui_element == self.exit_button: 
                self.is_running = False       

class SellScreen(GameScreen):
    def __init__(self, screen, city):
        super().__init__(screen)
        self.city = city

        self.labels = {}
        self.prices = {}
        self.entries = {}
        self.qty = {}

    def objects(self):
        super().objects()
        vertical_pos = 100 

        product_label = pygame_gui.elements.UILabel(text=f'Product',
                                        relative_rect=pygame.Rect((-300, vertical_pos), (150, 25)),
                                        manager=self.manager,
                                        anchors={'centerx': 'centerx'}
                                        )
        price_label = pygame_gui.elements.UILabel(text='Price',
                                        relative_rect=pygame.Rect((-100, vertical_pos), (150, 25)),
                                        manager=self.manager,
                                        anchors={'centerx': 'centerx'}
                                        )
        qty_available = pygame_gui.elements.UILabel(text='Qty Owned',
                                                relative_rect=pygame.Rect((100, vertical_pos), (150, 25)),
                                                manager=self.manager,
                                                anchors={'centerx': 'centerx'}
                                                )
        qty_label = pygame_gui.elements.UILabel(text='Sell Qty',
                                                relative_rect=pygame.Rect((300, vertical_pos), (150, 25)),
                                                manager=self.manager,
                                                anchors={'centerx': 'centerx'}
                                               )

        for product in player.cargo.values():
            vertical_pos += 50
            self.labels[product.name] = pygame_gui.elements.UILabel(text=f'{product.name}',
                                        relative_rect=pygame.Rect((-300, vertical_pos), (150, 25)),
                                        manager=self.manager,
                                        anchors={'centerx': 'centerx'}
                                        )
            if product in self.city.products:
                price = round(self.city.products[product].value * IN_STOCK_VALUE_MODIFIER)
            else:
                price = round(product.cost * BASE_SALE_COST_MODIFIER)
            self.prices[product.name] = pygame_gui.elements.UILabel(text=f'{price}',
                                        relative_rect=pygame.Rect((-100, vertical_pos), (150, 25)),
                                        manager=self.manager,
                                        anchors={'centerx': 'centerx'}
                                        )
            self.qty[product.name] = pygame_gui.elements.UILabel(text=f'{product.qty}',
                                        relative_rect=pygame.Rect((100, vertical_pos), (150, 25)),
                                        manager=self.manager,
                                        anchors={'centerx': 'centerx'}
                                        )
            self.entries[product.name] = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((300, vertical_pos), (150, 25)),
                                                manager=self.manager,
                                                placeholder_text='Qty',
                                                anchors={'centerx': 'centerx'}
                                               )

        if len(player.cargo) == 0:
            top_target = 'top'
            top_spacing = 300
        else:
            top_target = list(self.entries.values())[-1]
            top_spacing = 20


        self.sell_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100,top_spacing), (100, 50)),
                                                    text = 'Sell',
                                                    manager=self.manager,
                                                    anchors={'centerx': 'centerx',
                                                            'top_target': top_target}
                                                            )    
        self.exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-100,top_spacing), (100, 50)),
                                                    text = 'Leave',
                                                    manager=self.manager,
                                                    anchors={'centerx': 'centerx',
                                                            'top_target': top_target}
                                                            )  

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.sell_button:
                for product in self.entries:
                    if self.entries[product].text.isdigit():
                        qty = int(self.entries[product].text)
                        if product in self.city.products:
                            price = self.city.products[product].value * IN_STOCK_VALUE_MODIFIER
                        else:
                            price = player.cargo[product].cost * BASE_SALE_COST_MODIFIER
                        player.sell_cargo(product, price, qty)
                self.is_running = False
            if event.ui_element == self.exit_button:
                self.is_running = False

class BuyScreen(GameScreen):
    def __init__(self, screen, city: City):
        super().__init__(screen)

        self.labels: Dict[str, UILabel] = {}
        self.prices: Dict[str, UILabel] = {}
        self.entries: Dict[str, UITextEntryLine] = {}
        self.qty: Dict[str, UILabel] = {}
        self.city = city

    def objects(self):
        super().objects()
        vertical_pos = 100

        product_label = pygame_gui.elements.UILabel(text=f'Product',
                                        relative_rect=pygame.Rect((-300, vertical_pos), (150, 25)),
                                        manager=self.manager,
                                        anchors={'centerx': 'centerx'}
                                        )
        price_label = pygame_gui.elements.UILabel(text='Price',
                                        relative_rect=pygame.Rect((-100, vertical_pos), (150, 25)),
                                        manager=self.manager,
                                        anchors={'centerx': 'centerx'}
                                        )
        qty_available = pygame_gui.elements.UILabel(text='Qty Available',
                                                relative_rect=pygame.Rect((100, vertical_pos), (150, 25)),
                                                manager=self.manager,
                                                anchors={'centerx': 'centerx'}
                                               )
        qty_label = pygame_gui.elements.UILabel(text='Buy Qty',
                                                relative_rect=pygame.Rect((300, vertical_pos), (150, 25)),
                                                manager=self.manager,
                                                anchors={'centerx': 'centerx'}
                                               )
        
        for product in self.city.products.values():
            vertical_pos += 50
            self.labels[product.name] = pygame_gui.elements.UILabel(text=f'{product.name}',
                                        relative_rect=pygame.Rect((-300, vertical_pos), (150, 25)),
                                        manager=self.manager,
                                        anchors={'centerx': 'centerx'}
                                        )
            self.prices[product.name] = pygame_gui.elements.UILabel(text=f'{product.value}',
                                        relative_rect=pygame.Rect((-100, vertical_pos), (150, 25)),
                                        manager=self.manager,
                                        anchors={'centerx': 'centerx'}
                                        )
            self.qty[product.name] = pygame_gui.elements.UILabel(text=f'{product.qty}',
                                        relative_rect=pygame.Rect((100, vertical_pos), (150, 25)),
                                        manager=self.manager,
                                        anchors={'centerx': 'centerx'}
                                        )
            self.entries[product.name] = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((300, vertical_pos), (150, 25)),
                                                manager=self.manager,
                                                placeholder_text='Qty',
                                                anchors={'centerx': 'centerx'}
                                               )

        top_target = list(self.entries.values())[-1]
        top_spacing = 20


        self.buy_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100,top_spacing), (100, 50)),
                                                    text = 'Buy',
                                                    manager=self.manager,
                                                    anchors={'centerx': 'centerx',
                                                            'top_target': top_target}
                                                            )    
        self.exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-100,top_spacing), (100, 50)),
                                                    text = 'Leave',
                                                    manager=self.manager,
                                                    anchors={'centerx': 'centerx',
                                                            'top_target': top_target}
                                                            )  

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.buy_button:
                for product in self.entries:
                    if self.entries[product].text.isdigit():
                        qty = int(self.entries[product].text)
                        qty = min(self.city.products[product].qty, qty)
                        price = self.city.products[product].value
                        qty_bought = player.buy_cargo(self.city.products[product], price, qty)
                        self.city.products[product].qty -= qty_bought
                self.is_running = False
            if event.ui_element == self.exit_button:
                self.is_running = False

class PortScreen(GameScreen):
    def __init__(self, screen):
        super().__init__(screen)

# This is pretty ambitious. Generate a map of the coastline and cities
# with a moving dot (arrow?) for the current location
class SailingScreen(GameScreen):
    def __init__(self, screen):
        super().__init__(screen)

class PopUpScreen(UIWindow):
    def __init__(self, name: str, manager: pygame_gui.UIManager, size: tuple):
        super().__init__(pygame.Rect(*POPUP_TOPLEFT, *size),
                                    manager=manager,
                                    window_display_title=name,
                                    resizable=True,
                                    object_id=f'#{name}')
        self.manager = manager
        self.is_active = False
        self.width, self.height = size
        self.objects()

    def on_close_window_button_pressed(self):
        self.hide()
        self.is_active = False

    def objects(self):
        pass

    def handle_event(self, event):
        pass

# Need to turn the player class into a sprite for hp/energy bars
class CharScreen(PopUpScreen):
    def __init__(self, name: str, manager: pygame_gui.UIManager, size: tuple):
        super().__init__(name, manager, size)
        self.inv = None
        self.cargo = None

    def objects(self):
        self.player_name = pygame_gui.elements.UITextBox(html_text=f'{player.name}',
                                                    relative_rect=pygame.Rect(0, 25, 400, 50),
                                                    manager=self.manager,
                                                    container=self,
                                                    anchors={'centerx': 'centerx'})
        self.location = pygame_gui.elements.UILabel(text=f'Current City: {player.location}',
                                                    relative_rect=pygame.Rect(0, 25, 400, 25),
                                                    manager=self.manager,
                                                    container=self,
                                                    anchors={'centerx': 'centerx',
                                                             'top_target': self.player_energy})
        self.currency = pygame_gui.elements.UILabel(text=f'Gold: {player.currency}',
                                                    relative_rect=pygame.Rect(0, 25, 400, 25),
                                                    manager=self.manager,
                                                    container=self,
                                                    anchors={'centerx': 'centerx',
                                                             'top_target': self.location})


    def handle_event(self, event):
        if event.type == pygame_gui.UI_WINDOW_RESIZED:    
            self.width, self.height = event.internal_size
            self.player_health.set_dimensions((self.width-50, 25))
            self.player_energy.set_dimensions((self.width-50, 25))
        if event.type == pygame.KEYDOWN and not self.is_active:
            if event.key == pygame.K_c:
                self.show()
                self.is_active = True

class InvScreen(PopUpScreen):
    def __init__(self, name: str, manager: pygame_gui.UIManager, size: tuple):
        super().__init__(name, manager, size)
        self.objects()
        self.qty_held = 0

    def objects(self):
        item_size = (100, 100)
        spacing = 150
        top_spacing = 50
        i = 0
        for item in player.inventory:
            if i == 4:
                i = 0
                top_spacing += spacing
            pygame_gui.elements.UIButton(relative_rect=pygame.Rect(50+i*spacing, top_spacing, *item_size),
                                        text = item,
                                        manager=self.manager,
                                        container=self)
            i += 1

    def handle_event(self, event):
        if event.type == pygame_gui.UI_WINDOW_RESIZED:    
            self.width, self.height = event.internal_size
        if event.type == pygame_gui.UI_BUTTON_PRESSED and False:
            qty_owned = player.inventory[event.ui_element.text]['qty']
            if pygame.key == (pygame.K_LSHIFT or pygame.K_RSHIFT):
                self.qty_held = qty_owned
            elif pygame.key == (pygame.K_LALT or pygame.K_RALT):
                self.qty_held += min(qty_owned, 10)
            else:
                self.qty_held += 1
            self.qty_held = max(qty_owned, self.qty_held)

class CargoScreen(PopUpScreen):
    def __init__(self, name: str, manager: pygame_gui.UIManager, size: tuple):
        super().__init__(name, manager, size)
        self.objects()

    def objects(self):
        item_size = (100, 100)
        spacing = 150
        top_spacing = 50
        i = 0
        for item in player.cargo:
            if i == 4:
                i = 0
                top_spacing += spacing
            pygame_gui.elements.UIButton(relative_rect=pygame.Rect(50+i*spacing, top_spacing, *item_size),
                                        text = item['name'],
                                        manager=self.manager,
                                        container=self)
            i += 1

    def handle_event(self, event):
        if event.type == pygame_gui.UI_WINDOW_RESIZED:    
            self.width, self.height = event.internal_size
        if event.type == pygame_gui.UI_BUTTON_PRESSED and pygame.KEYDOWN and False:
            qty_owned = player.inventory[event.ui_element.text]['qty']
            if event.key == (pygame.K_LSHIFT or pygame.K_RSHIFT):
                qty_held = qty_owned
            if event.key == (pygame.K_LALT or pygame.K_RALT):
                qty_held += min(qty_owned, 10)

def main():
    pygame.init()
    pygame.display.set_caption('Trader')
    options = Options()
    screen = pygame.display.set_mode(options.resolution)

    StartScreen(screen).mainloop()

if __name__ == "__main__":
    main()
