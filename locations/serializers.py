from rest_framework import serializers
from .models import Location
from django_countries.serializer_fields import CountryField


class LocationSerializer(serializers.ModelSerializer):
    """
    Location serializer, references Location model.
    """
    country_name = serializers.SerializerMethodField()

    def get_country_name(self, obj):
        return obj.country.name

    class Meta:
        model = Location
        fields = ['id', 'locality', 'country', 'country_name']

