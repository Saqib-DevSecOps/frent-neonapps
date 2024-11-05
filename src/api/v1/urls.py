from django.urls import path

from src.api.v1.views import (HomeAPIView, ServiceListView, ServiceDetailView)

app_name = 'v1'
urlpatterns = [
    path('home/', HomeAPIView.as_view(), name='home'),
    path('services/', ServiceListView.as_view(), name='service-list'),
    path('services/<str:pk>/', ServiceDetailView.as_view(), name='service-detail'),
]