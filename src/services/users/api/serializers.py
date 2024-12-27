from rest_framework import serializers

from src.services.users.models import UserImage, Address, Interest, Certification, SocialMedia, User, ServiceProvider


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


class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = ['id', 'image']


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'user', 'address', 'city', 'region', 'country', 'zip_code', ]
        read_only_fields = ['user']


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'name']


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = ['id', 'certificate_file', ]


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = ['id', 'facebook', 'instagram', 'twitter', 'linkedin', ]


class ServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProvider
        fields = ['id', 'company_name', 'phone_number', 'website']


class ServiceProviderDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    social_media = SocialMediaSerializer()
    interests = InterestSerializer(many=True)
    certifications = CertificationSerializer(many=True)
    address = UserAddressSerializer(source="user.address")

    class Meta:
        model = ServiceProvider
        fields = ['id', 'user', 'address', 'company_name', 'phone_number', 'website', 'rating', 'total_reviews',
                  'verified', 'status', 'social_media', 'interests', 'certifications']
        read_only_fields = ['user', 'social_media', 'interests', 'certifications', 'address', 'rating', 'total_reviews',
                            'verified', 'status', ]
