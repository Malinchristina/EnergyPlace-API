from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_countries import countries


from rest_framework import generics
from rest_framework.response import Response
from .models import Location
from .serializers import LocationSerializer
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

class LocationList(generics.ListCreateAPIView):
    """
    Location list view.
    """
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['country',]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response(
                {"message": "No posts in this country."}, status=200)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)


class LocationDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve, update location.
    """
    serializer_class = LocationSerializer
    queryset = Location.objects.all()


@api_view(['GET'])
def full_country_list(request):
    """
    View to return the full list of countries with unique IDs.
    """
    full_country_list = [
        {"id": index + 1, "code": code, "name": name} 
        for index, (code, name) in enumerate(countries)
    ]
    return Response(full_country_list)
    

@api_view(['GET'])
def country_list(request):
    """
    View to return a list of countries with existing posts.
    """
    # Get unique country codes from locations in the database
    existing_countries = (
        Location.objects.filter(post__isnull=False)  # Only locations with associated posts
        .values_list('country', flat=True)
        .distinct()
    )
    
    # Filter the full list of countries to include 
    # only those in existing_countries
    country_list = [
        {"code": code, "name": name} 
        for code, name in countries 
        if code in existing_countries
    ]
 
    return Response(country_list)
