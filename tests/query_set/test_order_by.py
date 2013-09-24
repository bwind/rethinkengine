from .. import Foo
import unittest2 as unittest


class OrderByTestCase(unittest.TestCase):
    def setUp(self):
        # First, delete all objects
        Foo.objects.delete()

        Foo(name='John', number=5).save()
        Foo(name='Jack', number=10).save()
        Foo(name='Jill', number=15).save()

    def test_order_by_int(self):
        result = [f.number for f in Foo.objects.all().order_by('number')]
        self.assertEqual(result, [5, 10, 15])

    def test_order_by_int_reverse(self):
        result = [f.number for f in Foo.objects.all().order_by('-number')]
        self.assertEqual(result, [15, 10, 5])

    def test_order_by_str(self):
        result = [f.name for f in Foo.objects.all().order_by('name')]
        self.assertEqual(result, ['Jack', 'Jill', 'John'])

    def test_order_by_str_reverse(self):
        result = [f.name for f in Foo.objects.all().order_by('-name')]
        self.assertEqual(result, ['John', 'Jill', 'Jack'])

