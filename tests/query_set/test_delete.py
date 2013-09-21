from rethinkengine.connection import connect, disconnect, ConnectionError
from rethinkengine.document import Document
from rethinkengine.fields import TextField

import unittest2 as unittest
import rethinkdb as r


DB_NAME = 'test'


class Foo(Document):
    name = TextField()


class DeleteTestCase(unittest.TestCase):
    def setUp(self):
        connect(DB_NAME)
        try:
            Foo().table_drop()
        except r.RqlRuntimeError as e:
            print e
        Foo().table_create()

        Foo(name='foo1').save()
        Foo(name='foo2').save()
        Foo(name='foo3').save()

    def tearDown(self):
        try:
            disconnect(DB_NAME)
        except ConnectionError:
            pass

    def test_delete_document(self):
        self.assertEqual(len(Foo.objects.all()), 3)
        Foo.objects.get(name='foo1').delete()
        self.assertEqual(len(Foo.objects.all()), 2)

    def test_delete_queryset_all(self):
        self.assertEqual(len(Foo.objects.all()), 3)
        Foo.objects.all().delete()
        self.assertEqual(len(Foo.objects.all()), 0)

    def test_delete_queryset_one(self):
        self.assertEqual(len(Foo.objects.all()), 3)
        Foo.objects.all()[0].delete()
        self.assertEqual(len(Foo.objects.all()), 2)

    def test_delete_queryset_all_after_iter(self):
        objs = Foo.objects.all()
        objs.next()
        objs.delete()
        self.assertEqual(len(Foo.objects.all()), 0)
