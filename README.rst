rethinkengine
=============

RethinkDB Object-Document Mapper written in Python

Rethinkengine is currently in development and not ready for production
use.

Running unit tests
------------------

|Build Status| |Coverage Status|

In the root of the repository you'll find ``runtests.sh``, which will
run all the tests and show coverage stats. Requires packages ``nose``
and ``coverage`` to be installed. Rethinkengine aims to be compatible
with Python versions 2.6 and 2.7. Python 3 support will be added later.

Connecting to RethinkDB
-----------------------

::

    from rethinkengine import connect
    connect('dbname')

If ``dbname`` doesn't exist, it will be created for you.

Defining Documents
------------------

::

    from rethinkengine import *

    class User(Document):
        name = StringField()
        colors = ListField()

    # Create the table
    User.table_create()

Storing data
------------

::

    u = User(name='John', colors=['red', 'blue'])
    u.save()

    u.colors = []
    u.save()

Retrieving data
---------------

::

    for u in User.objects.all():
        print u.name, u.colors

    for u in User.objects.filter(name='John'):
        print u.name, u.colors

    for u in User.objects.all().order_by('name'):
        for field, value in u.items():
            print field, value

.. |Build Status| image:: https://travis-ci.org/bwind/rethinkengine.png?branch=master
   :target: https://travis-ci.org/bwind/rethinkengine
.. |Coverage Status| image:: https://coveralls.io/repos/bwind/rethinkengine/badge.png
   :target: https://coveralls.io/r/bwind/rethinkengine
