from django.db.models.signals import post_save
from django.dispatch import receiver

from src.services.finance.models import (
    Withdrawal, PayPalAccount, BankAccount
)
from src.services.finance.notifier import notify_user_finance_add, notify_user_finance_update, \
    notify_user_withdrawal_create, notify_user_withdrawal_update
from src.services.finance.utils import withdrawal_balance_calculation


@receiver(post_save, sender=Withdrawal)
def withdrawal_post(sender, instance, created, **kwargs):
    if created:
        notify_user_withdrawal_create(instance)
    else:
        notify_user_withdrawal_update(instance)
        withdrawal_balance_calculation(instance)


@receiver(post_save, sender=BankAccount)
def bank_account_post(sender, instance, created, **kwargs):
    if created:
        notify_user_finance_add(instance)
    else:
        notify_user_finance_update(instance)


@receiver(post_save, sender=PayPalAccount)
def paypal_account_post(sender, instance, created, **kwargs):
    if created:
        notify_user_finance_add(instance)
    else:
        notify_user_finance_update(instance)
