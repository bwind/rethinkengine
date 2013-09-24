from rethinkengine.fields import *

import unittest2 as unittest


class PrimaryKeyFieldTestCase(unittest.TestCase):
    def test_default(self):
        f = PrimaryKeyField()
        self.assertEqual(f._default, None)

    def test_is_valid(self):
        f = PrimaryKeyField()
        self.assertTrue(f.is_valid('cdc14784-3327-492b-a1db-ad8a3b8abcef'))

    def test_too_short(self):
        f = PrimaryKeyField()
        self.assertFalse(f.is_valid('cdc14784-3327-492b-a1db-ad8a3b8abce'))

    def test_too_long(self):
        f = PrimaryKeyField()
        self.assertFalse(f.is_valid('cdc14784-3327-492b-a1db-ad8a3b8abcefa'))

    def test_wrong_chars(self):
        f = PrimaryKeyField()
        self.assertFalse(f.is_valid('zzzzzzzz-3327-492b-a1db-ad8a3b8abcef'))

    def test_wrong_type(self):
        f = PrimaryKeyField()
        self.assertFalse(f.is_valid(123))


class TextFieldTestCase(unittest.TestCase):
    def test_default(self):
        f = TextField()
        self.assertEqual(f._default, '')

    def test_is_valid(self):
        f = TextField()
        self.assertTrue(f.is_valid('foo'))
        self.assertTrue(f.is_valid(''))

    def test_wrong_type(self):
        f = TextField()
        self.assertFalse(f.is_valid(123))


class IntegerFieldTestCase(unittest.TestCase):
    def test_default(self):
        f = IntegerField()
        self.assertEqual(f._default, 0)

    def test_is_valid(self):
        f = IntegerField()
        self.assertTrue(f.is_valid(123))

    def test_wrong_type(self):
        f = IntegerField()
        self.assertFalse(f.is_valid('foo'))


class ListFieldTestCase(unittest.TestCase):
    def test_default(self):
        f = ListField()
        self.assertEqual(f._default, [])

    def test_is_valid(self):
        f = ListField()
        self.assertTrue(f.is_valid([1, 2, 3]))

    def test_wrong_type(self):
        f = ListField()
        self.assertFalse(f.is_valid('foo'))


class DictFieldTestCase(unittest.TestCase):
    def test_default(self):
        f = DictField()
        self.assertEqual(f._default, {})

    def test_is_valid(self):
        f = DictField()
        self.assertTrue(f.is_valid({}))
        self.assertTrue(f.is_valid({'foo': 1, 'bar': 2}))

    def test_wrong_type(self):
        f = DictField()
        self.assertFalse(f.is_valid('foo'))
