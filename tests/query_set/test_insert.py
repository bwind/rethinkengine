__author__ = 'kuznetsov'

from .. import Foo
import unittest2 as unittest
from rethinkengine.query_set import InvalidQueryError


class FilterTestCase(unittest.TestCase):
    def setUp(self):
        Foo.objects.delete()

        Foo(name='Jack', number=42).save()
        Foo(name='Jill', number=42).save()
        Foo(name='John', number=42).save()

    def test_batch_insert(self):
        Foo.objects.insert([Foo(name="Ron", number=42), Foo(name="Don", number=42)])
        self.assertEqual(len(Foo.objects.all()), 5)
