from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from geoposition.fields import GeopositionField


@python_2_unicode_compatible
class Location(models.Model):
    country = models.CharField(max_length=20, default="")
    state = models.CharField(max_length=30, default="")
    city = models.CharField(max_length=20, default="")

    def __str__(self):
        return '{},{},{}'.format(self.country, self.state, self.city)


@python_2_unicode_compatible
class Photo(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    lat_lng = GeopositionField()
    file_path = models.CharField(max_length=200)
    file_path_real = models.CharField(max_length=240)
    width = models.IntegerField()
    height = models.IntegerField()
    date_time = models.DateTimeField()

    def __str__(self):
        return self.file_path
