# from django.contrib.auth.models import User, Group
from rest_framework import serializers

from books.models import (CanonicalBook, Author, Publisher, BookEdition,
                          BookExtra)


class ExtraSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    book = serializers.PrimaryKeyRelatedField(
        queryset=BookEdition.objects.all()
    )

    class Meta:
        model = BookExtra
        fields = ('book', 'key', 'value')

    def get_value(self, obj):
        return obj.get_value()


class EditionSerializer(serializers.HyperlinkedModelSerializer):
    book = serializers.PrimaryKeyRelatedField(
        queryset=CanonicalBook.objects.all()
    )
    extras = ExtraSerializer(many=True, read_only=True)
    publisher = serializers.PrimaryKeyRelatedField(
        queryset=Publisher.objects.all(),
    )
    editors = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        many=True
    )
    translators = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        many=True
    )

    class Meta:
        model = BookEdition
        fields = ('url', 'id', 'book', 'edition_name', 'pub_date', 'extras',
                  'publisher', 'editors', 'translators')
        extra_kwargs = {
            'url': {
                'view_name': 'books:bookedition-detail',
                }
            }


class CanonicalBookSerializer(serializers.HyperlinkedModelSerializer):
    editions = EditionSerializer(many=True)
    authors = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Author.objects.all()
    )

    class Meta:
        model = CanonicalBook
        fields = ('url', 'id', 'title', 'sub_title', 'authors', 'editions')
        extra_kwargs = {
            'url': {
                'view_name': 'books:canonicalbook-detail',
                }
            }


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    authored = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ('url', 'id', 'name', 'authored')
        extra_kwargs = {
            'url': {
                'view_name': 'books:author-detail',
                }
            }


class PublisherSerializer(serializers.HyperlinkedModelSerializer):
    published = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Publisher
        fields = ('url', 'id', 'name', 'published')
        extra_kwargs = {
            'url': {
                'view_name': 'books:publisher-detail',
                }
            }
