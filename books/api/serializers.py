# from django.contrib.auth.models import User, Group
from rest_framework import serializers

from books.models import (Book, Author, Publisher, Edition,
                          BookExtra)


class ExtraSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField('get_value')
    book = serializers.PrimaryKeyRelatedField(
        queryset=Edition.objects.all()
    )

    class Meta:
        model = BookExtra
        fields = ('book', 'key', 'value')

    def get_value(self, obj):
        return obj.get_value()


class EditionSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all()
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
        model = Edition
        fields = ('href', 'id', 'book', 'edition_name', 'pub_date', 'extras',
                  'publisher', 'editors', 'translators')
        extra_kwargs = {
            'href': {
                'view_name': 'books:books-editions-detail'
                }
            }


class BookSerializer(serializers.HyperlinkedModelSerializer):
    # editions = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='books:Edition-detail'
    # )
    editions = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Edition.objects.all()
    )
    authors = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Author.objects.all()
    )

    class Meta:
        model = Book
        fields = ('href', 'id', 'title', 'sub_title', 'authors', 'editions')
        extra_kwargs = {
            'href': {
                'view_name': 'books:book-detail',
                }
            }


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    authored = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ('href', 'id', 'name', 'authored')
        extra_kwargs = {
            'href': {
                'view_name': 'books:author-detail',
                }
            }


class PublisherSerializer(serializers.HyperlinkedModelSerializer):
    published = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Publisher
        fields = ('href', 'id', 'name', 'published')
        extra_kwargs = {
            'href': {
                'view_name': 'books:publisher-detail',
                }
            }
