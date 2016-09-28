from .response import InboundFax, OutboundFax, ForwardingEmail, Document, Image
from .files import File

__version__ = '1.0.0'

from .client import InterFAX  # NOQA

__all__ = ('InterFAX', 'InboundFax', 'OutboundFax', 'ForwardingEmail',
           'Document', 'Image', 'File')
