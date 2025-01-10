from django.urls import path

from src.services.order.api.views import AdvertisementListCreateAPIView, AdvertisementRequestListAPIView, \
    AdvertisementRequestCreateAPIView, AdvertisementRequestUpdateAPIView, OrderListCreateAPIView, \
    OrderRetrieveUpdateAPIView, ServiceBookingRequestListCreateAPIView, ServiceBookingRequestUpdateAPIView

app_name = "order-api"

urlpatterns = [
    path('v1/advertisement/', AdvertisementListCreateAPIView.as_view(), name='advertisement-list-create'),

    path('v1/advertisement-request/<str:advertisement_id>/', AdvertisementRequestListAPIView.as_view(),
         name='advertisement-request-list'),

    path('v1/provider/advertisement-request/<str:advertisement_id>/', AdvertisementRequestCreateAPIView.as_view(),
         name='advertisement-request-create'),

    path('v1/advertisement-request/<str:pk>/update/', AdvertisementRequestUpdateAPIView.as_view(),
         name='advertisement-request-update'),
    path('v1/orders/', OrderListCreateAPIView.as_view(), name='service-order-list-create'),
    path('v1/orders/<str:pk>/', OrderRetrieveUpdateAPIView.as_view(), name='order-retrieve-update'),

    path('v1/provider/service/service-booking-requests/', ServiceBookingRequestListCreateAPIView.as_view(),
         name='service-booking-request-list-create'),
    path('v1/provider/service/service-booking-requests/<str:pk>/', ServiceBookingRequestUpdateAPIView.as_view(),
         name='service-booking-request-update'),
]
