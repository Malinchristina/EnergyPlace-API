from rest_framework import serializers
from .models import Location
from django_countries.serializer_fields import CountryField


class LocationSerializer(serializers.ModelSerializer):
    """
    Location serializer, references Location model.
    """

    country = CountryField()

    class Meta:
        model = Location
        fields = ['id', 'name', 'country']

