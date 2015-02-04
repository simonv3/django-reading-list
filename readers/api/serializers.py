from django.contrib.auth.models import User
from rest_framework import serializers

from readers.models import (Save, Tag, Timeline, Reader)
from books.models import Edition
from books.api.serializers import EditionSerializer

import itertools


class TagSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class TimelineSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Timeline
        fields = ('href', 'id', 'start', 'end')


class SaveSerializer(serializers.HyperlinkedModelSerializer):
    edition = EditionSerializer()
    tags = TagSerializer(many=True)
    timelines = TimelineSerializer(many=True)

    class Meta:
        model = Save
        fields = ('href', 'id', 'edition', 'tags', 'timelines')


class NestedSaveSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Save
        fields = ('href', 'id', 'edition', 'tags', 'timelines')


class ReaderSerializer(serializers.HyperlinkedModelSerializer):
    # saves = NestedSaveSerializer(many=True)
    saves = serializers.SerializerMethodField()

    class Meta:
        model = Reader
        fields = ('href', 'id', 'saves')

    def get_saves(self, obj):
        saves = Save.objects.all()
        tags_filter = self.context['request'].query_params.get('tags', None)
        if tags_filter:
            saves = saves.filter(tags__slug=tags_filter)
        return NestedSaveSerializer(saves,
                                    context={'request': self.context['request']},
                                    many=True).data
