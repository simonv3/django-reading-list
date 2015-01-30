from django.contrib.auth.models import User, Group
from rest_framework import serializers

from readers.models import (Reader, Tag, Timeline)


class UserReadBookSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Reader
        fields = ('url', 'user', 'book', 'tags', 'timelines')
        extra_kwargs = {
            'url': {
                'view_name': 'reader-detail',
                }
            }


class TagSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tag
        fields = ('url', 'name', 'slug')
        extra_kwargs = {
            'url': {
                'view_name': 'tag-detail',
                }
            }


class NestedTimelineSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Timeline
        fields = ('url', 'start', 'end')
        extra_kwargs = {
            'url': {
                'view_name': 'timeline-detail',
                }
            }
