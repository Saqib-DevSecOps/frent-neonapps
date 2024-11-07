from django.urls import path, include

app_name = "users"

urlpatterns = [
    path('user/api/', include('src.services.users.api.urls', namespace='users-api')),
]
