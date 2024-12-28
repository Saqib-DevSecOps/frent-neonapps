from rest_framework import status
from rest_framework.generics import UpdateAPIView, CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.services.users.api.serializers import UserSerializer, UserImageSerializer, UserAddressSerializer, \
    ServiceProviderDetailSerializer, ServiceProviderSerializer, SocialMediaSerializer, InterestSerializer, \
    CertificationSerializer, UserUpdateSerializer
from src.services.users.models import UserImage, User, ServiceProvider, SocialMedia, Interest, Certification

""" ---------------------SERVICE SEEKER APIS------------------------ """


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """
    Retrieve and update user profile
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        return UserUpdateSerializer

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.save()


class UserImageCreateAPIView(CreateAPIView):
    """
    Create user image
    """
    queryset = UserImage.objects.all()
    serializer_class = UserImageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserImageDestroyAPIView(DestroyAPIView):
    """
    Delete user image
    """
    queryset = UserImage.objects.all()
    serializer_class = UserImageSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK, data={'message': 'Image deleted successfully'})


class UserAddressRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """
    Retrieve and update user address
    """
    queryset = User.objects.all()
    serializer_class = UserAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.save()


""" ---------------------SERVICE PROVIDER APIS------------------------ """


class ServiceProviderRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """
    Retrieve and update service provider profile
    """
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ServiceProviderDetailSerializer
        return ServiceProviderSerializer

    def get_object(self):
        return self.request.user.service_provider_profile


class ServiceProviderInterestCreateAPIView(CreateAPIView):
    """
    Create service provider interest
    """
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ServiceProviderCertificationCreateAPIView(CreateAPIView):
    """
    Create service provider certification
    """
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(service_provider=self.request.user.service_provider_profile)


class ServiceProviderCertificateDestroyAPIView(DestroyAPIView):
    """
    Delete service provider certification
    """
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.service_provider_profile

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK, data={'message': 'Certificate deleted successfully'})


class ServiceProviderSocialMediaUpdateAPIView(UpdateAPIView):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.service_provider_profile.social_media
