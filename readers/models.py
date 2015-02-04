from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save

from books.models import Edition
from readers.utils import slugify

from datetime import datetime


class GetOrNoneManager(models.Manager):
    """
    Adds get_or_none method to objects
    """
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class Reader(models.Model):
    user = models.OneToOneField(User)
    editions = models.ManyToManyField(Edition,
                                      through='Save')


def create_reader(sender, instance, created, **kwargs):
    if created:
        Reader.objects.get_or_create(user=instance)

post_save.connect(create_reader, sender=User)


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    def save(self, *args, **kwargs):
        self.slug = slugify._string_to_slug(self.name)
        return super(Tag, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Timeline(models.Model):
    start = models.DateTimeField(default=None, null=True)
    end = models.DateTimeField(default=None, null=True)
    read_instance = models.ForeignKey('Save',
                                      related_name='timelines',
                                      null=True,
                                      blank=True)


class Save(models.Model):
    reader = models.ForeignKey('Reader', related_name='saves')
    edition = models.ForeignKey(Edition)
    tags = models.ManyToManyField('Tag',
                                  related_name='books',
                                  null=True,
                                  blank=True)

    objects = GetOrNoneManager()

    def __unicode__(self):
        return "%s has saved book %s" % (self.reader.user.username, self.edition)

    def tags_list(self):
        # print 'tags' + self.tags.all()
        return [tag.name for tag in self.tags.all()]

    # def timelines_list(self):
    #     re
