from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book


class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="api-user", password="test-password"
        )
        self.client.force_authenticate(user=self.user)
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

    def test_filter_books_by_price(self):
        response = self.client.get(reverse("book-list"), {"price": "1125.00"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([book["id"] for book in response.data], [self.book_1.id])
        self.assertEqual(response.data[0]["price"], "1125.00")

    def test_search_books_by_name_and_author(self):
        test_cases = [
            ("dune", self.book_1.id),
            ("asimov", self.book_2.id),
        ]

        for search_query, expected_book_id in test_cases:
            with self.subTest(search_query=search_query):
                response = self.client.get(
                    reverse("book-list"), {"search": search_query}
                )

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(
                    [book["id"] for book in response.data], [expected_book_id]
                )

    def test_order_books_by_price_and_author(self):
        for ordering in ["-price", "author"]:
            with self.subTest(ordering=ordering):
                response = self.client.get(reverse("book-list"), {"ordering": ordering})

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(
                    [book["id"] for book in response.data],
                    [self.book_2.id, self.book_1.id]
                    if ordering == "-price"
                    else [self.book_1.id, self.book_2.id],
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


class UnauthenticatedBooksApiTestCase(APITestCase):
    def test_list_is_forbidden_for_anonymous_user(self):
        response = self.client.get(reverse("book-list"))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
