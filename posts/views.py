from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer
from rest_framework.pagination import LimitOffsetPagination

# Create your views here.

class TopFivePagination(LimitOffsetPagination):
    default_limit = 5  # Only return 5 posts by default
    max_limit = 5  # Ensure the max limit is 5

class PostList(generics.ListCreateAPIView):
    """
    List and create view for Post model.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True)
    )
    # .order_by('-likes_count', '-created_at')
    # pagination_class = TopFivePagination

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
        'categories',
        'location__locality',
        'location__country',
    ]
    ordering_fields = [
        'comments_count',
        'likes_count',
    ]

    pagination_class = None  # Default: no pagination

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('top_liked') == 'true':
            # Filter to include only posts with likes_count > 0
            queryset = queryset.filter(likes_count__gt=0)
            # Limit the queryset to the top 5 posts based on
            # likes_count and created_at
            return queryset.order_by('-likes_count', '-created_at')[:5]
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


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
