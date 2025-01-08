from rest_framework import serializers

from src.api.v1.serializers import LanguageSerializer
from src.core.models import Language
from src.services.services.api.serializers import ServiceSerializer
from src.services.services.models import FavoriteService
from src.services.users.models import UserImage, Address, Interest, Certification, SocialMedia, User, ServiceProvider, \
    ServiceProviderLanguage, UserContact


# """ ---------------------User Serializers--------------------- """
class UserSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile_image', 'bio', 'images', 'date_joined',
                  'last_login', ]
        read_only_fields = ['username', 'email', 'date_joined', 'images', 'last_login']

    def get_images(self, obj):
        images = obj.images.all()
        return UserImageSerializer(images, many=True).data


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profile_image', 'bio', ]


class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = ['id', 'image']


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'user', 'address', 'city', 'region', 'country', 'zip_code', ]
        read_only_fields = ['user']


# """ ---------------------Service Provider Interest  Serializers--------------------- """
class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'name']


# """ ---------------------Service Provider Language Serializers--------------------- """
class ServiceProviderLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProviderLanguage
        fields = ['id', 'language', 'fluency']


class ServiceProviderLanguageDetailSerializer(ServiceProviderLanguageSerializer):
    language = LanguageSerializer()

    class Meta(ServiceProviderLanguageSerializer.Meta):
        pass


# """ ---------------------Service Provider Certificate Serializers--------------------- """

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = ['id', 'certificate_file', ]


# """ ---------------------Service Provider Social Media Serializers--------------------- """
class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = ['id', 'facebook', 'instagram', 'twitter', 'linkedin', ]


# """ ---------------------Service Provider Serializers--------------------- """

class ServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProvider
        fields = ['id', 'company_name', 'phone_number', 'website']


class ServiceProviderDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    social_media = SocialMediaSerializer()
    interests = InterestSerializer(many=True)
    certifications = CertificationSerializer(many=True)
    languages = ServiceProviderLanguageDetailSerializer(many=True)
    address = UserAddressSerializer(source="user.address")

    class Meta:
        model = ServiceProvider
        fields = ['id', 'user', 'address', 'company_name', 'phone_number', 'website', 'rating', 'total_reviews',
                  'verified', 'status', 'social_media', 'interests', 'certifications', 'languages']
        read_only_fields = ['user', 'social_media', 'interests', 'certifications', 'address', 'rating', 'total_reviews',
                            'verified', 'status', ]


# """ ---------------------Favorite Service Serializers--------------------- """
class FavoriteServiceSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()

    class Meta:
        model = FavoriteService
        fields = ['id', 'user', 'service']


class FavoriteServiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteService
        fields = ['id', 'service']

    def validate(self, attrs):
        if FavoriteService.objects.filter(user=self.context['request'].user, service=attrs['service']).exists():
            raise serializers.ValidationError("Service already added to favorites")
        return attrs


# """ ---------------------User Contact Serializers--------------------- """
class UserContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserContact
        fields = ['id', 'name', 'phone_number']
