from mimetypes import guess_extension
from uuid import uuid4

from magic import from_buffer


class Files(object):

    def __init__(self, client):
        self.client = client

    def create(self, data, **kwargs):
        """Create a file object bound to the client."""
        return File(self.client, data, **kwargs)


class File(object):
    """Normalise urls, files, and binary data into one object.

    if mime_type is provided the data is assumed to be binary data, otherwise
    it is assumed to be a path or URL.

    if the binary data or file size exceeds the size of chunk_size it will be
    pre uploaded using the documents api.

    """

    def __init__(self, client, data, mime_type=None, chunk_size=None):
        self.client = client
        self.chunk_size = chunk_size or (1024 * 1024)
        self.headers = {}
        self.body = None
        self.mime_type = None

        if mime_type:
            self._init_binary(data, mime_type)
        elif data.startswith('http://') or data.startswith('https://'):
            self._init_url(data)
        else:
            self._init_path(data)

    def _init_url(self, data):
        """Initialise with a URL."""
        self.headers['Content-Location'] = data

    def _init_path(self, data):
        """Initialise with a file path."""
        with open(data, 'rb') as f:
            data = f.read()

        mime_type = from_buffer(data[0:1024], True)

        self._init_binary(data, mime_type)

    def _init_binary(self, data, mime_type):
        """Initialise with binary data."""
        if len(data) > self.chunk_size:
            return self._init_document(data, mime_type)

        self.mime_type = mime_type
        self.body = data

    def _init_document(self, data, mime_type):
        """Upload the data using the documents API."""
        filename = 'upload-{0}{1}'.format(uuid4(), guess_extension(mime_type))
        document = self.client.documents.create(filename, len(data))

        cursor = 0

        while cursor < len(data):
            chunk = data[cursor:cursor + self.chunk_size]

            document.upload(cursor, cursor + len(chunk) - 1, chunk)
            cursor += len(chunk)

        self._init_url(document.uri)

    def file_tuple(self):
        """Generate a file tuple for requests to upload."""
        return (None, self.body or '', self.mime_type, self.headers or None)
