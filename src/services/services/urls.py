from django.urls import path, include

app_name = "services"

urlpatterns = [
    path('services/api/', include('src.services.services.api.urls', namespace='services-api')),
]
