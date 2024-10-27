from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer

# Create your views here.

class CommentList(generics.ListCreateAPIView):
    """
    List and create view for Comment model.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Edit and delete view for Comment model.
    """
    serializer_class = CommentDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Comment.objects.all()