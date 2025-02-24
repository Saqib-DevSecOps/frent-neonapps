from django.urls import path

from .views import (
    FCMDeviceActivationAPIView, FCMDeviceRegistrationAPIView, FCMDeviceDeleteAPIView,
    FCMDeviceRegisterOrUpdateAPIView
)

app_name = 'api'
urlpatterns = [
    path('device/register/', FCMDeviceRegistrationAPIView.as_view(), name='device-register'),
    path('device/register-or-change/', FCMDeviceRegisterOrUpdateAPIView.as_view(), name='device-register-or-change'),
    path('device/<str:registration_id>/activation/', FCMDeviceActivationAPIView.as_view(), name='device-activate'),
    path('device/<str:registration_id>/delete/', FCMDeviceDeleteAPIView.as_view(), name='device-delete'),
]

