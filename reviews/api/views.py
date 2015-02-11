from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view, detail_route, list_route
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

import django_filters

from reviews.api.serializers import ReviewSerializer

from reviews.models import Review


class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed or edited.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        queryset = Review.objects.all()
        book_id = self.request.QUERY_PARAMS.get('book_id', None)
        if book_id is not None:
            queryset = queryset.filter(book__pk=book_id)
        return queryset
