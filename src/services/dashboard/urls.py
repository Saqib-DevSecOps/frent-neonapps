from django.urls import path

from src.services.dashboard import views

app_name = 'dashboard'
urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
