from src.services.finance.models import BankAccount, PayPalAccount


def get_finance_class(finance_object):
    if finance_object.__class__ == BankAccount:
        return 'Bank'
    elif finance_object.__class__ == PayPalAccount:
        return 'Paypal'
