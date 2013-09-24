from .. import Foo
import unittest2 as unittest


class SkipTestCase(unittest.TestCase):
    def setUp(self):
        # First, delete all objects
        Foo.objects.delete()

        Foo(name='John', number=5).save()
        Foo(name='Jack', number=10).save()
        Foo(name='Jill', number=10).save()
        Foo(name='Jane', number=10).save()
        Foo(name='Jade', number=15).save()

    def tearDown(self):
        Foo.objects.delete()

    def test_skip_zero(self):
        result = Foo.objects.all().skip(0)
        self.assertEqual(len(result), 5)

    def test_skip_two(self):
        result = Foo.objects.all().skip(2)
        self.assertEqual(len(result), 3)

    def test_skip_all(self):
        result = Foo.objects.all().skip(5)
        self.assertEqual(len(result), 0)

    def test_filter_and_skip(self):
        result = Foo.objects.filter(number=10).skip(2)
        self.assertEqual(len(result), 1)

    def test_limit_and_skip(self):
        result = Foo.objects.limit(3).skip(1)
        self.assertEqual(len(result), 2)

