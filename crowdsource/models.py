from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from crowdsource.managers import CrowdSourcedEntryManager

class CrowdSourcedObject(models.Model):
    name = models.CharField(max_length = 100, verbose_name = u'The name of the object type we\'re defining', unique = True)
    slug = models.SlugField(max_length = 100, verbose_name = u'Slug for the name', unique = True)
    icon = models.CharField(max_length=200, verbose_name = u'Icon for this Object', blank = True)
    help_text = models.CharField(max_length = 200, verbose_name = u'Help Text for this object type')

    def __unicode__(self):
        return self.name

class CrowdSourcedEntry(models.Model):
    csobj = models.ForeignKey(CrowdSourcedObject, verbose_name = u'Entry for CrowdSourcedObject')
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField()
    related_object = generic.GenericForeignKey()
    url = models.URLField(verbose_name = u'The url for this entry')
    verified = models.BooleanField()

    objects = CrowdSourcedEntryManager()

    def __unicode__(self):
        return "CrowdSource Entry for %s for object %s is %s. Verification Status: %s" % (self.csobj, self.related_object, self.url, unicode(self.verified))

