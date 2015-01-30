from django.conf.urls import patterns, include, url
from rest_framework import routers

from reader.api import views as api_views
from reader import views

router = routers.DefaultRouter()

# TODO: Nest API endpoints
# from rest_framework_extensions.routers import ExtendedSimpleRouter

router.register(r'readers', api_views.ReaderViewSet)

urlpatterns = patterns(
    '',
    url(r'^api/', include(router.urls)),
)
