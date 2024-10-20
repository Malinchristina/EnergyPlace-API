from django.db import models
from django_countries.fields import CountryField

# Create your models here.

class Location(models.Model):
    """
    Location model. Name is specific location name (e.g., city or landmark). 
    """
    name = models.CharField(max_length=100)
    country = CountryField()

    def __str__(self):
        return f'{self.name}, {self.country.name}'
