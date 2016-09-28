import py
import pytest
from faker import Factory
from inflection import underscore
from pyfakefs.fake_filesystem_unittest import Patcher
from pytest import fixture

from interfax.response import Document, Image, InboundFax, OutboundFax

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock


Patcher.SKIPMODULES.add(py)
Patcher.SKIPMODULES.add(pytest)


@fixture
def fs(request):
    patcher = Patcher()
    patcher.setUp()
    request.addfinalizer(patcher.tearDown)
    return patcher.fs


@fixture(scope='session')
def fake():
    return Factory.create()


@fixture
def fake_dict(fake):
    count = 0

    while count == 0:
        count = fake.random_number(digits=2)

    return dict([(fake.pystr(), fake.pystr()) for k in range(count)])


@fixture
def params(fake_dict):
    return dict([(underscore(k), v) for k, v in fake_dict.items()])


@fixture
def inbound_fax(fake):
    return InboundFax(Mock(), {'messageId': fake.random_number()})


@fixture
def outbound_fax(fake):
    return OutboundFax(Mock(), {'id': fake.random_number()})


@fixture
def document(fake):
    document_id = fake.random_number()

    return Document(Mock(), {
        'uri': 'https://example.com/{0}'.format(document_id)
    })


@fixture
def image(fake):
    return Image(Mock(), {'data': fake.binary()})


@fixture
def message_id(fake):
    return fake.random_number()


@fixture
def fax_number(fake):
    return '+{0}'.format(fake.random_int(10**11, 10**12 - 1))
