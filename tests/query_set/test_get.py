from .. import Foo

import unittest2 as unittest


class GetTestCase(unittest.TestCase):
    def setUp(self):
        Foo.objects.delete()

        Foo(name='foo').save()
        Foo(name='foo').save()
        Foo(name='foo1').save()

    def test_get_none(self):
        with self.assertRaises(Foo.DoesNotExist):
            Foo.objects.get(name='bar')

    def test_get_multiple(self):
        with self.assertRaises(Foo.MultipleObjectsReturned):
            Foo.objects.get(name='foo')

    def test_get_one(self):
        f = Foo.objects.get(name='foo1')
        self.assertIsInstance(f, Foo)
