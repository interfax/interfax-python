from interfax.inbound import Inbound

from interfax.response import InboundFax, ForwardingEmail, Image

try:
    from unittest.mock import Mock, patch, call
except ImportError:
    from mock import Mock, patch, call

class TestInbound(object):
    def setup_method(self, method):
        self.client = Mock()
        self.inbound = Inbound(self.client)

    def teardown_method(self, method):
        del self.client
        del self.inbound

    def test___init__(self):
        assert self.inbound.client == self.client

    def test_all(self, fake, message_id):
        self.client.get.return_value = [{'messageId': message_id}]

        valid_keys = ['unread_only', 'limit', 'last_id', 'all_users']

        kwargs = fake.pydict()

        result = self.inbound.all(**kwargs)

        self.client.get.assert_called_with('/inbound/faxes', kwargs, valid_keys)

        assert isinstance(result[0], InboundFax)
        assert result[0].id == message_id
        assert result[0].client == self.client

    def test_find(self, message_id):
        self.client.get.return_value = {'messageId': message_id}

        result = self.inbound.find(message_id)

        self.client.get.assert_called_with(
            '/inbound/faxes/{0}'.format(message_id))

        assert isinstance(result, InboundFax)
        assert result.id == message_id
        assert result.client == self.client

    def test_image(self, fake, message_id):
        self.client.get.return_value = return_value = fake.binary()

        result = self.inbound.image(message_id)

        self.client.get.assert_called_with(
            '/inbound/faxes/{0}/image'.format(message_id))

        assert isinstance(result, Image)
        assert result.data == return_value
        assert result.client == self.client

    def test_emails(self, fake, message_id):
        self.client.get.return_value = return_value = [{'email': fake.email()}]

        result = self.inbound.emails(message_id)

        self.client.get.assert_called_with(
            '/inbound/faxes/{0}/emails'.format(message_id))

        assert isinstance(result[0], ForwardingEmail)
        assert result[0].email == return_value[0]['email']
        assert result[0].client == self.client

    def test_mark(self, fake, message_id):
        read = fake.boolean()

        result = self.inbound.mark(message_id, read)

        valid_keys = ['unread']

        kwargs = {'unread': not read}

        self.client.post.assert_called_with(
            '/inbound/faxes/{0}/mark'.format(message_id), kwargs, valid_keys)

    def test_resend(self, fake, message_id):
        email = fake.email() if fake.boolean() else None

        result = self.inbound.resend(message_id, email)

        valid_keys = ['email']

        kwargs = {}
        
        if email:
            kwargs['email'] = email

        self.client.post.assert_called_with(
            '/inbound/faxes/{0}/resend'.format(message_id), kwargs, valid_keys)
