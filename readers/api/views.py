from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view, detail_route, list_route
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

import django_filters

from readers.api.serializers import (SaveSerializer,
                                     ReaderSerializer,
                                     TimelineSerializer,
                                     TagSerializer)
from readers.models import Save, Timeline, Reader, Tag
from books.models import Edition


class SaveViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows read instances to be viewed or edited.
    """
    model = Save
    queryset = Save.objects.all()
    serializer_class = SaveSerializer

    def create(self, request):
        edition_id = request.data.get('edition', None)
        reader_id = request.data.get('reader', None)

        if edition_id and reader_id:
            edition = Edition.objects.get(pk=edition_id)
            reader = Reader.objects.get(pk=reader_id)

            if reader == request.user.reader:
                tag_slugs = request.data.get('tags', None)
                tags = []
                for tag_slug in tag_slugs:
                    tags.append(Tag.objects.get_or_create(slug=tag_slug)[0])
                print tags
                saved, created = Save.objects.get_or_create(edition=edition,
                                                            reader=reader)
                saved.tags = tags
                saved.save()

                return Response(SaveSerializer(saved,
                                               context={'request': request}
                                               ).data)
        return Response({
            'edition': 'Required',
            'reader': 'Required'
        }, status=status.HTTP_400_BAD_REQUEST)


class ReaderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed or edited.
    """
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer


class TimelineViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed or edited.
    """
    queryset = Timeline.objects.all()
    serializer_class = TimelineSerializer


class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed or edited.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
