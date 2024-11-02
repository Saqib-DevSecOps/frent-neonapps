import django_filters
from django import forms

from src.apps.stripe.models import StripeCustomer


class StripeCustomerFilter(django_filters.FilterSet):
    user__email = django_filters.CharFilter(
        field_name='user__email',
        lookup_expr='icontains',
        label='User Name',
        widget=forms.TextInput(attrs={'placeholder': 'User Email', 'class': 'form-control'}),
    )

    class Meta:
        model = StripeCustomer
        fields = ('user__email', 'subscription_status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
