from .response import InboundFax, OutboundFax, ForwardingEmail, Document, Image
from .files import File

__version__ = '0.1.0-dev'

from .client import InterFAX  # NOQA

__all__ = ('InterFAX', 'InboundFax', 'OutboundFax', 'ForwardingEmail',
           'Document', 'Image', 'File')
