# serializers.py
from rest_framework import serializers
from src.services.services.models import ServiceCategory, Service, ServiceImage, ServiceAvailability, ServiceReview, \
    ServiceRequest
from src.services.users.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile_image', 'phone_number']


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id','name', 'thumbnail', 'description', 'is_active']


class ServiceHomeSerializer(serializers.ModelSerializer):
    provider = UserProfileSerializer()

    class Meta:
        model = Service
        fields = ['id','title', 'provider', 'thumbnail', 'description', 'price', 'discount', 'category', 'is_active']


class ServiceHomeListSerializer(serializers.Serializer):
    top_services = ServiceHomeSerializer(many=True)
    new_services = ServiceHomeSerializer(many=True)
    top_categories = ServiceCategorySerializer(many=True)


class ServiceSerializer(serializers.ModelSerializer):
    provider = UserProfileSerializer()

    class Meta:
        model = Service
        fields = ['id','title', 'provider', 'thumbnail', 'description', 'content', 'price', 'discount', 'category',
                  'is_active']


class ServiceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceImage
        fields = ['id', 'image']


class ServiceAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceAvailability
        fields = ['id', 'day_of_week', 'start_time', 'end_time', 'timezone', 'is_active']


class ServiceReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceReview
        fields = ['id', 'service', 'reviewer', 'rating', 'comment', 'created_at']


class ServiceDetailSerializer(serializers.ModelSerializer):
    provider = UserProfileSerializer()
    images = ServiceImageSerializer(many=True, read_only=True)  # Removed the source argument
    availability_slots = ServiceAvailabilitySerializer(many=True, read_only=True)
    reviews = ServiceReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = [
            'id','title', 'provider', 'thumbnail', 'description', 'content', 'price', 'discount',
            'category', 'is_active', 'images', 'availability_slots', 'reviews'
        ]
