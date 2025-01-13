import django_filters

from src.services.order.models import Advertisement, Order, AdvertisementRequest


class AdvertisementFilter(django_filters.FilterSet):
    class Meta:
        model = Advertisement
        fields = {
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
        fields = ['payment_type', 'order_status', 'payment_status']
