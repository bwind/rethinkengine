from .. import Foo
from rethinkengine.query_set import InvalidQueryError

import unittest2 as unittest


class FilterTestCase(unittest.TestCase):
    def test_filter_twice(self):
        with self.assertRaises(InvalidQueryError):
            Foo.objects.filter(name='John').filter(name='Jill')
