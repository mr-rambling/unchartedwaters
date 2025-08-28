from cities import Cities, City
from player import Player

class World:
    def __init__(self):
        self.cities = Cities()
        self.cities.add_city(City("Viremontis", 
                        (0, 0),
                        0, 
                        120000, 
                        ["The Great Library", "Viremontis Castle", "The Crystal Lake"])
                    )
        self.cities.add_city(City("Serathorne", 
                            (0, 98),
                            1, 
                            95000, 
                            ["The Serpent's Fountain", "Serathorne Cathedral", "The Whispering Woods"])
                        )
        self.cities.add_city(City("Draymoor", 
                            (-32, 50),
                            2, 
                            80000, 
                            ["The Draymoor Keep", "The Misty Marshes", "The Ancient Oak"])
                        )
        self.cities.add_city(City("Caldrith Vale", 
                            (-16, 75),
                            3, 
                            72000, 
                            ["The Caldrith Falls", "The Enchanted Glade", "The Ancient Ruins"])
                        )
        self.cities.add_city(City("Nex Hollow", 
                            (-86, 42),
                            4, 
                            65000, 
                            ["The Shadowed Glade", "Nex Hollow Caverns", "The Whispering Falls"])
                        )

        self.cities.get_city("Viremontis").add_product("Magical Tomes", 10, 1.2)

def main():
    world = World()
    print("Hello from unchartedwaters!")
    player = Player("Hero")
    player.location = world.cities.get_city("Viremontis")
    print(f"Welcome {player.name}! You have {player.currency} gold.")
    print(f"You are currently in {player.location.name}.")

    while True:
        print("What would you like to do?")
        print("1. Visit Shop")
        print("2. Check Inventory")
        print("3. Manage Cargo")
        print("4. Leave City")
        choice = input("Enter your choice: ")
        if choice == "1":
            shop(player.location)
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

def shop(city):
    print("Welcome to the shop!")
    print("Available products:")
    for product, details in city.get_products().items():
        print(f"{product}: {details['price']} gold (Stock: {details['stock']})")
    print("What would you like to do?")
    print("1. Buy Product")
    print("2. Sell Product")
    choice = input("Enter your choice: ")
    if choice == "1":
        product = input("Enter the product name: ")
        qty = int(input("Enter the quantity: "))
        city.buy_product(product, qty)
    elif choice == "2":
        product = input("Enter the product name: ")
        qty = int(input("Enter the quantity: "))
        city.sell_product(product, qty)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
