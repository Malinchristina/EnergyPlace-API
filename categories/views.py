from rest_framework import generics
from rest_framework.response import Response
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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response(
                {"message": "No posts in this categories found."}, status=200)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CategoryDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve, update category.
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
