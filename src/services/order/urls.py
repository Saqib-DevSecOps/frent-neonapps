from django.urls import path, include

from src.services.order.views import (
    AdvertisementListView, AdvertisementRequestsListView, OrderListView, OrderDetailView, ServiceBookingRequestListView,
    SpecialOfferListView, PaymentsListView, ServiceBookingRequestListView
)

app_name = "order"

urlpatterns = [
    path('advertisement/', AdvertisementListView.as_view(), name='advertisement-list'),
    path('advertisement-request/<str:advertisement_id>/', AdvertisementRequestsListView.as_view(),
         name='advertisement-request-list'),
    path('order/', OrderListView.as_view(), name='order-list'),
    path('order/<str:pk>/', OrderDetailView.as_view(), name='order-detail'),
]

urlpatterns += [
    path('order/api/', include('src.services.order.api.urls', namespace='order-api')),

]

urlpatterns += [
    path('service-requests/', ServiceBookingRequestListView.as_view(), name='services-request'),
    path('special-offers/', SpecialOfferListView.as_view(), name='special-offers'),
    path('payment/', PaymentsListView.as_view(), name='payment-list'),

]

urlpatterns += [
    path('service/<str:pk>/requests/', ServiceBookingRequestListView.as_view(), name='services-requests'),
]