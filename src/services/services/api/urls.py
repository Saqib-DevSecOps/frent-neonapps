from django.urls import path

from .views import (
    ServiceListAPIView, ServiceDetailAPIView,
    ProviderServiceListCreateAPIView, ProviderServiceRetrieveUpdateDestroyAPIView,
    ProviderServiceImageUploadCreateAPIView, ProviderServiceImageDeleteAPIView,
    ServiceAvailabilityCreateAPIView, ServiceAvailabilityUpdateDestroyAPIView,
    ServiceLocationCreateAPIView, ServiceLocationUpdateDestroyAPIView, ServiceReviewCreateAPIView,
    ServiceCurrencyView
)

app_name = "services-api"

urlpatterns = [
    path('v1/services/currency/', ServiceCurrencyView.as_view(), name='service-currency'),

    path('v1/services/', ServiceListAPIView.as_view(), name='service-list'),
    path('v1/services/<str:pk>/', ServiceDetailAPIView.as_view(), name='service-detail'),

    # Provider Service Endpoints
    path('v1/provider/services/', ProviderServiceListCreateAPIView.as_view(), name='provider-service-list-create'),

    path('v1/provider/services/<str:pk>/', ProviderServiceRetrieveUpdateDestroyAPIView.as_view(),
         name='provider-service-retrieve-update-destroy'),

    path('v1/provider/services/<str:service_pk>/image/', ProviderServiceImageUploadCreateAPIView.as_view(),
         name='provider-service-image-upload'),
    path('v1/provider/services/<str:pk>/image/delete/', ProviderServiceImageDeleteAPIView.as_view(),
         name='provider-service-image-delete'),

    path('v1/provider/services/<str:service_pk>/availability/', ServiceAvailabilityCreateAPIView.as_view(),
         name='provider-service-availability-create'),
    path('v1/provider/services/<str:service_pk>/availability/<str:pk>/',
         ServiceAvailabilityUpdateDestroyAPIView.as_view(),
         name='provider-service-availability-update-destroy'),

    # Provider Service Location Endpoints
    path('v1/provider/services/<str:service_pk>/location/', ServiceLocationCreateAPIView.as_view(),
         name='provider-service-location-create'),
    path('v1/provider/services/<str:service_pk>/location/<str:pk>/', ServiceLocationUpdateDestroyAPIView.as_view(),
         name='provider-service-location-update-destroy'),

    # Provider Service Review Endpoints
    path('v1/provider/services/<str:service_pk>/review/', ServiceReviewCreateAPIView.as_view(),
         name='provider-service-review-create'),

]
