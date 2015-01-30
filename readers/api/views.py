from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from readers.api.serializers import (UserReadBookSerializer)
from readers.models import UserReadBook


class ReaderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed or edited.
    """
    queryset = UserReadBook.objects.all()
    serializer_class = UserReadBookSerializer
