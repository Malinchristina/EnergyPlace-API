from django.db import models
from django_countries.fields import CountryField

# Create your models here.


class Location(models.Model):
    """
    Location model stores country
    """
    country = CountryField()  # Country code e.g. SE

    @property
    def country_name(self):
        return self.country.name  # Get full country name e.g. Sweden

    def __str__(self):
        # Display country name
        return self.country.name
