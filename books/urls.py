from django.conf.urls import patterns, include, url
from rest_framework import routers

from books.api import views as api_views
from books import views

router = routers.DefaultRouter()

# TODO: Nest API endpoints
# # from rest_framework_extensions.routers import ExtendedSimpleRouter

router.register(r'books', api_views.BookViewSet)
router.register(r'editions', api_views.EditionViewSet)
router.register(r'authors', api_views.AuthorViewSet)
router.register(r'publishers', api_views.PublisherViewSet)

urlpatterns = patterns(
    '',
    url(r'^api/search/external/(?P<q>[\w ]+)/$', api_views.search_external),
    url(r'^api/', include(router.urls)),
)
