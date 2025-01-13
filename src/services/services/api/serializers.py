from rest_framework import serializers
from src.services.services.models import ServiceCategory, Service, ServiceImage, ServiceAvailability, ServiceReview, \
    ServiceCurrency, ServiceLocation, FavoriteService
from src.services.users.models import User

""" ---------------------Helper Serializers--------------------- """


class UserProfileSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'profile_image', 'location']

    def get_location(self, obj):
        if obj.get_provider_location():
            return obj.get_provider_location()
        return None


""" ---------------------Service Serializers--------------------- """


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'thumbnail', 'description', 'is_active']
        ref_name = 'ServiceCategoryServices'


class ServiceCurrencySerializer(serializers.ModelSerializer):
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
    # Use SerializerMethodField to access related model fields
    city_name = serializers.SerializerMethodField()
    region_name = serializers.SerializerMethodField()
    country_name = serializers.SerializerMethodField()

    class Meta:
        model = ServiceLocation
        fields = ['id', 'address', 'city_name', 'region_name', 'country_name', 'latitude', 'longitude']

    def get_city_name(self, obj):
        return obj.city.name if obj.city else None

    def get_region_name(self, obj):
        return obj.region.name if obj.region else None

    def get_country_name(self, obj):
        return obj.country.name if obj.country else None


class ServiceReviewSerializer(serializers.ModelSerializer):
    reviewer = UserProfileSerializer(read_only=True)  # Make reviewer read-only

    class Meta:
        model = ServiceReview
        fields = ['id', 'service', 'reviewer', 'rating', 'comment', 'created_at']
        read_only_fields = ['service', 'reviewer', 'created_at']

    def validate(self, data):
        if data['rating'] < 1 or data['rating'] > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return data


class ServiceSerializer(serializers.ModelSerializer):
    provider = UserProfileSerializer()
    category = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    schedule = serializers.SerializerMethodField()
    images = ServiceImageSerializer(many=True, read_only=True)
    currency = ServiceCurrencySerializer()

    class Meta:
        model = Service
        fields = ['id', 'title', 'provider', 'images', 'thumbnail', 'category', 'service_type', 'schedule',
                  'description',
                  'price_type', 'price', 'discount', 'currency', 'rating', 'is_active']

    def get_rating(self, obj):
        return obj.get_total_rating()

    def get_category(self, obj):
        if obj.category:
            return obj.category.name
        return None

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


class ServiceDetailSerializer(serializers.ModelSerializer):
    provider = UserProfileSerializer()
    images = ServiceImageSerializer(many=True, read_only=True)
    category = ServiceCategorySerializer()
    availability_slots = ServiceAvailabilitySerializer(many=True, read_only=True)
    reviews = ServiceReviewSerializer(many=True, read_only=True)
    currency = ServiceCurrencySerializer()
    location = ServiceLocationSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = [
            'id', 'title', 'provider', 'service_type', 'thumbnail', 'description', 'content', 'price_type', 'price',
            'discount', 'currency', 'number_of_people',
            'category', 'is_active', 'images', 'availability_slots', 'location', 'reviews', 'created_at'
        ]


class ServiceCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'title', 'category', 'service_type', 'thumbnail', 'description', 'content', 'price_type',
                  'price', 'number_of_people',
                  'discount', 'currency', 'is_active']

    def validate_title(self, value):
        request = self.context.get("request")
        if Service.objects.filter(provider=request.user, title=value).exists():
            raise serializers.ValidationError("You already have a service with this title.")
        return value

