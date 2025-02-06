from django import forms

from src.services.finance.models import Withdrawal, PayPalAccount, BankAccount


class WithdrawalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.instance and self.user:
            self.instance.user = self.user  # Set the user on the instance

    class Meta:
        model = Withdrawal
        fields = ['amount', 'withdrawal_type']


class PaypalAccountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.instance and self.user:
            self.instance.user = self.user  # Set the user on the instance

    class Meta:
        model = PayPalAccount
        fields = ['account_holder_name', 'email']


class BankAccountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.instance and self.user:
            self.instance.user = self.user  # Set the user on the instance

    class Meta:
        model = BankAccount
        fields = ['account_holder_name', 'account_type', 'bank_name', 'iban', 'currency']

