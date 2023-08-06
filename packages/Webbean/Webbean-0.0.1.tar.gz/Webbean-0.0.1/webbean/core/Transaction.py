from datetime import timedelta


DELTA_DAY = 3


class Transaction:

    def __init__(self, date=None, amount=None, account=None, label=None):
        self.date = date
        self.amount = amount
        self.account = account
        self.label = label

    def __str__(self):
        return "{}: {}".format(self.date, self.amount)

    def __eq__(self, other):
        delta = self.date - other.date
        return abs(delta) < timedelta(days=DELTA_DAY) and self.amount == other.amount
