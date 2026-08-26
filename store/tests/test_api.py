from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book


class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.book_1 = Book.objects.create(
            name="Dune", price="1125.00", author="Frank Herbert"
        )
        self.book_2 = Book.objects.create(
            name="Foundation", price="2225.00", author="Isaac Asimov"
        )

    def test_list_returns_books_in_id_order(self):
        response = self.client.get(reverse("book-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            [
                {
                    "id": self.book_1.id,
                    "name": "Dune",
                    "price": "1125.00",
                    "author": "Frank Herbert",
                },
                {
                    "id": self.book_2.id,
                    "name": "Foundation",
                    "price": "2225.00",
                    "author": "Isaac Asimov",
                },
            ],
        )

    def test_create_book(self):
        response = self.client.post(
            reverse("book-list"),
            {"name": "Solaris", "price": "890.50", "author": "Stanislaw Lem"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Solaris")
        self.assertEqual(response.data["price"], "890.50")
        self.assertTrue(Book.objects.filter(pk=response.data["id"]).exists())

    def test_create_book_without_author_returns_validation_error(self):
        response = self.client.post(
            reverse("book-list"),
            {"name": "Solaris", "price": "890.50"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("author", response.data)

    def test_retrieve_book(self):
        response = self.client.get(reverse("book-detail", kwargs={"pk": self.book_1.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": self.book_1.id,
                "name": "Dune",
                "price": "1125.00",
                "author": "Frank Herbert",
            },
        )

    def test_retrieve_missing_book_returns_not_found(self):
        response = self.client.get(reverse("book-detail", kwargs={"pk": 99999}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_book(self):
        response = self.client.patch(
            reverse("book-detail", kwargs={"pk": self.book_1.id}),
            {"price": "1300.00"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book_1.refresh_from_db()
        self.assertEqual(str(self.book_1.price), "1300.00")

    def test_delete_book(self):
        response = self.client.delete(reverse("book-detail", kwargs={"pk": self.book_1.id}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book_1.id).exists())
