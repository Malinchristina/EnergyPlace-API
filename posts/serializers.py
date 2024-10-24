from rest_framework import serializers
from .models import Post
from locations.models import Location
from categories.models import Category
from locations.serializers import LocationSerializer
from categories.serializers import CategorySerializer


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    location = LocationSerializer()
    category = serializers.ChoiceField(choices=Category.CATEGORY_CHOICES)

    # category = CategorySerializer()
    # add likes and comments fields

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

    def create(self, validated_data):
        # Handle location creation manually
        location_data = validated_data.pop('location')
        category_data= validated_data.pop('category')

        location, created = Location.objects.get_or_create(**location_data)
        category, _ = Category.objects.get_or_create(name=category_data)
        
        post = Post.objects.create(
            location=location, category=category, **validated_data
        )
        return post

    def update(self, instance, validated_data):
        location_data = validated_data.pop('location', None)
        if location_data:
            Location.objects.filter(
                id=instance.location.id).update(**location_data)

        category_data = validated_data.pop('category', None)
        if category_data:
            Category.objects.filter(
                id=instance.category.id).update(**category_data)

        # Refresh instance to ensure it reflects 
        # updated related fields if necessary
        instance.refresh_from_db()
        return super().update(instance, validated_data)


    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'title', 'image', 'content', 'created_at', 'updated_at',
            'location', 'category', # 'likes',# 'comments', 
        ]

    