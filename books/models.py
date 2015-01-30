from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class GetOrNoneManager(models.Manager):
    """
    Adds get_or_none method to objects
    """
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class Book(models.Model):
    title = models.CharField(max_length=200)
    sub_title = models.CharField(max_length=500)
    authors = models.ManyToManyField('Author',
                                     related_name='authored',
                                     null=True)

    objects = GetOrNoneManager()

    def __unicode__(self):
        return self.title


class Edition(models.Model):
    book = models.ForeignKey('Book', related_name='editions')
    edition_name = models.CharField(max_length=100, null=True)
    publisher = models.ForeignKey('Publisher', related_name='published')
    pub_date = models.DateField(null=True, blank=True)
    editors = models.ManyToManyField('Author',
                                     related_name='edited',
                                     null=True,
                                     blank=True)
    translators = models.ManyToManyField('Author',
                                         related_name='translated',
                                         null=True,
                                         blank=True)

    def __unicode__(self):
        return "%s %s" % self.book.title, self.edition_name

    def get_key(self, key):
        return self.get(key, self.book.get(key))


class BookExtra(models.Model):
    book = models.ForeignKey('Edition', related_name='extras')
    key = models.CharField(max_length=20)
    val_text = models.TextField(blank=True, null=True)
    val_char = models.CharField(max_length=200, null=True)
    val_bool = models.NullBooleanField(null=True)

    def __unicode__(self):
        return "%s: %s" % self.key, str(self.get_value())

    def get_value(self):
        if self.val_text:
            return self.val_text
        elif self.val_char:
            return self.val_char
        elif self.val_bool:
            return self.val_bool

    def save(self, *args, **kwargs):
        """
        Override the save method to make sure that only one of the 'value'
        fields (text, char, boolean) get written to.
        Return an error if this is the case.
        If everything is okay, pass on to the super save method.
        """
        been_set = 0
        if self.val_text:
            been_set += 1
        elif self.val_char:
            been_set += 1
        # TODO include a test for boolean

        if been_set is 1:
            return super(BookExtra, self).save(*args, **kwargs)
        else:
            return


class Author(models.Model):
    # Stored by how the author writes it.

    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name
