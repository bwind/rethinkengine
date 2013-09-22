from rethinkengine import *

import unittest2 as unittest


class Foo(Document):
    name = TextField()
    number = IntegerField()


class DocumentTestCase(unittest.TestCase):
    def test_set_does_not_exist(self):
        # Should not raise an error
        f = Foo(doesnotexist='foo')
        f.asdf = 'foo'

    def test_get_does_not_exist(self):
        f = Foo(name='foo')
        with self.assertRaises(AttributeError):
            f.doesnotexist

    def test_str(self):
        s = str(Foo(name='foo'))
        self.assertEqual(s, '<Foo object>')

    def test_repr(self):
        r = repr(Foo(name='foo'))
        self.assertEqual(r, '<Foo object>')

    def test_iter(self):
        f = Foo(name='foo', number=42)
        self.assertEqual(f.next(), 'pk')
        self.assertEqual(f.next(), 'name')
        self.assertEqual(f.next(), 'number')

    def test_items(self):
        items = Foo(name='foo', number=42).items()
        del items['pk']
        self.assertEqual(items, {'name': 'foo', 'number': 42})
