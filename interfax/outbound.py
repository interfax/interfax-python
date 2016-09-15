from cached_property import cached_property

from .response import OutboundFax, Image

from .files import File

class Outbound(object):

    def __init__(self, client):
        self.client = client

    def deliver(self, fax_number, files, **kwargs):
        valid_keys = ['fax_number', 'contact', 'postpone_time', 
                      'retries_to_perform', 'csid', 'page_header', 'reference', 
                      'reply_address', 'page_size', 'fit_to_page', 
                      'page_orientation', 'resolution', 'rendering']

        kwargs['fax_number'] = fax_number

        result = self.client.post('/outbound/faxes', kwargs, valid_keys, 
                                  files=self._generate_files(files))

        return OutboundFax(self.client, {'id': result.split('/')[-1]})

    def _generate_files(self, files):
        results = []

        for f in files:
            if not hasattr(f, 'file_tuple'):
                f = File(self.client, f)

            results.append((None, f.file_tuple()))

        return results

    def all(self, **kwargs):
        valid_keys = ['limit', 'last_id', 'sort_order', 'user_id']

        faxes = self.client.get('/outbound/faxes', kwargs, valid_keys)

        return [OutboundFax(self.client, fax) for fax in faxes]

    def completed(self, *args):
        valid_keys = ['ids']

        kwargs = {'ids': args}

        faxes = self.client.get('/outbound/faxes/completed', kwargs, valid_keys)

        return [OutboundFax(self.client, fax) for fax in faxes]

    def find(self, message_id):
        fax = self.client.get('/outbound/faxes/{0}'.format(message_id))

        return OutboundFax(self.client, fax)

    def image(self, message_id):
        data = self.client.get('/outbound/faxes/{0}/image'.format(message_id))

        return Image(self.client, {'data': data})

    def cancel(self, message_id):
        self.client.post('/outbound/faxes/{0}/cancel'.format(message_id))

    def search(self, **kwargs):
        valid_keys = ['ids', 'reference', 'date_from', 'date_to', 'status',
                      'user_id', 'fax_number', 'limit', 'offset']

        faxes = self.client.get('/outbound/search', kwargs, valid_keys)

        return [OutboundFax(self.client, fax) for fax in faxes]
