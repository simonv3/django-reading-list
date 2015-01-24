from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer

from books.api.serializers import (BookSerializer,
                                   EditionSerializer,
                                   AuthorSerializer,
                                   PublisherSerializer
                                   )
from books.models import Book, Author, Publisher, Edition


class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed or edited.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class EditionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows book editions to be viewed or edited.
    """
    queryset = Edition.objects.all()
    serializer_class = EditionSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows authors to be viewed or edited.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class PublisherViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows publishers to be viewed or edited.
    """
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
