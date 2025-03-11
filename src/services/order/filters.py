import django_filters

from src.services.order.models import Advertisement, Order, AdvertisementRequest, ServiceBookingRequest, SpecialOffer, \
    Payment


class AdvertisementFilter(django_filters.FilterSet):
    class Meta:
        model = Advertisement
        fields = {
            'user__username': ['icontains'],
            'service': ['icontains'],
            'service_type': ['exact'],
        }


class AdvertisementRequestFilter(django_filters.FilterSet):
    service_provider_name = django_filters.CharFilter(field_name='service_provider__user__username',
                                                      lookup_expr='icontains')
    service_provider_email = django_filters.CharFilter(field_name='service_provider__user__email',
                                                       lookup_expr='icontains')
    service_name = django_filters.CharFilter(field_name='service__title', lookup_expr='icontains')

    class Meta:
        model = AdvertisementRequest
        fields = ['service_provider_name', 'service_provider_email','service_name']


class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = ['user__username', 'payment_type', 'order_status', 'payment_status']


class ServiceBookingRequestFilter(django_filters.FilterSet):
    service_name = django_filters.CharFilter(field_name='service__title', lookup_expr='icontains')
    user_name = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    user_email = django_filters.CharFilter(field_name='user__email', lookup_expr='icontains')

    class Meta:
        model = ServiceBookingRequest
        fields = ['service_name', 'user_name', 'user_email']


class SpecialOfferFilter(django_filters.FilterSet):
    class Meta:
        model = SpecialOffer
        fields = ['user__username', 'service__title', 'status']

class PaymentFilter(django_filters.FilterSet):
    class Meta:
        model = Payment
        fields = ['user__username', 'payment_method']
