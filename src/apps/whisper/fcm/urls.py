from django.urls import path, include
from .views import (
    FCMDeviceListView, FCMDeviceCreateView, FCMDeviceCreateJsonView,
    FCMNotificationCreateAdminView
)

app_name = 'fcm'
urlpatterns = [

    # path('device/', FCMDeviceListView.as_view(), name='device-list'),
    # path('device/create/', FCMDeviceCreateView.as_view(), name='device-create'),
    # path('device/create/post/', FCMDeviceCreateJsonView.as_view(), name='device-create-json'),

    path('api/', include('src.apps.whisper.fcm.api.urls', namespace='api')),
    path('notification/create/admin/', FCMNotificationCreateAdminView.as_view(), name='device-create-admin'),
]
