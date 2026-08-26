from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BooksSerializer


class BooksApiTestCase(APITestCase):
    def test_get(self,):
        book_1 = Book.objects.create(name='Test book 1', price=1125, author="Пидар 1")
        book_2 = Book.objects.create(name='Test book 2', price=2225, author="Пидар 2")

        url = reverse("book-list")
        response = self.client.get(url)
        serializer_data = BooksSerializer([book_1, book_2], many=True).data
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)
