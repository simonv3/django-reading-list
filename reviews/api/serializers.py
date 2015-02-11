from django.contrib.auth.models import User
from rest_framework import serializers

from reviews.models import Review
from books.api.serializers import BookSerializer


class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    book = BookSerializer()

    class Meta:
        model = Review
        fields = ('href', 'id', 'book', 'excerpt', 'source_url')
