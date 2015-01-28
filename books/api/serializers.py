# from django.contrib.auth.models import User, Group
from rest_framework import serializers

from books.models import (Book, Author, Publisher, Edition,
                          BookExtra)


# ToDo: Define serializers for editions and extras
# that aren't defined by author.

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    # authored = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ('url', 'id', 'name', 'authored')
        extra_kwargs = {
            'url': {
                'view_name': 'author-detail',
                }
            }


class PublisherSerializer(serializers.HyperlinkedModelSerializer):
    # published = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Publisher
        fields = ('url', 'id', 'name', 'published')
        extra_kwargs = {
            'url': {
                'view_name': 'publisher-detail',
                }
            }


class NestedAuthorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Author
        fields = ('url', 'id', 'name')
        extra_kwargs = {
            'url': {
                'view_name': 'author-detail',
                }
            }


class NestedPublisherSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Publisher
        fields = ('url', 'id', 'name')
        extra_kwargs = {
            'url': {
                'view_name': 'publisher-detail',
                }
            }


class NestedExtraSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField('get_val')

    class Meta:
        model = BookExtra
        fields = ('id', 'key', 'value')

    def get_val(self, obj):
        return obj.get_value()


class EditionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Edition
        fields = ('url', 'id', 'book', 'edition_name', 'pub_date', 'extras')
        extra_kwargs = {
            'url': {
                'view_name': 'edition-detail'
                }
            }


class NestedEditionSerializer(serializers.HyperlinkedModelSerializer):
    extras = NestedExtraSerializer(many=True, read_only=True)
    publisher = NestedPublisherSerializer()
    editors = NestedAuthorSerializer(many=True)
    translators = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        many=True
    )

    class Meta:
        model = Edition
        fields = ('url', 'id', 'edition_name', 'pub_date', 'extras',
                  'publisher', 'editors', 'translators')
        extra_kwargs = {
            'url': {
                'view_name': 'edition-detail'
                }
            }


class BookSerializer(serializers.HyperlinkedModelSerializer):
    editions = NestedEditionSerializer(many=True, read_only=True)
    authors = NestedAuthorSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ('url', 'id', 'title', 'sub_title', 'authors', 'editions')
        extra_kwargs = {
            'url': {
                'view_name': 'book-detail',
                }
            }
