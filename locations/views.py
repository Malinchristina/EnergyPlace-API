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
    filterset_fields = ['country']

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
    
