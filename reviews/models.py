from django.db import models
from django.contrib.auth.models import User

from books.models import Book


class Review(models.Model):
    added_by = models.ForeignKey(User,
                                 null=True,
                                 blank=True,
                                 related_name='added')
    excerpt = models.TextField(blank=True)
    book = models.ForeignKey(Book,
                             related_name='reviews')
    source_url = models.URLField()
    source = models.ForeignKey('ReviewSource',
                               null=True,
                               blank=True,
                               related_name='reviewed_by')

    def __unicode__(self):
        return "Review for {0}".format(self.book)


class ReviewSource(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
