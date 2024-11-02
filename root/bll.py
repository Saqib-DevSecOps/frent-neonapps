import decimal
from django.utils import timezone


def convert_cents_to_decimal(amount_in_cents):
    return decimal.Decimal(amount_in_cents) / 100
