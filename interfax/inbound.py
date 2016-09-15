from inflection import underscore

from .response import InboundFax, Image, ForwardingEmail


class Inbound(object):

    def __init__(self, client):
        self.client = client

    def all(self, **kwargs):
        valid_keys = ['unread_only', 'limit', 'last_id', 'all_users']

        faxes = self.client.get('/inbound/faxes', kwargs, valid_keys)

        return [InboundFax(self.client, fax) for fax in faxes]

    def find(self, message_id):
        fax = self.client.get('/inbound/faxes/{0}'.format(message_id))

        return InboundFax(self.client, fax)

    def image(self, message_id):
        data = self.client.get('/inbound/faxes/{0}/image'.format(message_id))

        return Image(self.client, {'data': data})

    def emails(self, message_id):
        emails = self.client.get('/inbound/faxes/{0}/emails'.format(message_id))

        return [ForwardingEmail(self.client, email) for email in emails]

    def mark(self, message_id, read=True):
        valid_keys = ['unread']

        kwargs = {'unread': not read}

        self.client.post('/inbound/faxes/{0}/mark'.format(message_id), 
                         kwargs, valid_keys)

    def resend(self, message_id, email=None):
        valid_keys = ['email']

        kwargs = {}

        if email:
            kwargs['email'] = email

        self.client.post('/inbound/faxes/{0}/resend'.format(message_id), kwargs, 
                    valid_keys)
