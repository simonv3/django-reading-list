from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'readinglist.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('books.urls')),
    url(r'^', include('readers.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^', include('core.urls', namespace='core')),
)
