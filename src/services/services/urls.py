from django.urls import path, include
from .views import (
    ServicesListView, ServiceDetailView, ServiceReviewListView, UserServiceReviewListView, UserServicesListView
)
app_name = "services"

urlpatterns = [
    path('services/api/', include('src.services.services.api.urls', namespace='services-api')),
    path('service/', ServicesListView.as_view(), name='services-list'),

    path('user/<str:pk>/services/', UserServicesListView.as_view(), name='user-services'),
    path('service/<str:pk>/', ServiceDetailView.as_view(), name='services-detail'),

    path('service/<str:pk>/reviews/', ServiceReviewListView.as_view(), name='services-reviews'),
    path('user/<str:pk>/reviews/', UserServiceReviewListView.as_view(), name='user-reviews'),
]
