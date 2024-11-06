# views.py
from cities_light.models import Region, SubRegion
from django.db import models
from django.db.models import Avg, Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.views import APIView

from src.services.services.models import Service, ServiceCategory
from .filters import ServiceFilter
from .serializers import (
    ServiceHomeListSerializer,
    ServiceDetailSerializer,
    ServiceSerializer, ServiceCategorySerializer, ServiceHomeSerializer, SubRegionSerializer, RegionSerializer
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


class ServiceListView(generics.ListAPIView):
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServiceFilter
    permission_classes = [IsAuthenticatedOrReadOnly]


class ServiceDetailView(generics.RetrieveAPIView):
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CategorySubRegionProvinceApiView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        category = ServiceCategory.objects.all()
        sub_region = SubRegion.objects.all()
        province = Region.objects.all()
        print(province)

        context = {
            'category': ServiceCategorySerializer(category, many=True).data,
            'sub_region': SubRegionSerializer(sub_region, many=True).data,
            'province': RegionSerializer(province, many=True).data

        }
        return Response(data=context, status=status.HTTP_200_OK)
