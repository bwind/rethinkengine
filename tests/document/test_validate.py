from .. import Foo
from rethinkengine import *

import unittest2 as unittest


class ValidateTestCase(unittest.TestCase):
    def test_does_not_validate(self):
        f = Foo(name=1)
        with self.assertRaises(ValidationError):
            f.validate()

    def test_validates(self):
        # If Document.__init__ doesn't raise an error, this test passes
        f = Foo(name='foo', number=42)
