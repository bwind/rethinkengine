from .. import Foo

import unittest2 as unittest


class CreateTestCase(unittest.TestCase):
    def setUp(self):
        # Make sure Foo is empty
        Foo.objects.delete()

    def test_get_or_create_new(self):
        created, doc = Foo.objects.get_or_create(name='John')
        self.assertTrue(created)
        self.assertIsInstance(doc, Foo)

    def test_get_or_create_existing(self):
        Foo(name='John').save()
        created, doc = Foo.objects.get_or_create(name='John')
        self.assertFalse(created)
        self.assertIsInstance(doc, Foo)

    def test_create(self):
        doc = Foo.objects.create(name='John')
        self.assertIsInstance(doc, Foo)
