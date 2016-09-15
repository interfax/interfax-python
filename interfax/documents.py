from .response import Document


class Documents(object):

    def __init__(self, client):
        self.client = client

    def all(self, **kwargs):
        """Get a list of previous document uploads which are currently
        available."""
        valid_keys = ['limit', 'offset']

        documents = self.client.get('/outbound/documents', kwargs, valid_keys)

        return [Document(self.client, document) for document in documents]

    def find(self, document_id):
        """Get the current status of a specific document upload."""
        document = self.client.get(
            '/outbound/documents/{0}'.format(document_id))

        return Document(self.client, document)

    def create(self, name, size, **kwargs):
        """Create a document upload session, allowing you to upload large files
        in chunks."""
        kwargs['name'] = name
        kwargs['size'] = size

        valid_keys = ['name', 'size', 'disposition', 'shared']

        uri = self.client.post('/outbound/documents', kwargs, valid_keys)

        return Document(self.client, {'uri': uri})

    def upload(self, document_id, range_start, range_end, chunk):
        """Upload a chunk to an existing document upload session."""
        headers = {'Range': 'bytes={0}-{1}'.format(range_start, range_end)}

        self.client.post('/outbound/documents/{0}'.format(document_id),
                         headers=headers, data=chunk)

    def cancel(self, document_id):
        """Cancel a document upload and tear down the upload session, or delete
        a previous upload."""
        self.client.delete('/outbound/documents/{0}'.format(document_id))
