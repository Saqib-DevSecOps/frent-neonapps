from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, \
    get_object_or_404, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from src.services.services.api.filters import ServiceFilter
from src.services.services.api.serializers import ServiceSerializer, ServiceDetailSerializer, \
    ServiceCreateUpdateSerializer, ServiceImageSerializer, ServiceAvailabilitySerializer, ServiceLocationSerializer, \
    ServiceReviewSerializer
from src.services.services.models import Service, ServiceImage, ServiceLocation, ServiceAvailability, ServiceReview

"""SERVICE SEEKER APIS"""


class ServiceListAPIView(ListAPIView):
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServiceFilter
    permission_classes = [IsAuthenticatedOrReadOnly]


class ServiceDetailAPIView(RetrieveAPIView):
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


"""SERVICE SEEKER APIS"""


# Provider Service
class ProviderServiceListCreateAPIView(ListCreateAPIView):
    queryset = Service.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ServiceCreateUpdateSerializer
        return ServiceSerializer

    def get_queryset(self):
        return Service.objects.filter(provider=self.request.user)

    def perform_create(self, serializer):
        serializer.save(provider=self.request.user)


class ProviderServiceRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(provider=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ServiceDetailSerializer
        return ServiceCreateUpdateSerializer

    def get_object(self):
        return get_object_or_404(Service, provider=self.request.user, pk=self.kwargs.get('pk'))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK, data={'message': 'Service deleted successfully'})


# Provider Service Image
class ProviderServiceImageUploadCreateAPIView(CreateAPIView):
    queryset = ServiceImage.objects.all()
    serializer_class = ServiceImageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        service = get_object_or_404(Service.objects.filter(provider=self.request.user),
                                    pk=self.kwargs.get('service_pk'))
        serializer.save(service=service)
        return Response(status=status.HTTP_201_CREATED, data={'message': 'Image uploaded successfully'})


class ProviderServiceImageDeleteAPIView(DestroyAPIView):
    queryset = ServiceImage.objects.all()
    serializer_class = ServiceImage
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(ServiceImage, service__provider=self.request.user, pk=self.kwargs.get('pk'))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK, data={'message': 'Image deleted successfully'})


# Provider Service Availability
class ServiceAvailabilityCreateAPIView(CreateAPIView):
    queryset = ServiceAvailability.objects.all()
    serializer_class = ServiceAvailabilitySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        service = get_object_or_404(Service, provider=self.request.user, pk=self.kwargs.get('service_pk'))
        serializer.save(service=service)
        return Response(status=status.HTTP_201_CREATED, data={'message': 'Availability slot created successfully'})


class ServiceAvailabilityUpdateDestroyAPIView(UpdateAPIView, DestroyAPIView):
    queryset = ServiceAvailability.objects.all()
    serializer_class = ServiceAvailabilitySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        service = get_object_or_404(Service, provider=self.request.user, pk=self.kwargs.get('service_pk'))
        return get_object_or_404(ServiceAvailability, service=service, pk=self.kwargs.get('pk'))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK, data={'message': 'Availability slot deleted successfully'})


# Provider Service Location

class ServiceLocationCreateAPIView(CreateAPIView):
    queryset = ServiceLocation.objects.all()
    serializer_class = ServiceLocationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        service = get_object_or_404(Service, provider=self.request.user, pk=self.kwargs.get('service_pk'))
        serializer.save(service=service)
        return Response(status=status.HTTP_201_CREATED, data={'message': 'Location created successfully'})


class ServiceLocationUpdateDestroyAPIView(UpdateAPIView, DestroyAPIView):
    queryset = ServiceLocation.objects.all()
    serializer_class = ServiceLocationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        service = get_object_or_404(Service, provider=self.request.user, pk=self.kwargs.get('service_pk'))
        return get_object_or_404(ServiceLocation, service=service, pk=self.kwargs.get('pk'))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK, data={'message': 'Location deleted successfully'})


class ServiceReviewCreateAPIView(CreateAPIView):
    queryset = ServiceReview.objects.all()
    serializer_class = ServiceReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        service = get_object_or_404(Service, pk=self.kwargs.get('service_pk'))
        serializer.save(service=service, reviewer=self.request.user)
        return Response(status=status.HTTP_201_CREATED, data={'message': 'Review created successfully'})
