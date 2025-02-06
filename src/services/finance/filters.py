import django_filters
from django.forms import TextInput

from src.services.finance.models import Withdrawal, BankAccount, PayPalAccount


class WithdrawalFilter(django_filters.FilterSet):
    class Meta:
        model = Withdrawal
        fields = {
            'withdrawal_type', 'status'
        }


class BankAccountFilter(django_filters.FilterSet):
    account_holder_name = django_filters.CharFilter(
        widget=TextInput(attrs={'placeholder': 'Account Holder Name'}), lookup_expr='icontains'
    )

    class Meta:
        model = BankAccount
        fields = {
            'status', 'account_type', 'currency'
        }


class PaypalAccountFilter(django_filters.FilterSet):
    account_holder_name = django_filters.CharFilter(
        widget=TextInput(attrs={'placeholder': 'Account holder name'}), lookup_expr='icontains'
    )
    email = django_filters.CharFilter(
        widget=TextInput(attrs={'placeholder': 'Paypal email'}), lookup_expr='icontains'
    )

    class Meta:
        model = PayPalAccount
        fields = {
            'status', 'email'
        }

