from .. import Foo
import unittest2 as unittest


class OrderByTestCase(unittest.TestCase):
    def setUp(self):
        # First, delete all objects
        Foo.objects.delete()

        Foo(name='John', number=5).save()
        Foo(name='Jack', number=10).save()
        Foo(name='Jill', number=15).save()
        Foo(name='Jane', number=15).save()
        Foo(name='Jade', number=15).save()

    def tearDown(self):
        Foo.objects.delete()

    def test_order_by_int(self):
        result = [f.number for f in Foo.objects.all().order_by('number')]
        self.assertEqual(result, [5, 10, 15, 15, 15])

    def test_order_by_int_reverse(self):
        result = [f.number for f in Foo.objects.all().order_by('-number')]
        self.assertEqual(result, [15, 15, 15, 10, 5])

    def test_order_by_str(self):
        result = [f.name for f in Foo.objects.all().order_by('name')]
        self.assertEqual(result, ['Jack', 'Jade', 'Jane', 'Jill', 'John'])

    def test_order_by_str_reverse(self):
        result = [f.name for f in Foo.objects.all().order_by('-name')]
        self.assertEqual(result, ['John', 'Jill', 'Jane', 'Jade', 'Jack'])

    def test_order_by_multiple(self):
        result = [(f.name, f.number) for f in
            Foo.objects.all().order_by('number', 'name')]
        expected = [('John', 5), ('Jack', 10), ('Jade', 15), ('Jane', 15),
            ('Jill', 15)]
        self.assertEqual(result, expected)

    def test_order_by_multiple_reverse(self):
        result = [(f.name, f.number) for f in
            Foo.objects.all().order_by('number', '-name')]
        expected = [('John', 5), ('Jack', 10), ('Jill', 15), ('Jane', 15),
            ('Jade', 15)]
        self.assertEqual(result, expected)

    def test_order_by_multiple_reverse_both(self):
        result = [(f.name, f.number) for f in
            Foo.objects.all().order_by('-number', '-name')]
        expected = [('Jill', 15), ('Jane', 15), ('Jade', 15), ('Jack', 10),
            ('John', 5)]
        self.assertEqual(result, expected)

    def test_order_by_pk(self):
        result = [f.pk for f in Foo.objects.all().order_by('pk')]
        result_sorted = sorted(result)
        self.assertEqual(result, result_sorted)

    def test_order_by_pk_reverse(self):
        result = [f.pk for f in Foo.objects.all().order_by('-pk')]
        result_sorted = sorted(result, reverse=True)
        self.assertEqual(result, result_sorted)
