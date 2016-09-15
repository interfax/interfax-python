from os import environ

from cached_property import cached_property
from inflection import camelize
from requests import request

from . import __version__
from .account import Account
from .documents import Documents
from .files import Files
from .inbound import Inbound
from .outbound import Outbound

try:
    from urllib.parse import urlunsplit, urlencode
except ImportError:
    from urllib import urlencode
    from urlparse import urlunsplit


class InterFAX(object):
    """The client follows the 12-factor apps principle and can be either setup
    directly or via environment variables."""

    USER_AGENT = 'InterFAX Python {0}'.format(__version__)
    DOMAIN = 'rest.interfax.net'

    def __init__(self, username=None, password=None):
        username = username or environ.get('INTERFAX_USERNAME', None)
        password = password or environ.get('INTERFAX_PASSWORD', None)

        cls = self.__class__.__name__

        if not username:
            raise TypeError('{0} expects argument username'.format(cls))

        if not password:
            raise TypeError('{0} expects argument password'.format(cls))

        self.username = username
        self.password = password

    @cached_property
    def inbound(self):
        return Inbound(self)

    @cached_property
    def outbound(self):
        return Outbound(self)

    @cached_property
    def files(self):
        return Files(self)

    @cached_property
    def documents(self):
        return Documents(self)

    @cached_property
    def account(self):
        return Account(self)

    @cached_property
    def deliver(self):
        return self.outbound.deliver

    def get(self, path, params={}, valid_keys=[], **kwargs):
        """Make a HTTP GET request."""

        url = self._url_for(path, params, valid_keys)
        return self._request('GET', url, **kwargs)

    def post(self, path, params={}, valid_keys=[], **kwargs):
        """Make a HTTP POST request."""
        url = self._url_for(path, params, valid_keys)
        return self._request('POST', url, **kwargs)

    def delete(self, path, **kwargs):
        """Make a HTTP DELETE request."""
        url = self._url_for(path)
        return self._request('DELETE', url, **kwargs)

    def _request(self, method, url, **kwargs):
        """Make a HTTP request."""
        kwargs.setdefault('headers', {})
        kwargs['headers']['User-Agent'] = self.USER_AGENT
        kwargs['auth'] = (self.username, self.password)

        return self._parse_response(request(method, url, **kwargs))

    def _url_for(self, path, params={}, keys=[]):
        """Validate query params and return fully qualified url."""
        invalid = [k for k in params if k not in keys]

        message = 'unexpected keyword argument "{0}", expecting: {1}'

        if len(invalid):
            raise TypeError(message.format(invalid[0], ', '.join(keys)))

        params = dict([(camelize(k, False), v) for k, v in params.items()])

        return urlunsplit(('https', self.DOMAIN, path, urlencode(params),
                           None))

    def _parse_response(self, response):
        """Parse a response object and return the url, json, or binary
        content."""
        if response.ok:
            if 'location' in response.headers:
                return response.headers['location']
            else:
                try:
                    return response.json()
                except:
                    return response.content
        else:
            response.raise_for_status()
