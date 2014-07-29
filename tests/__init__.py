from rethinkengine.connection import connect, disconnect, ConnectionError
from rethinkengine.document import Document
from rethinkengine.fields import *
from query_set import *

import rethinkdb as r


DB_NAME = 'test'


class Foo(Document):
    name = StringField(required=False)
    number = IntegerField(required=False)


class User(Document):
    class Meta(object):
        primary_key_field = 'email'

    email = StringField()
    born_date = DateField()


def setUp():
    connect(DB_NAME)
    try:
        Foo.table_create()
        User.table_create()

    except r.RqlRuntimeError:
        pass


def tearDown():
    try:
        disconnect(DB_NAME)
    except ConnectionError:
        pass

    try:
        disconnect()
    except ConnectionError:
        pass
