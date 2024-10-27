from rest_framework import generics
from .models import Category
from .serializers import CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

class CategoryList(generics.ListCreateAPIView):
    """
    Category list view.
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']


class CategoryDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve, update category.
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
