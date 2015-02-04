from rest_framework import serializers

from books.models import (Book, Author, Publisher, Edition,
                          BookExtra)


# ToDo: Define serializers for editions and extras
# that aren't defined by author.

class AuthorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Author
        fields = ('href', 'id', 'name', 'authored')


class PublisherSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Publisher
        fields = ('href', 'id', 'name', 'published')


class NestedAuthorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Author
        fields = ('href', 'id', 'name')


class NestedPublisherSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Publisher
        fields = ('href', 'id', 'name')


class NestedExtraSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField('get_val')

    class Meta:
        model = BookExtra
        fields = ('id', 'key', 'value')

    def get_val(self, obj):
        return obj.get_value()


class NestedEditionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Edition
        fields = ('href', 'id', 'book', 'edition_name', 'pub_date', 'title')


class EditionSerializer(serializers.HyperlinkedModelSerializer):
    extras = NestedExtraSerializer(many=True, read_only=True)
    publisher = NestedPublisherSerializer()
    editors = NestedAuthorSerializer(many=True)
    translators = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        many=True
    )
    authors = NestedAuthorSerializer(many=True)

    class Meta:
        model = Edition
        fields = ('href', 'id', 'edition_name', 'pub_date', 'extras',
                  'publisher', 'editors', 'translators', 'title', 'authors')


class BookSerializer(serializers.HyperlinkedModelSerializer):
    editions = EditionSerializer(many=True, read_only=True)
    authors = NestedAuthorSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ('href', 'id', 'title', 'sub_title', 'authors', 'editions')
