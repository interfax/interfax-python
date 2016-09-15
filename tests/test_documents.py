from interfax.documents import Documents
from interfax.response import Document

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock


class TestDocuments(object):

    def setup_method(self, method):
        self.client = Mock()
        self.documents = Documents(self.client)

    def teardown_method(self, method):
        del self.client
        del self.documents

    def test___init__(self):
        assert self.documents.client == self.client

    def test_all(self, fake):
        self.client.get.return_value = return_value = [
            {'uri': 'https://rest.interfax.net/outbound/documents/{0}'.format(
                fake.random_number())}
        ]

        valid_keys = ['limit', 'offset']

        kwargs = fake.pydict()

        result = self.documents.all(**kwargs)

        self.client.get.assert_called_with('/outbound/documents', kwargs,
                                           valid_keys)

        assert isinstance(result[0], Document)
        assert result[0].uri == return_value[0]['uri']
        assert result[0].client == self.client

    def test_find(self, fake):
        document_id = str(fake.random_number())

        self.client.get.return_value = return_value = {
            'uri': 'https://rest.interfax.net/outbound/documents/{0}'.format(
                document_id)
        }

        result = self.documents.find(document_id)

        self.client.get.assert_called_with(
            '/outbound/documents/{0}'.format(document_id))

        assert isinstance(result, Document)
        assert result.uri == return_value['uri']
        assert result.client == self.client

    def test_cancel(self, fake):
        document_id = str(fake.random_number())

        self.documents.cancel(document_id)

        self.client.delete.assert_called_with(
            '/outbound/documents/{0}'.format(document_id))

    def test_create(self, fake):
        document_id = str(fake.random_number())
        return_value = (
            'https://rest.interfax.net/outbound/documents/{0}'
        ).format(document_id)

        name = fake.file_name()
        size = fake.random_number()

        self.client.post.return_value = return_value

        valid_keys = ['name', 'size', 'disposition', 'shared']

        kwargs = fake.pydict()

        result = self.documents.create(name, size, **kwargs)

        kwargs['name'] = name
        kwargs['size'] = size

        self.client.post.assert_called_with('/outbound/documents', kwargs,
                                            valid_keys)

        assert isinstance(result, Document)
        assert result.uri == return_value
        assert result.client == self.client

    def test_upload(self, fake):
        document_id = str(fake.random_number())

        chunk = fake.pystr()
        start = fake.random_number()
        end = fake.random_number()

        self.documents.upload(document_id, start, end, chunk)

        headers = {'Range': 'bytes={0}-{1}'.format(start, end)}

        self.client.post.assert_called_with(
            '/outbound/documents/{0}'.format(document_id), headers=headers,
            data=chunk)
