# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Cities(models.Model):
    city_name = models.CharField(max_length=200)
    url = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.city_name



class Precipitation(models.Model):
    precipitation = models.CharField(max_length=255)

    def __str__(self):
        return self.precipitation


class Wind(models.Model):
    wind_short_name = models.CharField(max_length=255)
    wind_full_name = models.CharField(max_length=255)


class Weather(models.Model):
    date = models.DateField(db_index=True)
    time = models.TimeField()
    city = models.ForeignKey(Cities, models.CASCADE)
    temperature = models.FloatField(blank=True, null=True)
    wind_direction = models.ForeignKey(Wind, models.SET_NULL, blank=True, null=True)
    wind_speed = models.FloatField(blank=True, null=True)
    precipitation_mm = models.FloatField(blank=True, null=True)
    precipitation = models.ForeignKey(Precipitation, models.SET_NULL, blank=True, null=True)
