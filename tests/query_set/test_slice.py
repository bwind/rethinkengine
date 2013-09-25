from .. import Foo, DB_NAME
from rethinkengine.fields import *
from rethinkengine.connection import connect, disconnect, ConnectionError
from rethinkengine.document import Document

import rethinkdb as r
import unittest2 as unittest


def setUp():
    Foo.objects.all().delete()

    Foo(name='foo1').save()
    Foo(name='foo2').save()
    Foo(name='foo3').save()


class SliceTestCase(unittest.TestCase):
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

    def test_order(self):
        self.assertEqual(Foo.objects.order_by('name')[0].name, 'foo1')
        self.assertEqual(Foo.objects.order_by('name')[1].name, 'foo2')
        self.assertEqual(Foo.objects.order_by('name')[2].name, 'foo3')

    def test_invalid(self):
        with self.assertRaises(TypeError):
            Foo.objects.all()['foo']

    def test_index_after_iter(self):
        f = Foo.objects.order_by('name')
        f.next()
        # [0] should still refer to the first element
        self.assertEqual(f[0].name, 'foo1')
