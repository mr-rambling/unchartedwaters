# How can I treat a player as a sprite?
# Need to look at this

class Player:
    def __init__(self, name):
        self.name = name
        self.location = ""
        self.currency = 10_000
        self.health = 87
        self.energy = 92
        self.max_health = 100
        self.max_energy = 100
        self.inventory = {
            'Starting Dagger': {'value':100, 'dmg': 5, 'qty': 1}
            }
        self.cargo = {
            'Beans': {'value': 5, 'qty': 100},
            'Fish': {'value': 7, 'qty': 17},
            'Gunpowder': {'value': 80, 'qty': 23}
        }

    def add_item(self, item):
        self.inventory.append(item)

    def remove_item(self, item):
        self.inventory.remove(item)

    def sell_cargo(self, product, price, qty):
        if product in self.cargo:
            if qty < self.cargo[product]["qty"]:
                self.cargo[product]["qty"] -= qty
            elif self.cargo[product]["qty"] == qty or qty > self.cargo[product]["qty"]:
                qty = self.cargo[product]["qty"]
                del self.cargo[product]
        self.currency += price * qty
        print(f"{self.name} sold {qty} of {product} for a total of {price * qty}.")

    def buy_cargo(self, product, price, qty):
        '''
        Returns number of product purchased
        '''
        if self.currency < price * qty:
            print(f"{self.name} does not have enough currency to buy {qty} of {product}.")
            return 0
        if product in self.cargo:
            self.cargo[product]["qty"] += qty
        else:
            self.cargo[product] = {"qty": qty}
        self.currency -= price * qty
        print(f"{self.name} bought {qty} of {product} for a total of {price * qty}.")
        return qty

    def get_inventory(self):
        return self.inventory

    def get_cargo(self):
        return self.cargo
