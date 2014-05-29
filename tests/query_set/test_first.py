from .. import Foo

import unittest2 as unittest


class GetTestCase(unittest.TestCase):
    def setUp(self):
        Foo.objects.delete()

        Foo(name='foo').save()

    def test_get_none(self):
        f = Foo.objects.first(name='bar')
        self.assertIsNone(f)

    def test_get_one(self):
        f = Foo.objects.first(name='foo')
        self.assertIsInstance(f, Foo)
