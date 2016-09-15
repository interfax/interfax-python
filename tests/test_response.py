from interfax.response import Response, InboundFax

from inflection import underscore

try:
    from unittest.mock import Mock, patch, call
except ImportError:
    from mock import Mock, patch, call

class TestResponse(object):
    def test___init__(self, fake_dict):
        client = Mock()
        
        obj = Response(client, fake_dict)

        for k, v in fake_dict.items():
            assert getattr(obj, underscore(k)) == v

        assert obj.client == client

class TestInboundFax(object):
    def test_inheritance(self, inbound_fax):
        assert isinstance(inbound_fax, Response)
    
    def test_id(self, inbound_fax):
        assert inbound_fax.id == inbound_fax.message_id
    
    def test_image(self, inbound_fax):
        fax = inbound_fax

        assert fax.image() == fax.client.inbound.image.return_value

        fax.client.inbound.image.assert_called_with(fax.id)

    def test_reload(self, inbound_fax):
        fax = inbound_fax

        assert fax.reload() == fax.client.inbound.find.return_value

        fax.client.inbound.find.assert_called_with(fax.id)

    def test_mark(self, inbound_fax, fake):
        fax = inbound_fax

        read = fake.boolean()

        assert fax.mark(read) == fax.client.inbound.mark.return_value

        fax.client.inbound.mark.assert_called_with(fax.id, read)

    def test_resend(self, inbound_fax, fake):
        fax = inbound_fax

        email = fake.email() if fake.boolean() else None

        assert fax.resend(email) == fax.client.inbound.resend.return_value

        fax.client.inbound.resend.assert_called_with(fax.id, email)


class TestOutboundFax(object):
    def test_inheritance(self, outbound_fax):
        assert isinstance(outbound_fax, Response)
    
    def test_image(self, outbound_fax):
        fax = outbound_fax

        assert fax.image() == fax.client.outbound.image.return_value

        fax.client.outbound.image.assert_called_with(fax.id)

    def test_reload(self, outbound_fax):
        fax = outbound_fax
        
        assert fax.reload() == fax.client.outbound.find.return_value

        fax.client.outbound.find.assert_called_with(fax.id)

    def test_cancel(self, outbound_fax):
        fax = outbound_fax
        
        assert fax.cancel() == fax.client.outbound.cancel.return_value

        fax.client.outbound.cancel.assert_called_with(fax.id)


class TestDocument(object):
    def test_inheritance(self, document):
        assert isinstance(document, Response)
    
    def test_id(self, document):
        assert document.id == document.uri.split('/')[-1]
    
    def test_upload(self, document, fake):
        start = fake.random_number()
        end = fake.random_number()
        chunk = fake.pystr()

        result = document.upload(start, end, chunk)

        assert result == document.client.documents.upload.return_value

        document.client.documents.upload.assert_called_with(document.id, start, 
                                                            end, chunk)

    def test_reload(self, document):
        doc = document
        
        assert doc.reload() == doc.client.documents.find.return_value

        doc.client.documents.find.assert_called_with(doc.id)

    def test_cancel(self, document):
        doc = document
        
        assert doc.cancel() == doc.client.documents.cancel.return_value

        doc.client.documents.cancel.assert_called_with(doc.id)

class TestImage(object):
    def test_inheritance(self, image):
        assert isinstance(image, Response)

    def test_save(self, image, fs, fake):
        filename = '/{0}'.format(fake.file_name(extension='tiff'))
        
        image.save(filename)
        
        with open(filename, 'rb') as f:
            data = f.read()
        
        assert image.data == data