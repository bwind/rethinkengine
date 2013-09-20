rethinkengine
=============

RethinkDB Object-Document Mapper written in Python

Rethinkengine is currently in development and not ready for production use.

Running unit tests
------------------

In the root of the repository you'll find `runtests.sh`, which will run all the tests and show coverage stats. Requires packages `nose` and `coverage` to be installed.

Defining Documents
------------------

    from rethinkengine import *

    class User(Document):
        name = TextField()
        colors = ListField()

    # Create the table
    User().table_create()

Connecting to RethinkDB
-----------------------

    from rethinkengine import connect
    connect('dbname')

Storing data
------------

    u = User(name='John', colors=['red', 'blue'])
    u.save()

    u.colors = []
    u.save()

Retrieving data
---------------

    for u in User.objects.all():
        print u.name, u.colors

    for u in User.objects.filter(name='John'):
        print u.name, u.colors

    User.objects.all().order_by('name')
