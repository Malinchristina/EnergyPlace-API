from rest_framework import generics
from .models import Location
from .serializers import LocationSerializer

# Create your views here.

class LocationList(generics.ListCreateAPIView):
    """
    Location list view.
    """
    serializer_class = LocationSerializer
    queryset = Location.objects.all()


class LocationDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve, update location.
    """
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
    
