from cities import City, WestEurope
from player import Player
from constants import *
import landcheck
import pygame, pygame_gui
import sys, copy, os, pickle, math
from pygame_gui.elements.ui_window import UIWindow
from pygame_gui.elements.ui_label import UILabel
from pygame_gui.elements.ui_button import UIButton
from pygame_gui.elements.ui_text_entry_line import UITextEntryLine
from typing import Dict

# Create landcheck list
if not os.path.exists('data/landcheck.pkl'):
    landcheck.create()

# default player
player = Player('I was too lazy to change from Default', WestEurope, WestEurope.cities['Seville'])

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
# Can likely just save player state to a txt file
# can probs use pickle for this
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
                sys.exit()

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
                    player = Player(f'{self.player_name.text}', WestEurope, WestEurope.cities['Viremontis'])
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
        if player.ship.current_health <= 0:
            player.ship.current_health = round(0.5 * player.ship.health_capacity)
            cost = round(player.currency * 0.1)
            player.currency -= cost
            self.NPC_speech.set_text(f'Your ship has reached 0 durability, you have sunk.\nWe have repaired your ship to {player.ship.current_health} durability for {cost} gold.')

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
                CityScreen(self.screen, self.city).mainloop()

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
        vertical_pos = 200 

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

        for product in player.ship.cargo.values():
            vertical_pos += 50
            self.labels[product.name] = pygame_gui.elements.UILabel(text=f'{product.name}',
                                        relative_rect=pygame.Rect((-300, vertical_pos), (150, 25)),
                                        manager=self.manager,
                                        anchors={'centerx': 'centerx'}
                                        )
            
            price = self.city.get_selling_price(product)
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

        if len(player.ship.cargo) == 0:
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
                        price = self.city.get_selling_price(player.ship.cargo[product])
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
        vertical_pos = 200

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
        self.locations = {}

    def objects(self):
        super().objects()        
        self.sail_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,275), (100, 50)),
                                                        text = 'Set Sail',
                                                        manager=self.manager,
                                                    anchors={'centerx': 'centerx'})
        self.exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,20), (100, 50)),
                                                    text = 'Leave',
                                                    manager=self.manager,
                                                    anchors={'centerx': 'centerx',
                                                             'top_target': self.sail_button})        
    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.exit_button: 
                self.is_running = False  
            if event.ui_element == self.sail_button:
                self.is_running = False
                SailingScreen(self.screen).mainloop()

# start with just generating random events
# implement food requirement
class SailingScreen(GameScreen):
    def __init__(self, screen):
        super().__init__(screen)

        self.left = player.ship.coords[0]
        self.top = player.ship.coords[1]
        self.viewport = self.centre_viewport(*player.location.coords, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.region = player.region
        self.mouse_x, self.mouse_y = 0, 0
        self.color = pygame.Color(255,255,255)

    def centre_viewport(self, x, y, viewport_x, viewport_y):
        '''
        returns a viewport Rect of size (viewport_x, viewport_y) centered on coords (x, y)
        '''
        centre_x = x - viewport_x / 2
        centre_y = y - viewport_y / 2
        return pygame.Rect(centre_x, centre_y, viewport_x, viewport_y)    

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
        '''
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.left += 1
            if event.key == pygame.K_LEFT:
                self.left -= 1
            if event.key == pygame.K_DOWN:
                self.top += 1
            if event.key == pygame.K_UP:
                self.top -= 1
            self.viewport = self.centre_viewport(self.left, self.top, SCREEN_WIDTH, SCREEN_HEIGHT)
        '''

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
        self.ship_durability = pygame_gui.elements.UIScreenSpaceHealthBar(relative_rect=pygame.Rect((50, 25), (200, 25)),
                                                                        manager=self.manager,
                                                                        anchors={'left': 'left',
                                                                        'top_target': self.currency})
        self.ship_durability.set_sprite_to_monitor(player.ship)
        self.player_energy = pygame_gui.elements.UIScreenSpaceHealthBar(relative_rect=pygame.Rect((50, 25), (200, 25)),
                                                                        manager=self.manager,
                                                                        anchors={'left': 'left',
                                                                        'top_target': self.ship_durability})
        self.player_energy.bar_filled_colour = 'blue'
        self.coordinates = pygame_gui.elements.UILabel(text=f'Mouse coords: {self.mouse_x}, {self.mouse_y}',
                                                        relative_rect=pygame.Rect((-225, -50), (200, 25)),
                                                        manager=self.manager,
                                                        anchors={'right': 'right',
                                                                 'bottom': 'bottom'})       
        self.color_label = pygame_gui.elements.UILabel(text=f'Color: {self.color}',
                                                        relative_rect=pygame.Rect((-245, -20), (220, 25)),
                                                        manager=self.manager,
                                                        anchors={'right': 'right',
                                                                 'bottom': 'bottom',
                                                                 'bottom_target': self.coordinates})
 
    def mainloop(self):
        self.is_running = True
        player.prev_location = player.location
        player.ship.coords = pygame.Vector2(*player.location.harbour)

        ship_harbour_angle = get_angle_between_points(player.location.coords.x, 
                                                        player.location.coords.y,
                                                        player.location.harbour.x,
                                                        player.location.harbour.y)
        player.ship.reset_angle(ship_harbour_angle)
        self.objects()

        ships = pygame.sprite.Group()
        cities = pygame.sprite.Group()

        ships.add(player.ship)
        for city in self.region.cities.values():
            cities.add(city)

        while self.is_running:
            # limit the frame rate to 60 fps
            dt = self.clock.tick(60) / 1000

            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    self.is_running = False
                    pygame.quit()
                    sys.exit()
        
                self.handle_event(event)
                self.manager.process_events(event)    

            for city in cities:
                if player.ship.collision(city) and player.location != city:
                    player.location = city
                    self.is_running = False
                    CityScreen(self.screen, city).mainloop()
                if not player.ship.collision(city) and player.location == city:
                    player.location = None
                    city.reset_market()

            if player.ship.current_health <= 0:
                self.is_running = False
                player.location = player.prev_location
                player.ship.coords = player.location.coords
                player.ship.rotation = 0
                CityScreen(self.screen, player.location).mainloop()

            # UI Elements
            self.update_gold()
            self.manager.update(dt)

            # Update
            ships.update(dt)
            cities.update(dt)

            # Render
            self.screen.fill((255,255,255))
            bg = copy.copy(gamemap)
            ships.draw(bg)
            cities.draw(bg)

            # Add map viewport
            self.viewport = self.centre_viewport(*player.ship.coords, SCREEN_WIDTH, SCREEN_HEIGHT)
            self.screen.blit(source=bg, dest=(0,0), area=self.viewport)

            # Get the current mouse position
            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
            self.mouse_x += self.viewport.left
            self.mouse_y += self.viewport.top
            self.coordinates.set_text(f'Mouse coords: {self.mouse_x}, {self.mouse_y}')
            self.color_label.set_text(f'Color: {bg.get_at((self.mouse_x, self.mouse_y))}')

            self.manager.draw_ui(self.screen)

            # updates the frames of the game
            pygame.display.update() 

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
                                                    relative_rect=pygame.Rect(0, 25, 250, 50),
                                                    manager=self.manager,
                                                    container=self,
                                                    anchors={'centerx': 'centerx'})
        self.location = pygame_gui.elements.UILabel(text=f'Current City: {player.location.name}',
                                                    relative_rect=pygame.Rect(0, 25, 250, 25),
                                                    manager=self.manager,
                                                    container=self,
                                                    anchors={'centerx': 'centerx',
                                                             'top_target': self.player_name})
        self.currency = pygame_gui.elements.UILabel(text=f'Gold: {player.currency}',
                                                    relative_rect=pygame.Rect(0, 25, 250, 25),
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
        self.buttons: Dict[str, UIButton] = {}
        self.objects()

    def objects(self):
        item_size = (100, 100)
        spacing = 150
        top_spacing = 50
        i = 0
        for item in player.inventory.keys():
            if i == 4:
                i = 0
                top_spacing += spacing
            self.buttons[item] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(50+i*spacing, top_spacing, *item_size),
                                                                text = item,
                                                                manager=self.manager,
                                                                container=self)
            pygame_gui.elements.UILabel(relative_rect=pygame.Rect((-35,-30), (25,20)),
                                        text=f'{player.inventory[item]['qty']}',
                                        container=self,
                                        manager=self.manager,
                                        anchors={'top_target':self.buttons[item],
                                                 'left_target':self.buttons[item]})
            i += 1

    def handle_event(self, event):
        if event.type == pygame_gui.UI_WINDOW_RESIZED:    
            self.width, self.height = event.internal_size

class CargoScreen(PopUpScreen):
    def __init__(self, name: str, manager: pygame_gui.UIManager, size: tuple):
        super().__init__(name, manager, size)
        self.buttons: Dict[str, UIButton] = {}
        self.objects()

    def objects(self):
        item_size = (100, 100)
        spacing = 150
        top_spacing = 50
        i = 0
        for item in player.ship.cargo:
            if i == 4:
                i = 0
                top_spacing += spacing
            self.buttons[item] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(50+i*spacing, top_spacing, *item_size),
                                        text = item,
                                        manager=self.manager,
                                        container=self)
            pygame_gui.elements.UILabel(relative_rect=pygame.Rect((-35,-30), (25,20)),
                                        text=f'{player.ship.cargo[item].qty}',
                                        container=self,
                                        manager=self.manager,
                                        anchors={'top_target':self.buttons[item],
                                                 'left_target':self.buttons[item]})
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

def get_angle_between_points(x1, y1, x2, y2):
    """
    Calculates the angle (in degrees) of the line segment from (x1, y1) to (x2, y2)
    relative to the positive x-axis.

    Args:
        x1, y1: Coordinates of the first point.
        x2, y2: Coordinates of the second point.

    Returns:
        The angle in degrees, ranging from -180 to 180.
    """
    dx = x2 - x1
    dy = y2 - y1
    angle_radians = math.atan2(dy, dx)
    angle_degrees = math.degrees(angle_radians)
    return angle_degrees

def main():
    global gamemap, land
    pygame.init()
    pygame.display.set_caption('Trader')
    options = Options()
    screen = pygame.display.set_mode(options.resolution)

    with open('data/landcheck.pkl', 'rb') as file:
        land = pickle.load(file)

    # Generate map
    image_path = "images/MapChart_Map.png"
    image = pygame.image.load(image_path)
    pixel_array = pygame.surfarray.array3d(image)
    gamemap = pygame.surfarray.make_surface(pixel_array)

    StartScreen(screen).mainloop()

if __name__ == "__main__":
    main()
