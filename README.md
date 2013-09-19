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

    connect('test')

    class User(Document):
        name = TextField()
        colors = ListField()

    User().table_create()

    u = User(name='John', colors=['red', 'blue'])
    u.save()

    print [u.name for u in User.objects.all()]
    print [u.colors for u in User.objects.filter(name='John')]
