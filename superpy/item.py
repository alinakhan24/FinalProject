class Item:
    def __init__(self, name, price, expiration_date, salePrice, id):
        self.name = name
        self.price = price
        self.expiration_date = expiration_date
        self.salePrice = salePrice
        self.id = id
    def __eq__(self, other):
        if isinstance(other, Item):
            return self.id == other.id
        return False
    def __hash__(self):
        return hash((self.id))