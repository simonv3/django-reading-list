# Based on https://djangosnippets.org/snippets/98/

import re
from django.db import models


class SlugNotCorrectlyPrePopulated(Exception):
    pass


def _string_to_slug(s):
    raw_data = s
    # normalze string as proposed on:
    # http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/251871
    # by Aaron Bentley, 2006/01/02
    try:
        import unicodedata
        raw_data = unicodedata.normalize('NFKD',
                                         raw_data.decode('utf-8', 'replace')
                                         ).encode('ascii', 'ignore')
    except:
        pass
    return re.sub(r'[^a-z0-9-]+', '-', raw_data.lower()).strip('_')


# as proposed by Archatas (http://www.djangosnippets.org/users/Archatas/)
def _get_unique_value(model,
                      proposal,
                      field_name="slug",
                      instance_pk=None,
                      separator="-"):
    """ Returns unique string by the proposed one.
    Optionally takes:
    * field name which can  be 'slug', 'username', 'invoice_number', etc.
    * the primary key of the instance to which the string will be assigned.
    * separator which can be '-', '_', ' ', '', etc.
    By default, for proposal 'example' returns strings from the sequence:
        'example', 'example-2', 'example-3', 'example-4', ...
    """
    if instance_pk:
        similar_ones = model.objects.filter(
            **{field_name + "__startswith": proposal}
        ).exclude(pk=instance_pk).values(field_name)
    else:
        similar_ones = model.objects.filter(
            **{field_name + "__startswith": proposal}
        ).values(field_name)
    similar_ones = [elem[field_name] for elem in similar_ones]
    if proposal not in similar_ones:
        return proposal
    else:
        numbers = []
        for value in similar_ones:
            match = re.match(r'^%s%s(\d+)$' % (proposal, separator), value)
            if match:
                numbers.append(int(match.group(1)))
        if len(numbers) == 0:
            return "%s%s2" % (proposal, separator)
        else:
            largest = sorted(numbers)[-1]
            return "%s%s%d" % (proposal, separator, largest + 1)


def _get_fields_and_data(model):
    opts = model._meta
    slug_fields = []
    for f in opts.fields:
        if isinstance(f, models.SlugField):
            if not f.prepopulate_from:
                raise SlugNotCorrectlyPrePopulated(
                    "Slug for %s is not prepopulated" % f.name
                )

            prepop = []
            for n in f.prepopulate_from:
                if not hasattr(model, n):
                    raise SlugNotCorrectlyPrePopulated(
                        "Slug for %s is to be prepopulated from %s, yet %s." +
                        "%s does not exist" % (f.name, n, type(model), n))
                else:
                    prepop.append(getattr(model, n))
            slug_fields.append([f, "_".join(prepop)])
    return slug_fields


def slugify(sender, instance, signal, *args, **kwargs):
    for slugs in _get_fields_and_data(instance):
        original_slug = _string_to_slug(slugs[1])
        slug = original_slug
        ct = 0
        try:
            # See if object is new
            # To prevent altering urls, don't update slug on existing objects
            sender.objects.get(pk=instance._get_pk_val())
        except:
            slug = _get_unique_value(instance.__class__,
                                     slug,
                                     slugs[0].name,
                                     separator="_")
            setattr(instance, slugs[0].name, slug)


# ===========================
# To attach it to your model:
# ===========================
#
# dispatcher.connect(_package_.slugify,
#                    signal=signals.pre_save,
#                    sender=_your_model_)
