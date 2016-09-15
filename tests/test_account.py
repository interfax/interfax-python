from interfax.account import Account

from decimal import Decimal

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock


class TestAccount(object):
    def setup_method(self, method):
        self.client = Mock()
        self.account = Account(self.client)

    def teardown_method(self, method):
        del self.client
        del self.account

    def test___init__(self):
        assert self.account.client == self.client

    def test_balance(self, fake):
        balance = fake.pydecimal(3, 2, True)
        
        self.client.get.return_value = str(balance)

        assert self.account.balance() == balance

        self.client.get.assert_called_with('/accounts/self/ppcards/balance')


