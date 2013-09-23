from rethinkengine.connection import connect, disconnect, ConnectionError
from rethinkengine.document import Document
from rethinkengine.fields import *
from query_set import *

import rethinkdb as r


DB_NAME = 'test'


class Foo(Document):
    name = TextField()
    number = IntegerField()


def setUp():
    connect(DB_NAME)
    try:
        Foo().table_create()
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
