from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from geoposition.fields import GeopositionField


@python_2_unicode_compatible
class Location(models.Model):
    name = models.CharField(max_length=30)
    postion = GeopositionField()

    def __str__(self):
        return self.name
