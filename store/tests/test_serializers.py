from django.test import TestCase

from store.models import Book
from store.serializers import BooksSerializer


class BooksSerializerTestCase(TestCase):
    def test_ok(self,):
        book_1 = Book.objects.create(name='Test book 1', price=1125, author="Пидар 1")
        book_2 = Book.objects.create(name='Test book 2', price=2225, author="Пидар 2")
        data = BooksSerializer([book_1, book_2], many=True).data
        expected_data = [
            {
                'id':book_1.id,
                'name': 'Test book 1',
                'price': '1125.00',
                'author': 'Пидар 1',
            },
            {
                'id':book_2.id,
                'name': 'Test book 2',
                'price': '2225.00',
                'author': 'Пидар 2',
            },
        ]
        self.assertEqual(data, expected_data)
