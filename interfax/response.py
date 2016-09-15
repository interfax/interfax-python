from inflection import underscore


class Response(object):

    def __init__(self, client, data):
        self.__dict__.update([(underscore(k), v) for k, v in data.items()])
        self.client = client

    def __repr__(self):
        return '{0}(id={1})'.format(self.__class__.__name__, repr(self.id))


class InboundFax(Response):

    @property
    def id(self):
        """Return the fax's id."""
        return self.message_id

    def image(self):
        """Retrieves the fax's image."""
        return self.client.inbound.image(self.id)

    def reload(self):
        """Retrieves the fax's metadata (receive time, sender number, etc.)."""
        return self.client.inbound.find(self.id)

    def mark(self, read=True):
        """Mark the fax as read/unread."""
        return self.client.inbound.mark(self.id, read)

    def resend(self, email=None):
        """Resend the fax to a specific email address."""
        return self.client.inbound.resend(self.id, email)

    def emails(self):
        """Retrieve the list of email addresses to which the fax was
        forwarded."""
        return self.client.inbound.emails(self.id)


class OutboundFax(Response):

    def image(self):
        """Retrieve the fax image (TIFF file) of the fax."""
        return self.client.outbound.image(self.id)

    def reload(self):
        """Retrieve information regarding the fax, including its current
        status."""
        return self.client.outbound.find(self.id)

    def cancel(self):
        """Cancel the fax in progress."""
        return self.client.outbound.cancel(self.id)


class ForwardingEmail(Response):

    def __repr__(self):
        return '{0}(email_address={1})'.format(self.__class__.__name__,
                                               repr(self.email_address))


class Document(Response):

    @property
    def id(self):
        """Return the documents id."""
        return self.uri.split('/')[-1]

    def upload(self, range_start, range_end, chunk):
        """Upload a chunk to the document upload session."""
        return self.client.documents.upload(self.id, range_start, range_end,
                                            chunk)

    def cancel(self):
        """Cancel the document upload and tear down the upload session, or
        delete a previous upload."""
        return self.client.documents.cancel(self.id)

    def reload(self):
        """Get the current status of the document upload."""
        return self.client.documents.find(self.id)

    def __repr__(self):
        return '{0}(uri={1})'.format(self.__class__.__name__,
                                     repr(self.uri))


class Image(Response):

    def save(self, filename):
        """Write the image data to file."""
        with open(filename, 'wb') as f:
            f.write(self.data)

    def __repr__(self):
        return '{0}()'.format(self.__class__.__name__)
