from decimal import Decimal


class Account(object):

    def __init__(self, client):
        self.client = client

    def balance(self):
        """Determine the remaining faxing credits in your account."""

        return Decimal(self.client.get('/accounts/self/ppcards/balance'))
