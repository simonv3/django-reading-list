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


class Reader(models.Model):
    user = models.OneToOneField(User)
    books = models.ForeignKey('BookEdition', related_name='reader')


# Register a reader when a user instance is created.
def create_reader(sender, **kw):
    user = kw["instance"]
    if kw["created"]:
        reader = Reader(user=user)
        reader.save()

post_save.connect(create_reader, sender=User)


class CanonicalBook(models.Model):
    title = models.CharField(max_length=200)
    sub_title = models.CharField(max_length=500)
    authors = models.ManyToManyField('Author',
                                     related_name='authored',
                                     null=True)

    def __unicode__(self):
        return self.title


class BookEdition(CanonicalBook):
    book = models.ForeignKey('CanonicalBook', related_name='editions')
    edition_name = models.CharField(max_length=100, null=True)
    publisher = models.ForeignKey('Publisher', related_name='published')
    pub_date = models.DateField()
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
    book = models.ForeignKey('BookEdition', related_name='extra')
    key = models.CharField(max_length=20)
    val_text = models.TextField(blank=True, null=True)
    val_char = models.CharField(max_length=200, null=True)
    val_bool = models.NullBooleanField(null=True)

    def __unicode__(self):
        return "%s: %s" % self.key, str(self.get_value())

    def get_value(self):
        if self.text:
            return text
        elif self.char:
            return char
        elif self.boolean:
            return boolean

    def save(self, *args, **kwargs):
        """
        Override the save method to make sure that only one of the 'value'
        fields (text, char, boolean) get written to.
        Return an error if this is the case.
        If everything is okay, pass on to the super save method.
        """
        been_set = 0
        if self.text:
            been_set += 1
        elif self.char:
            been_set += 1
        elif not boolean is True or not boolean is False:
            been_set += 1

        if been_set is 1:
            return super(BookExtra, self).save(*args, **kwargs)
        else:
            return


class Author(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name
