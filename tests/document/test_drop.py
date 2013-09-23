from .. import Foo

import rethinkdb as r
import unittest2 as unittest


class DropTestCase(unittest.TestCase):
    def tearDown(self):
        # recreate Foo table
        Foo().table_create()

    def test_drop(self):
        Foo().table_drop()
        with self.assertRaises(r.RqlRuntimeError):
            Foo(name='John').save()
