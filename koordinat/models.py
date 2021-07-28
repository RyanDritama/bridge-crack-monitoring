from django.db import models
from django.contrib.postgres import fields

class Koordinat(models.Model):
    segmen = models.IntegerField(null=True, blank=True)
    longitude = models.FloatField()
    lat = models.FloatField()
    alt = models.FloatField()
# Create your models here.
