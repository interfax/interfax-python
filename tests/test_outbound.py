from interfax.outbound import Outbound

from interfax.response import OutboundFax, Image

from interfax.files import File

try:
    from unittest.mock import Mock, patch, call
except ImportError:
    from mock import Mock, patch, call

class TestOutbound(object):
    def setup_method(self, method):
        self.client = Mock()
        self.outbound = Outbound(self.client)

    def teardown_method(self, method):
        del self.client
        del self.outbound

    def test___init__(self):
        assert self.outbound.client == self.client
    
    def test__generate_files(self, fake):
        count = fake.random_number(2)
        
        files = []
        
        while count > 0:
            files.append(File(self.client, fake.pystr(), 
                              mime_type=fake.mime_type()))
            count -= 1
        
        result = self.outbound._generate_files(files)
        
        for i, f in enumerate(result):
            assert f[1] == files[i].file_tuple()
        
        count = fake.random_number(2)
        
        files = []
        
        while count > 0:
            files.append(fake.uri())
            count -= 1
            
        result = self.outbound._generate_files(files)
        
        for i, f in enumerate(result):
            assert f[1][3]['Content-Location'] == files[i]
    
    
    def test_deliver(self, fake, fax_number, message_id):
        return_value = "https://rest.interfax.net/outbound/faxes/{0}".format(
            message_id)

        self.client.post.return_value = return_value
        
        files = fake.pytuple(10, True, str)

        kwargs = fake.pydict()
        
        valid_keys = ['fax_number', 'contact', 'postpone_time', 
                      'retries_to_perform', 'csid', 'page_header', 'reference', 
                      'reply_address', 'page_size', 'fit_to_page', 
                      'page_orientation', 'resolution', 'rendering']
        
        self.outbound._generate_files = m = Mock()
        
        result = self.outbound.deliver(fax_number, files, **kwargs)
        
        kwargs['fax_number'] = fax_number
    
        self.client.post.assert_called_with('/outbound/faxes', kwargs, 
                                            valid_keys, files=m.return_value)
        
        assert isinstance(result, OutboundFax)
        assert result.id == str(message_id)
        assert result.client == self.client

    def test_all(self, fake, message_id):
        self.client.get.return_value = [{'id': message_id}]

        valid_keys = ['limit', 'last_id', 'sort_order', 'user_id']

        kwargs = fake.pydict()

        result = self.outbound.all(**kwargs)

        self.client.get.assert_called_with('/outbound/faxes', kwargs, valid_keys)

        assert isinstance(result[0], OutboundFax)
        assert result[0].id == message_id
        assert result[0].client == self.client

    def test_completed(self, fake, message_id):
        self.client.get.return_value = [{'id': message_id}]

        ids = fake.pytuple(10, True, int)

        valid_keys = ['ids']

        kwargs = {'ids': ids}

        result = self.outbound.completed(*ids)

        self.client.get.assert_called_with('/outbound/faxes/completed', kwargs, 
                                           valid_keys)

        assert isinstance(result[0], OutboundFax)
        assert result[0].id == message_id
        assert result[0].client == self.client

    def test_find(self, message_id):
        self.client.get.return_value = {'id': message_id}

        result = self.outbound.find(message_id)

        self.client.get.assert_called_with(
            '/outbound/faxes/{0}'.format(message_id))

        assert isinstance(result, OutboundFax)
        assert result.id == message_id
        assert result.client == self.client

    def test_image(self, fake, message_id):
        self.client.get.return_value = return_value = fake.binary()

        result = self.outbound.image(message_id)

        self.client.get.assert_called_with(
            '/outbound/faxes/{0}/image'.format(message_id))

        assert isinstance(result, Image)
        assert result.data == return_value
        assert result.client == self.client

    def test_cancel(self, message_id):
        self.outbound.cancel(message_id)

        self.client.post.assert_called_with(
            '/outbound/faxes/{0}/cancel'.format(message_id))

    def test_search(self, fake, message_id):
        self.client.get.return_value = [{'id': message_id}]

        valid_keys = ['ids', 'reference', 'date_from', 'date_to', 'status',
                      'user_id', 'fax_number', 'limit', 'offset']

        kwargs = fake.pydict()

        result = self.outbound.search(**kwargs)

        self.client.get.assert_called_with('/outbound/search', kwargs, 
                                           valid_keys)

        assert isinstance(result[0], OutboundFax)
        assert result[0].id == message_id
        assert result[0].client == self.client
