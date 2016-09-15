from os import environ

try:
    from urllib.parse import urlunsplit, urlencode
except ImportError:
    from urllib import urlencode
    from urlparse import urlunsplit

from requests import request

from inflection import camelize

from cached_property import cached_property

from . import __version__

from .inbound import Inbound
from .outbound import Outbound
from .documents import Documents
from .files import Files
from .account import Account

class InterFAX(object):

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

    def deliver(self, fax_number, files, **kwargs):
        return self.outbound.deliver(fax_number, files, **kwargs)

    def get(self, path, params={}, valid_keys=[], **kwargs):
        url = self._url_for(path, params, valid_keys)
        return self._request('GET', url, **kwargs)

    def post(self, path, params={}, valid_keys=[], **kwargs):
        url = self._url_for(path, params, valid_keys)
        return self._request('POST', url, **kwargs)

    def delete(self, path, **kwargs):
        url = self._url_for(path)
        return self._request('DELETE', url, **kwargs)

    def _request(self, method, url, **kwargs):
        kwargs.setdefault('headers', {})
        kwargs['headers']['User-Agent'] = self.USER_AGENT
        kwargs['auth'] = (self.username, self.password)

        return self._parse_response(request(method, url, **kwargs))

    def _url_for(self, path, params={}, keys=[]):
        invalid = [k for k in params if k not in keys]

        message = 'unexpected keyword argument "{0}", expecting: {1}'

        if len(invalid):
            raise TypeError(message.format(invalid[0], ', '.join(keys)))

        params = dict([(camelize(k, False), v) for k,v in params.items()])

        return urlunsplit(('https', self.DOMAIN, path, urlencode(params), None))

    def _parse_response(self, response):
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
