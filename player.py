class Player:
    def __init__(self, name):
        self.name = name
        self.location = ""
        self.currency = 10_000
        self.inventory = []
        self.cargo = {}

    def add_item(self, item):
        self.inventory.append(item)

    def remove_item(self, item):
        self.inventory.remove(item)

    def sell_cargo(self, product, price, qty):
        if product in self.cargo:
            if self.cargo[product]["qty"] < qty:
                self.cargo[product]["qty"] -= qty
            elif self.cargo[product]["qty"] == qty:
                del self.cargo[product]
            else:
                print(f"You only have {self.cargo[product]['qty']} of {product}.")
                return
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
