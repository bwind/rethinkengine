from .. import Foo
from rethinkengine.query_set import InvalidQueryError

import unittest2 as unittest


class FilterTestCase(unittest.TestCase):
    def setUp(self):
        Foo.objects.delete()

        Foo(name='Jack', number=42).save()
        Foo(name='Jill', number=42).save()
        Foo(name='John', number=42).save()

    def test_filter_twice(self):
        with self.assertRaises(InvalidQueryError):
            Foo.objects.filter(name='John').filter(name='Jill')

    def test_filter_all(self):
        f = Foo.objects.filter(number=42).order_by('name')
        self.assertEqual(f.next().name, 'Jack')
        self.assertEqual(f.next().name, 'Jill')
        self.assertEqual(f.next().name, 'John')

    def test_filter_none(self):
        f = Foo.objects.filter(number=30)
        self.assertEqual(len(f), 0)
        with self.assertRaises(StopIteration):
            f.next()

    def test_filter_one(self):
        f = Foo.objects.filter(name='John')
        self.assertEqual(len(f), 1)
        self.assertEqual(f.next().name, 'John')

    def test_filter_two_fields(self):
        f = Foo.objects.filter(name='Jill', number=42)
        self.assertEqual(len(f), 1)
        f = Foo.objects.filter(name='Jane', number=42)
        self.assertEqual(len(f), 0)
