from django.conf.urls import patterns, include, url
from rest_framework import routers
from rest_framework_extensions.routers import ExtendedSimpleRouter

from books.api import views as api_views
from books import views

router = ExtendedSimpleRouter()
router.register(r'books', api_views.BookViewSet)\
    # .register(r'editions',
    #           api_views.BookEditionViewSet,
    #           base_name='bookedition',
    #           parents_query_lookups=['book_id']
    #           )
# router.register(r'bookedition', api_views.BookEditionViewSet)
router.register(r'authors', api_views.AuthorViewSet)
router.register(r'publishers', api_views.PublisherViewSet)

urlpatterns = patterns(
    '',
    url(r'^api/', include(router.urls)),
    # url(r'^$', views.BookListView.as_view(), name='index'),
)
