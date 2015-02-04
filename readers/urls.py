from django.conf.urls import patterns, include, url
from rest_framework import routers
from rest_framework_extensions.routers import ExtendedSimpleRouter

from readers.api import views as api_views
from readers import views


router = routers.DefaultRouter()

router.register(r'saves', api_views.SaveViewSet)
router.register(r'readers', api_views.ReaderViewSet)
router.register(r'timelines', api_views.TimelineViewSet)
router.register(r'tags', api_views.TagViewSet)

urlpatterns = patterns(
    '',
    url(r'^api/', include(router.urls)),
)
