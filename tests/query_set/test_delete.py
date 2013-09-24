from .. import Foo, DB_NAME
from rethinkengine.connection import connect, disconnect, ConnectionError

import unittest2 as unittest
import rethinkdb as r


class DeleteTestCase(unittest.TestCase):
    def setUp(self):
        connect(DB_NAME)
        Foo.objects.all().delete()

        Foo(name='foo1').save()
        Foo(name='foo2').save()
        Foo(name='foo3').save()

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
