from django.test import TestCase

from store.models import Book
from store.serializers import BooksSerializer


class BooksSerializerTestCase(TestCase):
    def test_serializes_all_book_fields(self):
        book_1 = Book.objects.create(name="Dune", price="1125.00", author="Frank Herbert")
        book_2 = Book.objects.create(
            name="Foundation", price="2225.00", author="Isaac Asimov"
        )

        data = BooksSerializer([book_1, book_2], many=True).data

        self.assertEqual(
            data,
            [
                {
                    "id": book_1.id,
                    "name": "Dune",
                    "price": "1125.00",
                    "author": "Frank Herbert",
                },
                {
                    "id": book_2.id,
                    "name": "Foundation",
                    "price": "2225.00",
                    "author": "Isaac Asimov",
                },
            ],
        )

    def test_rejects_price_with_too_many_digits(self):
        serializer = BooksSerializer(
            data={"name": "Dune", "price": "100000.00", "author": "Frank Herbert"}
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("price", serializer.errors)
