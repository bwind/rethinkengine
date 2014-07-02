from .. import Foo, User
from rethinkengine import RqlOperationError

import unittest2 as unittest


class DocumentTestCase(unittest.TestCase):
    def setUp(self):
        Foo.objects.all().delete()
        User.objects.all().delete()

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
        items = dict(Foo(name='foo', number=42).items())
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

    def test_save_and_update(self):
        # Insert a new document and save its pk
        f = Foo(name='John')
        f.save()
        pk = f.pk

        # Update the doc
        f.name = 'Jack'
        f.save()

        # Retrieve doc and make sure pks are equal
        f = Foo.objects.get(name='Jack')
        self.assertEqual(f.pk, pk)

    def test_rql_operation_error(self):
        user1 = User(email='contact1@example.com')
        user1.save()

        user2 = User(email='contact2@example.com')
        user2.save()

        with self.assertRaises(RqlOperationError):
            user3 = User(email='contact1@example.com')
            user3.save()
