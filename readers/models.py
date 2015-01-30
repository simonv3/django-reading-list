from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save

from books.models import Edition
from readers.utils import slugify

from datetime import datetime


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    def save(self, *args, **kwargs):
        self.slug = slugify._string_to_slug(args['name'])
        return super(Tag, self).save(*args, **kwargs)


class Timeline(models.Model):
    start = models.DateTimeField(default=datetime.now(), null=True)
    end = models.DateTimeField(default=None, null=True)


class UserReadBook(models.Model):
    user = models.OneToOneField(User)
    book = models.ForeignKey(Edition, related_name='read_by')
    tags = models.ManyToManyField('Tag', related_name='books')
    timelines = models.ForeignKey('Timeline', related_name='books')


def create_reader(sender, **kw):
    user = kw["instance"]
    if kw["created"]:
        reader = UserReadBook(user=user)
        reader.save()

post_save.connect(create_reader, sender=User)
