# views.py
from cities_light.models import Region, SubRegion
from django.db import models
from django.db.models import Avg, Count
from django.views.generic import CreateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404, \
    UpdateAPIView, DestroyAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.views import APIView

from src.services.services.models import Service, ServiceCategory, ServiceImage
from .filters import ServiceFilter
from .serializers import (
    ServiceHomeListSerializer,
    ServiceDetailSerializer,
    ServiceSerializer, ServiceCategorySerializer, SubRegionSerializer, RegionSerializer, ServiceCreateUpdateSerializer,
    ServiceAvailabilitySerializer, ServiceLocationSerializer, ServiceImageSerializer
)


class HomeAPIView(ListAPIView):
    serializer_class = ServiceHomeListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        popular_services = (
            Service.objects.filter(is_active=True)
            .annotate(
                average_rating=Avg('reviews__rating', filter=models.Q(reviews__is_active=True)),
                reviews_count=Count('reviews', filter=models.Q(reviews__is_active=True))
            )
            .order_by('-average_rating')[:5]
        )
        my_interest = Service.objects.filter(is_active=True).order_by('?')[:10]
        top_categories = ServiceCategory.objects.filter(is_active=True)[:10]

        data = {
            'top_categories': top_categories,
            'my_interest': my_interest,
            'popular_services': popular_services,
        }
        return data

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class ServiceListAPIView(generics.ListAPIView):
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServiceFilter
    permission_classes = [IsAuthenticatedOrReadOnly]


class ServiceDetailAPIView(generics.RetrieveAPIView):
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


"""-------------------For Service Providers-------------------"""


# Provider Service
class ProviderServiceListCreateAPIView(ListCreateAPIView):
    queryset = Service.objects.all()
    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        service = get_object_or_404(Service.objects.filter(provider=self.request.user),
                                    pk=self.kwargs.get('service_pk'))
        serializer.save(service=service)
        return Response(status=status.HTTP_201_CREATED, data={'message': 'Image uploaded successfully'})


class ProviderServiceImageDeleteAPIView(DestroyAPIView):
    queryset = ServiceImage.objects.all()
    serializer_class = ServiceImage
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_object_or_404(ServiceImage, service__provider=self.request.user, pk=self.kwargs.get('pk'))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK, data={'message': 'Image deleted successfully'})


# Provider Service Availability
class ServiceAvailabilityCreateAPIView(CreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceAvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        service = get_object_or_404(Service, provider=self.request.user, pk=self.kwargs.get('service_pk'))
        serializer.save(service=service)
        return Response(status=status.HTTP_201_CREATED, data={'message': 'Availability slot created successfully'})


class ServiceAvailabilityUpdateDestroyAPIView(UpdateAPIView, DestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceAvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Service, provider=self.request.user, pk=self.kwargs.get('service_pk'))

    def perform_update(self, serializer):
        serializer.save(service=self.get_object())

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK, data={'message': 'Availability slot deleted successfully'})


# Provider Service Location

class ServiceLocationCreateAPIView(CreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceLocationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        service = get_object_or_404(Service, provider=self.request.user, pk=self.kwargs.get('service_pk'))
        serializer.save(service=service)
        return Response(status=status.HTTP_201_CREATED, data={'message': 'Location created successfully'})


class ServiceLocationUpdateDestroyAPIView(UpdateAPIView, DestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceLocationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Service, provider=self.request.user, pk=self.kwargs.get('pk'))

    def perform_update(self, serializer):
        serializer.save(service=self.get_object())

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK, data={'message': 'Location deleted successfully'})


"""-------------------Helper-------------------"""


class CategorySubRegionProvinceApiView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        category = ServiceCategory.objects.all()
        sub_region = SubRegion.objects.all()
        province = Region.objects.all()
        context = {
            'category': ServiceCategorySerializer(category, many=True).data,
            'sub_region': SubRegionSerializer(sub_region, many=True).data,
            'province': RegionSerializer(province, many=True).data

        }
        return Response(data=context, status=status.HTTP_200_OK)
