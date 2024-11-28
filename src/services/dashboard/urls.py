from django.urls import path

from src.services.dashboard.views import DashboardView

app_name = 'dashboard'
urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
