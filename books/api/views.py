from rest_framework import viewsets

from books.api.serializers import (CanonicalBookSerializer,
                                   EditionSerializer,
                                   AuthorSerializer,
                                   PublisherSerializer
                                   )
from books.models import CanonicalBook, Author, Publisher, BookEdition


class CanonicalBookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed or edited.
    """
    queryset = CanonicalBook.objects.all()
    serializer_class = CanonicalBookSerializer


class BookEditionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows book editions to be viewed or edited.
    """
    queryset = BookEdition.objects.all()
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
