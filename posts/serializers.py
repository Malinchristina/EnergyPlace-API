from rest_framework import serializers
from .models import Post
from locations.models import Location
from categories.models import Category
from likes.models import Like
from locations.serializers import LocationSerializer
from categories.serializers import CategorySerializer


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    
    # Display full location and category details
    location = LocationSerializer(read_only=True)
    locality = serializers.CharField(write_only=True, required=True)
    category = CategorySerializer(read_only=True) 

     # For filtering and setting location and category
    location_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), source='location', write_only=True
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    like_id = serializers.SerializerMethodField()
    comments_count = serializers.ReadOnlyField()
    likes_count = serializers.ReadOnlyField()
    

    def validate_image(self, value):
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError('Image size too large.')
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width larger than 4096px.'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px.'
            )
        return value

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return request.user == obj.owner
    
    #   #Create location and category fields
    def create(self, validated_data):
        location_instance = validated_data.pop('location', None)
        locality = validated_data.pop('locality', None)
        category_instance = validated_data.pop('category', None)
        
        if location_instance:
            location_instance.locality = locality
            location_instance.save()

        post = Post.objects.create(
            category=category_instance,
            location=location_instance,
            **validated_data
        )
        return post

    # Update location and category fields
    def update(self, instance, validated_data):
        locality = validated_data.pop('locality', None)
        location_instance = validated_data.pop('location', None)
        category_instance = validated_data.pop('category', None)

        if location_instance:
            if locality:
                location_instance.locality = locality
                location_instance.save()
            instance.location = location_instance

        if category_instance:
            instance.category = category_instance

        updated_instance = super().update(instance, validated_data)
        instance.refresh_from_db()
        return updated_instance

    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(
                owner=user, post=obj
            ).first()
            return like.id if like else None
        return None

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'title', 'image', 'content', 'created_at', 'updated_at',
            'like_id', 'comments_count', 'likes_count',
            'category', 'category_id', 'location', 'location_id', 'locality',
        ]

    