from inflection import underscore

from decimal import Decimal

class Account(object):

    def __init__(self, client):
        self.client = client

    def balance(self, **kwargs):
        return Decimal(self.client.get('/accounts/self/ppcards/balance'))
