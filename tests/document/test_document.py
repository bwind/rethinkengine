from rethinkengine import *

import rethinkdb as r
import unittest2 as unittest


DB_NAME = 'test'


class Foo(Document):
    name = TextField()
    number = IntegerField()


def setUp():
    connect(DB_NAME)

def tearDown():
    try:
        disconnect(DB_NAME)
    except ConnectionError:
        pass
    try:
        disconnect()
    except ConnectionError:
        pass


class DocumentTestCase(unittest.TestCase):
    def setUp(self):
        try:
            Foo().table_drop()
        except r.RqlRuntimeError as e:
            print e
        Foo().table_create()

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

    def test_is_dirty_new(self):
        f = Foo()
        self.assertTrue(f._dirty)

    def test_is_not_dirty_after_save(self):
        f = Foo(name='John')
        f.save()
        self.assertFalse(f._dirty)

    def test_is_not_dirty_from_db(self):
        f = Foo(name='John')
        f.save()
        f = Foo.objects.get(name='John')
        self.assertFalse(f._dirty)

    def test_save_non_dirty(self):
        f = Foo(name='John')
        f.save()
        f = Foo.objects.get(name='John')
        result = f.save()
        self.assertTrue(result)
