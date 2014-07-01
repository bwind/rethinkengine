from .. import Foo

import rethinkdb as r
import unittest2 as unittest


class CreateTableTestCase(unittest.TestCase):
    def tearDown(self):
        # recreate Foo table
        Foo.table_create()

    def test_create(self):
        Foo.table_drop()
        Foo.table_create()
        Foo.table_create()
        with self.assertRaises(r.RqlRuntimeError):
            Foo.table_create(if_not_exists=False)
