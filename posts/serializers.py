from rest_framework import serializers
from .models import Post
# from locations.models import Location
from categories.models import Category
from likes.models import Like
# from locations.serializers import LocationSerializer
from categories.serializers import CategorySerializer


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    # Revisit after core funtions are working
    # location = LocationSerializer()
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )
    like_id = serializers.SerializerMethodField()
    comments_count = serializers.ReadOnlyField()
    likes_count = serializers.ReadOnlyField()
    

    def validate_image(self, value):
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError('Image size too large.')
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width largern than 4096px.'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px.'
            )
        return value

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return request.user == obj.owner
    # Revisit after core functions are working
    #   #Create location and category fields
    def create(self, validated_data):
        # Handle location creation manually
        # location_data = validated_data.pop('location')
        category_data= validated_data.pop('category')

        # location, created = Location.objects.get_or_create(**location_data)
        category, _ = Category.objects.get_or_create(name=category_data)

        post = Post.objects.create(
            category=category, **validated_data #location=location, 
        )
        return post

    # Update location and category fields
    # def update(self, instance, validated_data):
    #     location_data = validated_data.pop('location', None)
    #     if location_data:
    #         if instance.location:
    #             # Update the existing location
    #             Location.objects.filter(id=instance.location.id).update(**location_data)
    #         else:
    #             # Create a new location if there is no existing one
    #             instance.location = Location.objects.create(**location_data)
    #     else:
    #         # Handle the case where no location data is provided
    #         raise serializers.ValidationError("Location data is required.")

        category_data = validated_data.pop('category', None)
        if category_data:
            category, created = Category.objects.get_or_create(name=category_data)
            instance.category = category

        # Save and update
        instance.save()
        instance.refresh_from_db()

        updated_instance = super().update(instance, validated_data)
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
            'category', #'location',
        ]

    