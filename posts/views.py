from django.db.models import Count
from rest_framework import generics, permissions, filters, serializers
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Post
from locations.models import Location
from .serializers import PostSerializer
from rest_framework.pagination import LimitOffsetPagination

# Create your views here.


class TopFivePagination(LimitOffsetPagination):
    """
    Custom pagination class for limiting posts to 5 by default.
    """
    default_limit = 5  # Only return 5 posts by default
    max_limit = 5  # Ensure the max limit is 5


class PostList(generics.ListCreateAPIView):
    """
    List and create view for Post model.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = TopFivePagination
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True)
    ).order_by('-created_at', '-likes_count')

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend
    ]
    filterset_fields = [
        'owner__followed__owner__profile',
        'likes__owner__profile',
        'owner__profile',
        'category',
        'location',
    ]
    search_fields = [
        'title',
        'owner__username',
        'category__name',
        'location__locality',
        'location__country',
    ]
    ordering_fields = [
        'comments_count',
        'likes_count',
    ]

    def perform_create(self, serializer):
        location_id = self.request.data.get('location_id')
        locality = self.request.data.get('locality')

        if not location_id:
            raise serializers.ValidationError({
                'location_id': 'This field is required.'})
        if not locality:
            raise serializers.ValidationError({
                'locality': 'This field is required.'})

        location_instance = Location.objects.get(id=location_id)

        # Save the post with the location and locality
        serializer.save(
            owner=self.request.user,
            location=location_instance,
            locality=locality,
        )

    def create(self, request, *args, **kwargs):
        """
        Override the create method to include a success message.
        """
        response = super().create(request, *args, **kwargs)
        response.data['detail'] = "Post created successfully."
        return response


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve posts, edit and delete view for Post model as owner.
    """
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True)
    ).order_by('-created_at')

    def delete(self, request, *args, **kwargs):
        """
        Override the delete method to include a success message.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Post deleted successfully."}, status=200)
