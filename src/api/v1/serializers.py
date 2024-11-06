# serializers.py
from cities_light.models import SubRegion, Region, Country
from rest_framework import serializers
from src.services.services.models import ServiceCategory, Service, ServiceImage, ServiceAvailability, ServiceReview, \
    ServiceRequest, ServiceCurrency, ServiceLocation
from src.services.users.models import User

""" ---------------------Helper Serializers--------------------- """


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']


class RegionSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = Region
        fields = ['id', 'name', 'country']


class SubRegionSerializer(serializers.ModelSerializer):
    region = RegionSerializer()

    class Meta:
        model = SubRegion
        fields = ['id', 'name', 'region']


class UserProfileSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile_image', 'phone_number', 'location']

    def get_location(self, obj):
        return obj.get_provider_location()


""" ---------------------Service Serializers--------------------- """


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'thumbnail', 'description', 'is_active']


class ServiceCurrentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCurrency
        fields = ['id', 'name']


class ServiceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceImage
        fields = ['id', 'image']


class ServiceAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceAvailability
        fields = ['id', 'day_of_week', 'start_time', 'end_time', 'timezone', 'is_active']


class ServiceLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceLocation
        fields = ['id', 'address', 'city', 'region', 'country']


class ServiceReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceReview
        fields = ['id', 'service', 'reviewer', 'rating', 'comment', 'created_at']


class ServiceHomeSerializer(serializers.ModelSerializer):
    provider = UserProfileSerializer()
    category = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    schedule = serializers.SerializerMethodField()
    currency = ServiceCurrency()

    class Meta:
        model = Service
        fields = ['id', 'title', 'thumbnail', 'provider', 'service_type', 'category', 'schedule', 'description',
                  'price_type', 'price', 'discount', 'currency', 'rating',
                  'is_active']

    def get_rating(self, obj):
        return obj.get_total_rating()

    def get_category(self, obj):
        return obj.category.name

    def get_schedule(self, obj):
        schedules = obj.get_service_schedule()
        data = []
        for schedule in schedules:
            data.append({
                'day_of_week': schedule.day_of_week,
                'start_time': schedule.start_time,
                'end_time': schedule.end_time,
                'timezone': schedule.timezone
            })
        return data


class ServiceHomeListSerializer(serializers.Serializer):
    top_categories = ServiceCategorySerializer(many=True)
    my_interest = ServiceHomeSerializer(many=True)
    popular_services = ServiceHomeSerializer(many=True)


class ServiceSerializer(serializers.ModelSerializer):
    provider = UserProfileSerializer()
    category = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    schedule = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ['id', 'title', 'provider', 'thumbnail', 'category', 'service_type', 'schedule', 'description',
                  'price_type', 'price', 'discount', 'currency', 'rating', 'is_active']

    def get_rating(self, obj):
        return obj.get_total_rating()

    def get_category(self, obj):
        return obj.category.name

    def get_schedule(self, obj):
        schedules = obj.get_service_schedule()
        data = []
        for schedule in schedules:
            data.append({
                'day_of_week': schedule.day_of_week,
                'start_time': schedule.start_time,
                'end_time': schedule.end_time,
                'timezone': schedule.timezone
            })
        return data


class ServiceCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['title', 'category', 'service_type', 'thumbnail', 'description', 'content', 'price_type', 'price',
                  'discount', 'currency', 'is_active']

    def validate_title(self, value):
        request = self.context.get("request")
        if Service.objects.filter(provider=request.user, title=value).exists():
            raise serializers.ValidationError("You already have a service with this title.")
        return value


class ServiceDetailSerializer(serializers.ModelSerializer):
    provider = UserProfileSerializer()
    images = ServiceImageSerializer(many=True, read_only=True)
    availability_slots = ServiceAvailabilitySerializer(many=True, read_only=True)
    reviews = ServiceReviewSerializer(many=True, read_only=True)
    currency = ServiceCurrency()

    class Meta:
        model = Service
        fields = [
            'id', 'title', 'provider', 'service_type', 'thumbnail', 'description', 'content', 'price_type', 'price',
            'discount', 'currency',
            'category', 'is_active', 'images', 'availability_slots', 'reviews'
        ]
