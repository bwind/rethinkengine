from rethinkengine import *

import unittest2 as unittest


class Foo(Document):
    x1 = StringField()
    x2 = IntegerField()
    x3 = ListField()
    x4 = DictField()
    x5 = BooleanField()


class FieldOrderTestCase(unittest.TestCase):
    def setUp(self):
        self.fields = iter(['pk'] + ['x' + str(i) for i in range(1, 6)])

    def test_field_order_iter(self):
        f = Foo()
        for field in f:
            self.assertEqual(field, self.fields.next())
