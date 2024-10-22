from rest_framework import generics
from .models import Category
from .serializers import CategorySerializer

# Create your views here.

class CategoryList(generics.ListCreateAPIView):
    """
    Category list view.
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve, update category.
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
