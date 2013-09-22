from rethinkengine import *

import unittest2 as unittest


class Foo(Document):
    name = TextField()


class ValidateTestCase(unittest.TestCase):
    def test_does_not_validate(self):
        with self.assertRaises(ValidationError):
            f = Foo(name=1)

    def test_validates(self):
        # If Document.__init__ doesn't raise an error, this test passes
        f = Foo(name='foo')
