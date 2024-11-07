from django.urls import path

from .views import (
    ServiceListAPIView, ServiceDetailAPIView,
    ProviderServiceListCreateAPIView, ProviderServiceRetrieveUpdateDestroyAPIView,
    ProviderServiceImageUploadCreateAPIView, ProviderServiceImageDeleteAPIView,
    ServiceAvailabilityCreateAPIView, ServiceAvailabilityUpdateDestroyAPIView,
    ServiceLocationCreateAPIView, ServiceLocationUpdateDestroyAPIView
)

app_name = "services-api"
urlpatterns = [
    path('v1/service/', ServiceListAPIView.as_view(), name='service-list'),
    path('v1/<str:pk>/service/', ServiceDetailAPIView.as_view(), name='service-detail'),
    path('v1/provider/service/', ProviderServiceListCreateAPIView.as_view(), name='provider-service-list-create'),
    path('v1/provider/<str:pk>/service/', ProviderServiceRetrieveUpdateDestroyAPIView.as_view(),
         name='provider-service-retrieve-update-destroy'),
    path('v1/provider/<str:service_pk>/service/image/', ProviderServiceImageUploadCreateAPIView.as_view(),
         name='provider-service-image-upload'),
    path('v1/provider/<str:pk>/service/image/', ProviderServiceImageDeleteAPIView.as_view(),
         name='provider-service-image-delete'),
    path('v1/provider/<str:service_pk>/service/availability/', ServiceAvailabilityCreateAPIView.as_view(),
         name='provider-service-availability-create'),
    path('v1/provider/service/<str:pk>/availability/', ServiceAvailabilityUpdateDestroyAPIView.as_view(),
         name='provider-service-availability-update-destroy'),
    path('v1/provider/<str:service_pk>/service/location/', ServiceLocationCreateAPIView.as_view(),
         name='provider-service-location-create'),
    path('v1/provider/<str:pk>/service/location/', ServiceLocationUpdateDestroyAPIView.as_view(),
         name='provider-service-location-update-destroy'),

]
