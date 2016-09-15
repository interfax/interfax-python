from mimetypes import guess_extension
from uuid import UUID

from interfax.files import File, Files
from interfax.response import Document

try:
    from unittest.mock import Mock, patch, call
except ImportError:
    from mock import Mock, patch, call


class TestFiles(object):

    def setup_method(self, method):
        self.client = Mock()
        self.files = Files(self.client)

    def teardown_method(self, method):
        del self.client
        del self.files

    def test___init__(self):
        assert self.files.client == self.client

    def test_create(self, fake):
        data = fake.pystr()
        kwargs = fake.pydict()

        with patch('interfax.files.File') as f:
            self.files.create(data, **kwargs)

        f.assert_called_with(self.client, data, **kwargs)


class TestFile(object):

    def setup_method(self, method):
        self.client = Mock()

    def teardown_method(self, method):
        del self.client

    def test_with_binary(self, fake):
        data = fake.binary(512 * 1024)

        mime_type = fake.mime_type()

        f = File(self.client, data, mime_type=mime_type)

        assert 'Content-Location' not in f.headers
        assert f.mime_type == mime_type
        assert f.body == data
        assert f.file_tuple() == (None, data, mime_type, None)

    def test_with_uri(self, fake):
        data = fake.uri()

        f = File(self.client, data)

        assert f.headers == {'Content-Location': data}
        assert f.mime_type is None
        assert f.body is None
        assert f.file_tuple() == (None, '', None, {'Content-Location': data})

    def test_with_path(self, fake):
        data = './tests/test.pdf'

        f = File(self.client, data)

        with open(data, 'rb') as fp:
            content = fp.read()

        assert 'Content-Location' not in f.headers
        assert f.mime_type == 'application/pdf'
        assert f.body == content
        assert f.file_tuple() == (None, content, 'application/pdf', None)

    def test_with_large_file(self, fake):
        data = fake.binary()
        mime_type = fake.mime_type()
        chunk_size = fake.random_int(len(data) // 20, len(data) // 2)

        document = Document(self.client, {
            'uri': 'https://rest.interfax.net/outbound/documents/{0}'.format(
                fake.random_number())
        })

        self.client.documents.create.return_value = document

        with patch('interfax.files.uuid4') as m:
            m.return_value = UUID('8fbaaaaf-87bb-4bd0-9d82-823c3eb38e49')
            f = File(self.client, data, mime_type=mime_type,
                     chunk_size=chunk_size)

        assert f.headers == {'Content-Location': document.uri}
        assert f.mime_type is None
        assert f.body is None
        assert f.file_tuple() == (None, '', None, {
            'Content-Location': document.uri
        })

        filename = 'upload-8fbaaaaf-87bb-4bd0-9d82-823c3eb38e49{0}'.format(
            guess_extension(mime_type)
        )

        calls = [call.create(filename, len(data))]

        cursor = 0

        while cursor < len(data):
            chunk = data[cursor:cursor + chunk_size]

            calls.append(call.upload(document.id, cursor,
                                     cursor + len(chunk) - 1, chunk))
            cursor += len(chunk)

        self.client.documents.assert_has_calls(calls)
