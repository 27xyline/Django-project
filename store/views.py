from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from store.models import Book
from store.serializers import BooksSerializer


def login_page(request: HttpRequest) -> HttpResponse:
    """Display the page that starts Google OAuth with a POST request."""
    return render(request, "store/login.html")


class BookViewSet(ModelViewSet):
    queryset = Book.objects.order_by("id")
    serializer_class = BooksSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    filterset_fields = ['price']
    search_fields = ['name', 'author']
    ordering_fields = ['price', 'author']

    permission_classes = [IsAuthenticated]
