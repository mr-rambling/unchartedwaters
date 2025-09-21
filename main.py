from cities import Cities, City, cities
from player import Player
from constants import *
import pygame
import pygame_gui
import sys

class World:
    def __init__(self):
        self.cities = Cities()
        for city in cities:
            self.cities.add_city(city)

        self.cities.get_city("Viremontis").add_product("Magical Tomes", 10, 1.2)

class Options():
    def __init__(self):
        self.resolution = (SCREEN_HEIGHT, SCREEN_WIDTH)
        self.fullscreen = False

class Stage():
    def __init__(self, screen):
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

            self.screen.blit(self.background, (0,0))
            self.manager.draw_ui(self.screen)

            # updates the frames of the game
            pygame.display.update()            


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
            if event.ui_element == self.load_game_button:
                print('Load Game')
            if event.ui_element == self.settings_button:
                print('Settings')
                SettingsScreen(self.screen, self.manager).mainloop()
            if event.ui_element == self.exit_button:
                self.is_running = False   

class SettingsScreen(Stage):
    def __init__(self, screen):
        super().__init__(screen)

    def objects(self):
        self.resolution = pygame_gui.elements.UIDropDownMenu(options_list=['640x480', '800x600', '1024x768', '1280x720'],
                                                            starting_option='1280x720',
                                                            relative_rect=pygame.Rect((500,400),(200, 30)),
                                                            manager=self.manager)  

def main_n():
    pygame.init()
    pygame.display.set_caption('Trader')
    options = Options()
    screen = pygame.display.set_mode(options.resolution)

    StartScreen(screen).mainloop()


def main():
    world = World()
    print("Hello from unchartedwaters!")
    player = Player("Hero")
    player.location = world.cities.get_city("Viremontis")
    print(f"You are currently in {player.location.name}.")

    while True:
        print(f"You have {player.currency} gold.")
        print("What would you like to do?")
        print("1. Visit Shop")
        print("2. Check Inventory")
        print("3. Manage Cargo")
        print("4. Leave City")
        choice = input("Enter your choice: ")
        if choice == "1":
            shop(player)
        elif choice == "2":
            print("Your inventory:")
            for item in player.get_inventory():
                print(f"- {item}")
        elif choice == "3":
            print("Your cargo:")
            for product in player.get_cargo():
                print(f"- {product}: {player.get_cargo()[product]['qty']}")
        elif choice == "4":
            print("Leaving city...")
            break
        else:
            print("Invalid choice.")
        print("--------------------")

def shop(player):
    city = player.location
    print("\nWelcome to the shop!")
    print("Available products:")
    for product, details in city.get_products().items():
        print(f"{product}: {details['price']} gold (Stock: {details['qty']})")
    print("What would you like to do?")
    print("1. Buy Product")
    print("2. Sell Product")
    choice = input("Enter your choice: ")
    if choice == "1":
        product = input("Enter the product name: ")
        if product not in city.get_products():
            print('Invalid choice')
            return
        qty = int(input("Enter the quantity: "))
        city.sell_product(player, product, qty)
    elif choice == "2":
        print(f'You have {player.get_cargo()}')
        product = input("Enter the product name: ")
        qty = int(input("Enter the quantity: "))
        city.sell_product(player, product, qty)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main_n()
