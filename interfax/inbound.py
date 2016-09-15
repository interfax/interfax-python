from .response import ForwardingEmail, Image, InboundFax


class Inbound(object):

    def __init__(self, client):
        self.client = client

    def all(self, **kwargs):
        """Retrieves a user's list of inbound faxes.

        (Sort order is always in descending ID).

        """
        valid_keys = ['unread_only', 'limit', 'last_id', 'all_users']

        faxes = self.client.get('/inbound/faxes', kwargs, valid_keys)

        return [InboundFax(self.client, fax) for fax in faxes]

    def find(self, message_id):
        """Retrieves a single fax's metadata (receive time, sender number,
        etc.)."""
        fax = self.client.get('/inbound/faxes/{0}'.format(message_id))

        return InboundFax(self.client, fax)

    def image(self, message_id):
        """Retrieves a single fax's image."""
        data = self.client.get('/inbound/faxes/{0}/image'.format(message_id))

        return Image(self.client, {'data': data})

    def emails(self, message_id):
        """Retrieve the list of email addresses to which a fax was
        forwarded."""
        emails = self.client.get('/inbound/faxes/{0}/emails'.format(
            message_id))

        return [ForwardingEmail(self.client, email) for email in emails]

    def mark(self, message_id, read=True):
        """Mark a transaction as read/unread."""
        valid_keys = ['unread']

        kwargs = {'unread': not read}

        self.client.post('/inbound/faxes/{0}/mark'.format(message_id),
                         kwargs, valid_keys)

    def resend(self, message_id, email=None):
        """Resend an inbound fax to a specific email address."""
        valid_keys = ['email']

        kwargs = {}

        if email:
            kwargs['email'] = email

        self.client.post('/inbound/faxes/{0}/resend'.format(message_id),
                         kwargs, valid_keys)
