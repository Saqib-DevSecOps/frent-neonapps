from src.apps.whisper.main import NotificationService
from src.services.finance.helpers import get_finance_class
from src.services.finance.models import Withdrawal, BankAccount, PayPalAccount


def notify_user_withdrawal_create(withdrawal: Withdrawal):
    description = (
        f'Your withdrawal request for {withdrawal.amount} using '
        f'{withdrawal.withdrawal_type} has been submitted successfully.'
    )
    notify = NotificationService(
        heading='Withdrawal update!', description=description,
        obj=withdrawal, recipient_list=[withdrawal.user]
    )
    notify.send_app_notification(actor=withdrawal.user)
    notify.send_email_notification(
        'finance/emails/email_withdrawal_create.html',
        {'obj': withdrawal, 'description': description}
    )


def notify_user_withdrawal_update(withdrawal: Withdrawal):

    description = (
        f'Your withdrawal request for {withdrawal.amount} using '
        f'{withdrawal.withdrawal_type} is {withdrawal.status}, please check your portal for more details'
    )
    notify = NotificationService(
        heading='Withdrawal update!', description=description,
        obj=withdrawal, recipient_list=[withdrawal.user]
    )
    notify.send_app_notification(actor=withdrawal.user)
    notify.send_email_notification(
        'finance/emails/email_withdrawal_update.html',
        {'obj': withdrawal, 'description': description}
    )


def notify_user_finance_add(finance_object):
    finance_class = get_finance_class(finance_object)
    description = (
        f'Your {finance_class} account has been created successfully, please wait for the the verification process.'
    )

    notify = NotificationService(
        heading=f'{finance_class} created!', description=description,
        obj=finance_object, recipient_list=[finance_object.user]
    )
    notify.send_app_notification(actor=finance_object.user)
    notify.send_email_notification(
        'finance/emails/email_finance_create.html',
        {'obj': finance_object, 'description': description}
    )


def notify_user_finance_delete(finance_object):
    pass


def notify_user_finance_update(finance_object):
    finance_class = get_finance_class(finance_object)
    description = f'Your {finance_class} account has been {finance_object.status}'

    notify = NotificationService(
        heading=f'{finance_class} updated!', description=description,
        obj=finance_object, recipient_list=[finance_object.user]
    )
    notify.send_app_notification(actor=finance_object.user)
    notify.send_email_notification(
        'finance/emails/email_finance_update.html',
        {'obj': finance_object, 'description': description}
    )

