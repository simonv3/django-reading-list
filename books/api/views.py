from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

try:
    from isbndb import utils as isbndb
except ImportError as e:
    isbndb_imported = False
    isbndb_imported_error = e
else:
    isbndb_imported = True
    from books.utils import process_isbndb_result

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


@api_view(['GET'])
def search_external(request, q):

    if isbndb_imported:
        result = isbndb.fetch_from_isbndb(q)
        pks = process_isbndb_result(result)
        books = Book.objects.filter(pk__in=pks)
        serialized = BookSerializer(
            books,
            many=True,
            context={'request': request}).data
        return Response(serialized)
        # return Response(BookSerializer(
        #     books
        # ).data)

    return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
