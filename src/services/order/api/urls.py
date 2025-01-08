from django.urls import path
from .views import AdvertListCreateAPIView, AdvertDestroyAPIView, \
    BookingRequestListCreateAPIView, BookingRequestUpdateAPIView, BookingRequestDestroyAPIView

app_name = "order-api"

urlpatterns = [

    path('adverts/', AdvertListCreateAPIView.as_view(), name='adverts'),
    path('advert/<int:pk>/delete/', AdvertDestroyAPIView.as_view(), name='advert-delete'),
    path('advert/<int:advert_id>/booking-requests/', BookingRequestListCreateAPIView.as_view(),
         name='booking-requests'),
    path('booking-request/<int:pk>/', BookingRequestUpdateAPIView.as_view(), name='booking-request-update'),
    path('booking-request/<int:pk>/', BookingRequestDestroyAPIView.as_view(), name='booking-request-delete'),
]