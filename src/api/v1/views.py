# views.py
from django.db import models
from django.db.models import Avg, Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from src.services.services.models import Service, ServiceCategory
from .filters import ServiceFilter
from .serializers import (
    ServiceHomeListSerializer,
    ServiceDetailSerializer,
    ServiceSerializer, ServiceCategorySerializer, ServiceHomeSerializer
)


class HomeAPIView(ListAPIView):
    serializer_class = ServiceHomeListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        top_services = (
            Service.objects.filter(is_active=True)
            .annotate(
                average_rating=Avg('reviews__rating', filter=models.Q(reviews__is_active=True)),
                reviews_count=Count('reviews', filter=models.Q(reviews__is_active=True))
            )
            .order_by('-average_rating')[:5]
        )
        new_services = Service.objects.filter(is_active=True).order_by('-created_at')[:5]
        top_categories = ServiceCategory.objects.filter(is_active=True)[:5]

        data = {
            'top_services': top_services,
            'new_services': new_services,
            'top_categories': top_categories,
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
