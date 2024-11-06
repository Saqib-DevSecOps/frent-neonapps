from django.urls import path
from zope.interface import named

from src.api.v1.views import (HomeAPIView, ServiceListAPIView, ServiceDetailAPIView, CategorySubRegionProvinceApiView,
                              ProviderServiceListCreateAPIView, ProviderServiceRetrieveUpdateDestroyAPIView,
                              ProviderServiceImageUploadCreateAPIView, ProviderServiceImageDeleteAPIView,
                              ServiceAvailabilityCreateAPIView, ServiceAvailabilityUpdateDestroyAPIView,
                              ServiceLocationCreateAPIView, ServiceLocationUpdateDestroyAPIView
                              )

app_name = 'v1'

"""-----------------For Service Seekers-----------------"""
urlpatterns = [
    path('home/', HomeAPIView.as_view(), name='home'),
    path('services/', ServiceListAPIView.as_view(), name='service-list'),
    path('services/<str:pk>/', ServiceDetailAPIView.as_view(), name='service-detail'),
    path('helpers/', CategorySubRegionProvinceApiView.as_view(), name='service-helper'),
]

"""-----------------For Service Providers-----------------"""

urlpatterns += [
    path('provider/service/', ProviderServiceListCreateAPIView.as_view(), name='provider-service-list-create'),

    path('provider/service/<str:pk>/', ProviderServiceRetrieveUpdateDestroyAPIView.as_view(),
         name='provider-service-retrieve-update-destroy'),

    path('provider/service/images/<str:service_pk>', ProviderServiceImageUploadCreateAPIView.as_view(),
         name='provider-service-image-upload'),
    path('provider/service/image/<str:pk>', ProviderServiceImageDeleteAPIView.as_view(),
         name='provider-service-image-delete'),
    path('provider/service/availability/<str:service_pk>/', ServiceAvailabilityCreateAPIView.as_view(),
         name='provider-service-availability-create'),

    path('api/v1/provider/service/availability/<str:pk>/', ServiceAvailabilityUpdateDestroyAPIView.as_view(),
         name='provider-service-availability-update-destroy'),

    path('provider/service/location/<str:service_pk>/', ServiceLocationCreateAPIView.as_view(),
         name='provider-service-location-create'),

    path('provider/service/location/<str:pk>/', ServiceLocationUpdateDestroyAPIView.as_view(),
         name='provider-service-location-update-destroy'),
]

"""-----------------For Admins-----------------"""
urlpatterns += [

]
