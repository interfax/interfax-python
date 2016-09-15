from .files import File
from .response import Image, OutboundFax


class Outbound(object):

    def __init__(self, client):
        self.client = client

    def deliver(self, fax_number, files, **kwargs):
        """Submit a fax to a single destination number."""
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
        """Get a list of recent outbound faxes (which does not include batch
        faxes)."""
        valid_keys = ['limit', 'last_id', 'sort_order', 'user_id']

        faxes = self.client.get('/outbound/faxes', kwargs, valid_keys)

        return [OutboundFax(self.client, fax) for fax in faxes]

    def completed(self, *args):
        """Get details for a subset of completed faxes from a submitted list.

        (Submitted id's which have not completed are ignored).

        """
        valid_keys = ['ids']

        kwargs = {'ids': args}

        faxes = self.client.get('/outbound/faxes/completed', kwargs,
                                valid_keys)

        return [OutboundFax(self.client, fax) for fax in faxes]

    def find(self, message_id):
        """Retrieves information regarding a previously-submitted fax,
        including its current status."""
        fax = self.client.get('/outbound/faxes/{0}'.format(message_id))

        return OutboundFax(self.client, fax)

    def image(self, message_id):
        """Retrieve the fax image (TIFF file) of a submitted fax."""
        data = self.client.get('/outbound/faxes/{0}/image'.format(message_id))

        return Image(self.client, {'data': data})

    def cancel(self, message_id):
        """Cancel a fax in progress."""
        self.client.post('/outbound/faxes/{0}/cancel'.format(message_id))

    def search(self, **kwargs):
        """Search for outbound faxes."""
        valid_keys = ['ids', 'reference', 'date_from', 'date_to', 'status',
                      'user_id', 'fax_number', 'limit', 'offset']

        faxes = self.client.get('/outbound/search', kwargs, valid_keys)

        return [OutboundFax(self.client, fax) for fax in faxes]
