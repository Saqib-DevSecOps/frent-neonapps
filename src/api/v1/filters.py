import django_filters
from django.db.models import Avg
from src.services.services.models import Service

class ServiceFilter(django_filters.FilterSet):
    category = django_filters.UUIDFilter(field_name="category__id")
    location = django_filters.CharFilter(field_name="provider__service_provider_profile__address", lookup_expr='icontains')
    province = django_filters.CharFilter(field_name="provider__service_provider_profile__region__name", lookup_expr='icontains')
    sub_region = django_filters.CharFilter(field_name="provider__service_provider_profile__sub_region__name", lookup_expr='icontains')
    average_rating = django_filters.NumberFilter(method='filter_by_average_rating')
    date = django_filters.CharFilter(method='filter_by_date_and_time')
    start_time = django_filters.TimeFilter(method='filter_by_date_and_time')
    end_time = django_filters.TimeFilter(method='filter_by_date_and_time')

    class Meta:
        model = Service
        fields = ['category', 'location', 'average_rating', 'date', 'start_time', 'end_time', 'sub_region']

    def filter_by_average_rating(self, queryset, name, value):
        # Annotate services with average rating and filter based on the provided value
        return queryset.annotate(average_rating=Avg('reviews__rating')).filter(average_rating=value)

    def filter_by_date_and_time(self, queryset, name, value):
        date = self.data.get('date')
        start_time = self.data.get('start_time')
        end_time = self.data.get('end_time')

        if date and start_time and end_time:
            queryset = queryset.filter(
                availability_slots__day_of_week=date,
                availability_slots__start_time__lte=start_time,
                availability_slots__end_time__gte=end_time,
                availability_slots__is_active=True
            )

        return queryset
