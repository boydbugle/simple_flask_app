class ShoppingCart(object):

    def __init__(self):
        self.total = 0
        self.items = {}

    def add_item(self, item_name, quantity, price):
        self.total += price*quantity
        self.items.update({item_name: quantity})

    def remove_item(self, item_name, quantity, price):
        if item_name in self.items:
            if quantity < self.items[item_name] and quantity > 0:
                self.items[item_name] -= quantity
                self.total -= price*quantity
            elif quantity >= self.items[item_name]:
                self.total -= price*self.items[item_name]
                del self.items[item_name]

    def checkout(self, cash_paid):
        if cash_paid >= self.total:
            return cash_paid - self.total
        return "Cash paid not enough"


class Shop(ShoppingCart):

    def __init__(self):
        self.quantity = 100

    def remove_item(self):
        self.quantity -= 1


class ShoppingCart(object):

    def __init__(self):
        self.total = 0
        self.items = {}

    def add_item(self, item_name, quantity, price):
        self.total += quantity*price
        self.items.update({item_name: quantity})

    def remove_item(self, item_name, quantity, price):
        if item_name in self.items:
            if quantity >= self.items[item_name]:
                del self.items[item_name]
            else:
                self.items[item_name] -= quantity
                self.total -= quantity*price

    def checkout(self, cash_paid):
        if self.total > cash_paid:
            return "Cash paid not enough"
        else:
            return cash_paid - self.total


class Shop(ShoppingCart):

    def __init__(self):
        self.quantity = 100

    def remove_item(self):
        self.quantity -= 1


def is_isogram(word):
    if word == " ":
        return (word, False)
    elif type(word) == str:
        for i in word:
            if word.count(i) > 1:
                return (word, False)
            else:
                return (word, True)
    else:
        raise TypeError("'{}' should be a string" .format(word))


def get_middle(s):
    if len(s) % 2 != 0 or s == 1:
        index = len(s)/2
        print s[index]
    else:
        index = len(s)/2
        index1 = index - 1
        return s[index1] + s[index]

    [[x, l.count(x)] for x in set(l)]


def find_it(seq):
    i = 0
    array_set = [[x, seq.count(x)] for x in set(seq)]
    while i < len(array_set):
        times = array_set[i][1]
        if times % 2 == 0:
            pass
        else:
            return array_set[i][0]
        i += 1
