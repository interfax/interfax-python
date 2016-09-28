InterFAX Python Package
=======================

.. image:: https://travis-ci.org/interfax/interfax-python.svg?branch=master
    :target: https://travis-ci.org/interfax/interfax-python

`Installation`_ \| `Getting Started`_ \| `Contributing`_ \| `Usage`_ \| `License`_

Send and receive faxes in Python with the
`InterFAX <https://www.interfax.net/en/dev>`__ REST API.

Installation
------------

This package requires Python 2.6+. You can install it using:

::

    pip install interfax

Getting started
---------------

To send a fax from a PDF file:

.. code:: python

    from interfax import InterFAX

    interfax = InterFAX(username="username", password="password")
    fax = interfax.deliver(fax_number="+11111111112", files=["folder/fax.pdf"])
    fax = fax.reload() # resync with API to get latest status
    fax.status # Success if 0. Pending if < 0. Error if > 0

Usage
=====

`Client`_ \| `Account`_ \| `Outbound`_ \| `Inbound`_ \| `Documents`_ \| `Helper Classes`_

Client
------

The client follows the `12-factor <http://12factor.net/config>`__ apps
principle and can be either set directly or via environment variables.

.. code:: python

    # Initialize using parameters
    interfax = InterFAX(username="...", password="...")

    # Alternatice: Initialize using environment variables
    # * INTERFAX_USERNAME
    # * INTERFAX_PASSWORD
    interfax = InterFAX()

All connections are established over HTTPS.

Account
-------

Balance
~~~~~~~

Determine the remaining faxing credits in your account.

.. code:: python

    >>>  interfax.account.balance()
    9.86

**More:**
`documentation <https://www.interfax.net/en/dev/rest/reference/3001>`__

Outbound
--------

`Send fax`_ \| `Get outbound fax list`_ \| `Get completed fax list`_ \| `Get outbound fax record`_ \| `Get outbound fax image`_ \| `Cancel a fax`_ \| `Search fax list`_

Send fax
~~~~~~~~

``interfax.outbound.deliver(fax_number, files, **kwargs)``

Submit a fax to a single destination number.

There are a few ways to send a fax. One way is to directly provide a
file path or url.

.. code:: python

    # with a path
    interfax.outbound.deliver(fax_number="+11111111112", files=["folder/fax.txt"])
    # with a URL
    interfax.outbound.deliver(fax_number="+11111111112", files=["https://s3.aws.com/example/fax.pdf"])

InterFAX supports over 20 file types including HTML, PDF, TXT, Word, and
many more. For a full list see the `Supported File
Types <https://www.interfax.net/en/help/supported_file_types>`__
documentation.

The returned object is a ``OutboundFax`` with just an ``id``. You can
use this object to load more information, get the image, or cancel the
sending of the fax.

.. code:: python

    fax = interfax.outbound.deliver(fax_number="+11111111112", files=["fax.pdf"])
    fax = fax.reload() # Reload fax, allowing you to inspect the status and more

    fax.id        # the ID of the fax that can be used in some of the other API calls
    fax.image()     # returns an image representing the fax sent to the fax_number
    fax.cancel()    # cancel the sending of the fax

Alternatively you can create an `File <#file>`__ with binary data and
pass this in as well.

.. code:: python

    with open("fax.pdf", "rb") as fp:
        f = interfax.files.create(fp.read(), mime_type="application/pdf")
    interfax.outbound.deliver(fax_number="+11111111112", files=[f])

To send multiple files just pass in a list of strings and `File`_ objects.

.. code:: python

    interfax.outbound.deliver(fax_number="+11111111112", files=["fax.pdf", "https://s3.aws.com/example/fax.pdf"])

Under the hood every path and string is turned into a
`File <#interfaxfile>`__ object. For more information see `the
documentation <#interfaxfile>`__ for this class.

**Keyword Arguments:** ``contact``, ``postpone_time``,
``retries_to_perform``, ``csid``, ``page_header``, ``reference``,
``page_size``, ``fit_to_page``, ``page_orientation``, ``resolution``,
``rendering``

**More:**
`documentation <https://www.interfax.net/en/dev/rest/reference/2918>`__

**Alias**: ``interfax.deliver``

--------------

Get outbound fax list
~~~~~~~~~~~~~~~~~~~~~

``interfax.outbound.all(**kwargs)``

Get a list of recent outbound faxes (which does not include batch
faxes).

.. code:: python

    >>> interfax.outbound.all()
    [OutboundFax(id=1), ...]
    >>> interfax.outbound.all(limit=1)
    [OutboundFax(id=1)]

**Keyword Arguments:** ``limit``, ``last_id``, ``sort_order``,
``user_id``

**More:**
`documentation <https://www.interfax.net/en/dev/rest/reference/2920>`__

--------------

Get completed fax list
~~~~~~~~~~~~~~~~~~~~~~

``interfax.outbound.completed(*args)``

Get details for a subset of completed faxes from a submitted list.
(Submitted id's which have not completed are ignored).

.. code:: python

    >> interfax.outbound.completed(123, 234)
    [OutboundFax(id=123), ...]

**More:**
`documentation <https://www.interfax.net/en/dev/rest/reference/2972>`__

--------------

Get outbound fax record
~~~~~~~~~~~~~~~~~~~~~~~

``interfax.outbound.find(fax_id)``

Retrieves information regarding a previously-submitted fax, including
its current status.

.. code:: python

    >>> interfax.outbound.find(123456)
    OutboundFax(id=123456)

**More:**
`documentation <https://www.interfax.net/en/dev/rest/reference/2921>`__

--------------

Get outbound fax image
~~~~~~~~~~~~~~~~~~~~~~

``interfax.outbound.image(fax_id)``

Retrieve the fax image (TIFF file) of a submitted fax.

.. code:: python

    >>> image = interfax.outbound.image(123456)
    Image(id=123456)
    >>> image.data
    "....binary data...."
    >>> image.save("fax.tiff")
    # saves image to file

**More:**
`documentation <https://www.interfax.net/en/dev/rest/reference/2941>`__

--------------

Cancel a fax
~~~~~~~~~~~~

``interfax.outbound.cancel(fax_id)``

Cancel a fax in progress.

.. code:: python

    interfax.outbound.cancel(123456)
    => true

**More:**
`documentation <https://www.interfax.net/en/dev/rest/reference/2939>`__

--------------

Search fax list
~~~~~~~~~~~~~~~

``interfax.outbound.search(**kwargs)``

Search for outbound faxes.

.. code:: python

    >>> interfax.outbound.search(fax_number="+1230002305555")
    [OutboundFax(id=1234), ...]

**Keyword Arguments:** ``ids``, ``reference``, ``date_from``,
``date_to``, ``status``, ``user_id``, ``fax_number``, ``limit``,
``offset``

**More:**
`documentation <https://www.interfax.net/en/dev/rest/reference/2959>`__

Inbound
-------

`Get inbound fax list`_ \| `Get inbound fax record`_ \| `Get inbound fax image`_ \| `Get forwarding emails`_ \| `Mark as read/unread`_ \| `Resend inbound fax`_

Get inbound fax list
~~~~~~~~~~~~~~~~~~~~

``interfax.inbound.all(**kwargs)``

Retrieves a user's list of inbound faxes. (Sort order is always in
descending ID).

.. code:: python

    interfax.inbound.all()
    => [InboundFax(id=1234), ...]
    interfax.inbound.all(limit=1)
    => [InboundFax(id=1234)]

**Keyword Arguments:** ``unread_only``, ``limit``, ``last_id``,
``all_users``

**More:**
`documentation <https://www.interfax.net/en/dev/rest/reference/2935>`__

--------------

Get inbound fax record
~~~~~~~~~~~~~~~~~~~~~~

``interfax.inbound.find(fax_id)``

Retrieves a single fax's metadata (receive time, sender number, etc.).

.. code:: python

    >>> interfax.inbound.find(123456)
    InboundFax(id=123456)

**More:**
`documentation <https://www.interfax.net/en/dev/rest/reference/2938>`__

--------------

Get inbound fax image
~~~~~~~~~~~~~~~~~~~~~

``interfax.inbound.image(fax_id)``

Retrieves a single fax's image.

.. code:: python

    >>> image = interfax.inbound.image(123456)
    Image(id=123456)
    >>> image.data
    "....binary data...."
    >>> image.save("fax.tiff")
    # saves image to file

**More:**
`documentation <https://www.interfax.net/en/dev/rest/reference/2937>`__

--------------

Get forwarding emails
~~~~~~~~~~~~~~~~~~~~~

``interfax.inbound.emails(fax_id)``

Retrieve the list of email addresses to which a fax was forwarded.

.. code:: python

    interfax.inbound.email(123456)
    [ForwardingEmail()]

**More:**
`documentation <https://www.interfax.net/en/dev/rest/reference/2930>`__

--------------

Mark as read/unread
~~~~~~~~~~~~~~~~~~~

``interfax.inbound.mark(fax_id, read=True)``

Mark a transaction as read/unread.

.. code:: python

    interfax.inbound.mark(123456, read=True) # mark read
    interfax.inbound.mark(123456, read=False) # mark unread

**More:**
`documentation <https://www.interfax.net/en/dev/rest/reference/2936>`__

--------------

Resend inbound fax
~~~~~~~~~~~~~~~~~~

``interfax.inbound.resend(fax_id, email=None)``

Resend an inbound fax to a specific email address.

.. code:: python

    >>> # resend to the email(s) to which the fax was previously forwarded
    >>> interfax.inbound.resend(123456)
    True
    >>> # resend to a specific address
    >>> interfax.inbound.resend(123456, email="test@example.com")
    True

**More:**
`documentation <https://www.interfax.net/en/dev/rest/reference/2929>`__

--------------

Documents
---------

`Create Documents`_ \| `Upload chunk`_ \| `Get document list`_ \| `Get document status`_ \| `Cancel document`_

Document allow for uploading of large files up to 20MB in 200kb chunks.
The `File`_ format automatically uses this if needed but a
sample implementation would look as followed.

.. code:: python

    document = interfax.documents.create("test.pdf", os.stat("test.pdf").st_size)

    with open("test.pdf", "rb") as fp:
        cursor = 0
        while True:
            chunk = fp.read(500)
            if not chunk:
                break
            next_cursor = cursor + len(chunk)
            document.upload(cursor, next_cursor-1, chunk)
            cursor = next_cursor

Create Documents
~~~~~~~~~~~~~~~~

``interfax.documents.create(name, size, **kwargs)``

Create a document upload session, allowing you to upload large files in
chunks.

.. code:: python

    >>> interfax.documents.create("large_file.pdf", 231234)
    Document(id=123456)

**Keyword Arguments:** ``disposition``, ``sharing``

**More:**
`documentation  <https://www.interfax.net/en/dev/rest/reference/2967>`__

--------------

Upload chunk
~~~~~~~~~~~~

``interfax.documents.upload(id, range_start, range_end, chunk)``

Upload a chunk to an existing document upload session.

.. code:: python

    >>> interfax.documents.upload(123456, 0, 999, "....binary-data....")
    True

**More:**
`documentation <https://www.interfax.net/en/dev/rest/reference/2966>`__

--------------

Get document list
~~~~~~~~~~~~~~~~~

``interfax.documents.all(options = {})``

Get a list of previous document uploads which are currently available.

.. code:: python

    >>> interfax.documents.all()
    [Document(id=123456), ...]
    >>> interfax.documents.all(offset=10)
    [Document(id=123466), ...]

**Keyword Arguments:** ``limit``, ``offset``

**More:**
`documentation <https://www.interfax.net/en/dev/rest/reference/2968>`__

--------------

Get document status
~~~~~~~~~~~~~~~~~~~

``interfax.documents.find(id)``

Get the current status of a specific document upload.

.. code:: python

    >>> interfax.documents.find(123456)
    Document(id=123456)

**More:**
`documentation <https://www.interfax.net/en/dev/rest/reference/2965>`__

--------------

Cancel document
~~~~~~~~~~~~~~~

``interfax.documents.cancel(id)``

Cancel a document upload and tear down the upload session, or delete a
previous upload.

.. code:: python

    >>> interfax.documents.cancel(123456)
    True

**More:**
`documentation <https://www.interfax.net/en/dev/rest/reference/2964>`__

--------------

Helper Classes
--------------

OutboundFax
~~~~~~~~~~~

The ``OutboundFax`` is returned in most Outbound APIs. As a convenience
the following methods are available.

.. code:: python

    fax = interfax.outbound.find(123)
    fax = fax.reload() # Loads or reloads object
    fax.cancel() # Cancels the fax
    fax.image() # Returns an `Image` for this fax

InboundFax
~~~~~~~~~~

The ``InboundFax`` is returned in some of the Inbound APIs. As a
convenience the following methods are available.

.. code:: python

    fax = interfax.inbound.find(123)
    fax = fax.reload() # Loads or reloads object
    fax.mark(true) # Marks the fax as read/unread
    fax.resend(email) # Resend the fax to a specific email address.
    fax.image() # Returns an `Image` for this fax
    fax.emails() # Returns a list of ForwardingEmail objects that the fax was forwarded on to

Image
~~~~~

A lightweight wrapper around the image data for a sent or received fax.
Provides the following convenience methods.

.. code:: python

    image = interfax.outbound.image(123)
    image.data # Returns the raw binary data for the TIFF image.
    image.save("folder/fax.tiff") # Saves the TIFF to the path provided

File
~~~~

This class is used by ``interfax.outbound.deliver`` and
``interfax.files`` to turn every URL, path and binary data into a
uniform format, ready to be sent out to the InterFAX API.

It is most useful for sending binary data to the ``.deliver`` method.

.. code:: python

    >>> # binary data
    >>> f = File(interfax, "....binary data.....", mime_type="application/pdf")
    File()

    >>> # Alternatively
    >>> f = interfax.files.create("....binary data.....", mime_type="application/pdf")
    >>> f.headers
    {"Content-Type": "application/pdf"}
    >>> f.body
    "....binary data....."

    interfax.outbound.deliver(fax_number="+1111111111112", files=[f])

Additionally it can be used to turn a URL or path into a valid object as
well, though the ``.deliver`` method does this conversion automatically.

.. code:: python

    >>> # a file by path
    >>> f = interfax.files.create("foo/bar.pdf")
    >>> f.headers
    { "Content-Type": "application/pdf" }
    >>> f.body
    "....binary data....."

    >>> # a file by url
    >>> f = interfax.files.create("https://foo.com/bar.html")
    >>> f.headers
    {"Content-Location": "https://foo.com/bar.html"}
    >>> f.body
    None

ForwardingEmail
~~~~~~~~~~~~~~~

A light wrapper around `the
response <https://www.interfax.net/en/dev/rest/reference/2930>`__ received by
asking for the forwarded emails for a fax.

.. code:: python

    fax = interfax.inbound.find(123)
    email = fax.emails()[0]
    email.email_address # An email address to which forwarding of the fax was attempted.
    email.message_status # 0 = OK; number smaller than zero = in progress; number greater than zero = error.
    email.completion_time # Completion timestamp.

Document
~~~~~~~~

The ``Document`` is returned in most of the Document APIs. As a
convenience the following methods are available.

.. code:: python

    document = interfax.documents.find(123)
    document = document.reload() # Loads or reloads object
    document.upload(0, 999, ".....binary data...." # Maps to the interfax.documents.upload method
    document.cancel() # Maps to the interfax.documents.cancel method
    document.id  # Extracts the ID from the URI (the API does not return the ID)

Contributing
------------

#. **Fork** the repo on GitHub
#. **Clone** the project to your own machine
#. **Commit** changes to your own branch
#. **Push** your work back up to your fork
#. Submit a **Pull request** so that we can review your changes

License
-------

This library is released under the `MIT License <https://github.com/interfax/interfax-python/blob/master/LICENSE>`__.