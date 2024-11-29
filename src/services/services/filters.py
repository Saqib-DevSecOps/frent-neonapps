import django_filters


class ServiceFilter(django_filters.FilterSet):
    class Meta:
        model = Service