from inflection import camelize
from pytest import raises

from interfax.client import InterFAX

try:
    from urllib.parse import urlunsplit, urlencode
except ImportError:
    from urllib import urlencode
    from urlparse import urlunsplit

try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch


class TestInterFAX(object):

    def setup_method(self, method):
        self.client = InterFAX('username', 'password')

    def teardown_method(self, method):
        del self.client

    def test___init__(self, fake):
        username = fake.pystr()
        password = fake.pystr()
        timeout = fake.pyfloat()

        client = InterFAX(username, password, timeout)

        assert client.username == username
        assert client.password == password
        assert client.timeout == timeout

        client = InterFAX(username, password)

        assert client.username == username
        assert client.password == password
        assert client.timeout is None

    def test__init__environ(self, fake):
        username = fake.pystr()
        password = fake.pystr()

        environ = {
            'INTERFAX_USERNAME': username,
            'INTERFAX_PASSWORD': password
        }

        with patch.dict('os.environ', environ):
            client = InterFAX()

        assert client.username == username
        assert client.password == password

    def test___init__errors(self, fake):
        username = fake.pystr()
        password = fake.pystr()

        with raises(TypeError):
            InterFAX(username=username)

        with raises(TypeError):
            InterFAX(password=password)

    def test_inbound(self):
        assert self.client.inbound.client == self.client

    def test_outbound(self):
        assert self.client.outbound.client == self.client

    def test_account(self):
        assert self.client.account.client == self.client

    def test_documents(self):
        assert self.client.documents.client == self.client

    def test_files(self):
        assert self.client.files.client == self.client

    def test_deliver(self, fax_number, fake):
        self.client.outbound = Mock()

        files = fake.pytuple(10, True, str)

        kwargs = fake.pydict()

        result = self.client.deliver(fax_number, files, **kwargs)

        self.client.outbound.deliver.assert_called_with(fax_number, files,
                                                        **kwargs)

        assert result == self.client.outbound.deliver.return_value

    def test_get(self, fake):
        path = fake.pystr()
        params = fake.pydict()
        valid_keys = fake.pytuple(10, True, str)

        self.client._request = Mock()
        self.client._url_for = Mock()

        kwargs = fake.pydict()

        result = self.client.get(path, params, valid_keys, **kwargs)

        self.client._url_for.assert_called_with(path, params, valid_keys)

        url = self.client._url_for.return_value

        self.client._request.assert_called_with('GET', url, **kwargs)

        assert result == self.client._request.return_value

    def test_post(self, fake):
        path = fake.pystr()
        params = fake.pydict()
        valid_keys = fake.pytuple(10, True, str)
        kwargs = fake.pydict()

        self.client._request = Mock()
        self.client._url_for = Mock()

        result = self.client.post(path, params, valid_keys, **kwargs)

        self.client._url_for.assert_called_with(path, params, valid_keys)

        url = self.client._url_for.return_value

        self.client._request.assert_called_with('POST', url, **kwargs)

        assert result == self.client._request.return_value

    def test_delete(self, fake):
        path = fake.pystr()
        kwargs = fake.pydict()

        self.client._request = Mock()
        self.client._url_for = Mock()

        result = self.client.delete(path, **kwargs)

        self.client._url_for.assert_called_with(path)

        url = self.client._url_for.return_value

        self.client._request.assert_called_with('DELETE', url, **kwargs)

        assert result == self.client._request.return_value

    def test__request(self, fake):
        url = fake.uri()
        method = fake.pystr()
        kwargs = fake.pydict()

        self.client._parse_response = Mock()
        self.client.timeout = fake.pyfloat()

        with patch('interfax.client.request') as request:
            self.client._request(method, url, **kwargs)

        kwargs.setdefault('headers', {})
        kwargs.setdefault('timeout', self.client.timeout)
        kwargs['headers']['User-Agent'] = self.client.USER_AGENT
        kwargs['auth'] = (self.client.username, self.client.password)

        request.assert_called_with(method, url, **kwargs)
        self.client._parse_response.assert_called_with(request.return_value)

    def test__url_for(self, fake, params):
        path = fake.pystr()
        keys = list(params.keys())

        result = self.client._url_for(path, params, keys)

        camel = dict([(camelize(k, False), v) for k, v in params.items()])

        assert result == urlunsplit(('https', self.client.DOMAIN, path,
                                     urlencode(camel), None))

        keys.pop()
        with raises(TypeError):
            self.client._url_for(path, params, keys)

    def test__parse_response(self, fake):
        url = fake.uri()

        parse = self.client._parse_response

        # json

        response = Mock()
        response.ok = True
        response.headers = {}

        assert parse(response) == response.json.return_value

        # redirect

        response = Mock()
        response.ok = True
        response.headers = {'location':  url}

        assert parse(response) == url

        # binary

        response = Mock()
        response.ok = True
        response.headers = {}
        response.json.side_effect = Exception

        assert parse(response) == response.content

        # error

        response = Mock()
        response.ok = False

        parse(response)

        response.raise_for_status.assert_called_with()

    def test_user_agent(self):
        assert self.client.USER_AGENT.startswith('InterFAX Python ')
