from rethinkengine.fields import *
from rethinkengine.connection import connect, disconnect, get_conn, \
    ConnectionError
from rethinkengine.document import Document

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import rethinkdb as r


DB_NAME = 'test'


class Foo(Document):
    name = TextField()


def setUp():
    connect(DB_NAME)


def tearDown():
    try:
        disconnect(DB_NAME)
    except ConnectionError:
        pass


class SliceTestCase(unittest.TestCase):
    def setUp(self):
        try:
            Foo().table_drop()
        except r.RqlRuntimeError as e:
            print e
        Foo().table_create()

        Foo(name='foo1').save()
        Foo(name='foo2').save()
        Foo(name='foo3').save()

    def tearDown(self):
        pass

    def test_out_of_range(self):
        with self.assertRaises(IndexError):
            Foo.objects.all()[3]

    def test_in_range(self):
        Foo.objects.all()[0]
        Foo.objects.all()[1]
        Foo.objects.all()[2]

    def test_negative_index(self):
        with self.assertRaises(AssertionError):
            Foo.objects.all()[-1]

    def test_len(self):
        self.assertEqual(len(Foo.objects.all()), 3)

    def test_all(self):
        self.assertEqual(len(Foo.objects.all()[:]), 3)
