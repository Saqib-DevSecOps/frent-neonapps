from django.urls import path, include

app_name = "order"

urlpatterns = [
    path('order/api/', include('src.services.order.api.urls', namespace='order-api')),
]
