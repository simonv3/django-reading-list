from django.conf.urls import patterns, include, url
from rest_framework import routers

from reviews.api import views as api_views
from reviews import views

router = routers.DefaultRouter()

# TODO: Nest API endpoints
# # from rest_framework_extensions.routers import ExtendedSimpleRouter

router.register(r'reviews', api_views.ReviewViewSet)

urlpatterns = patterns(
    '',
    url(r'^api/', include(router.urls)),
)
