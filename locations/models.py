from django.db import models
from django_countries.fields import CountryField

# Create your models here.

class Location(models.Model):
    """
    Location model. Locality is specific location name (e.g., city or landmark). 
    """
    locality = models.CharField(max_length=100)
    country = CountryField() # Country code e.g. SE

    class Meta:
        unique_together = ('locality', 'country')

    @property
    def country_name(self):
        return self.country.name #Get full country name e.g. Sweden

    def __str__(self):
        # Return only the country name for dropdowns or displays
        return f"{self.country.name}"
