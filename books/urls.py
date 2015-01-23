from django.conf.urls import patterns, include, url
from rest_framework import routers

from books.api import views as api_views
from books import views

router = routers.DefaultRouter()
router.register(r'book', api_views.CanonicalBookViewSet)
router.register(r'bookedition', api_views.BookEditionViewSet)
router.register(r'author', api_views.AuthorViewSet)
router.register(r'publisher', api_views.PublisherViewSet)

urlpatterns = patterns(
    '',
    url(r'^api/', include(router.urls)),
    url(r'^$', views.BookListView.as_view(), name='index'),
)
