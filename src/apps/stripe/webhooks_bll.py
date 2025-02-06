from src.apps.stripe.helpers import get_date_time
from src.apps.stripe.models import (
    Transfer, Price, StripeCustomer, Payout, ExternalAccount
)
from src.apps.stripe.notifier import (
    notify_payout_created, notify_payout_status_changed, notify_subscriptions_updated
)
from src.services.finance.models import Wallet

""" HELPERS """


def get_user(connect_account_id):
    wallets = Wallet.objects.filter(stripe_account_id=connect_account_id)
    if wallets.exists():
        return wallets.first().user
    return None


def external_account_update_helper(data, external_account):
    external_account.country = data.get("country")
    external_account.fingerprint = data.get("fingerprint")
    external_account.last4 = data.get("last4")
    external_account.metadata = data.get("metadata", {})
    external_account.full_response = data

    if data.get("object") == "bank_account":
        external_account.bank_account_holder_name = data.get("account_holder_name")
        external_account.bank_routing_number = data.get("routing_number")
        external_account.bank_account_holder_type = data.get("account_holder_type")
        external_account.bank_bank_name = data.get("bank_name")
        external_account.bank_currency = data.get("currency")
        external_account.status = data.get('status')

    elif data.get("object") == "card":
        external_account.card_name = data.get('name')
        external_account.card_tokenization_method = data.get('tokenization_method')
        external_account.card_wallet = data.get('wallet')
        external_account.card_brand = data.get('brand')
        external_account.card_exp_month = data.get('exp_month')
        external_account.card_exp_year = data.get('exp_year')
        external_account.card_cvc_check = data.get('cvc_check')
        external_account.card_funding = data.get('funding')
        external_account.card_last4 = data.get('last4')
        external_account.card_address_city = data.get('address_city')
        external_account.card_address_country = data.get('address_country')
        external_account.card_address_line1 = data.get('address_line1')
        external_account.card_address_line1_check = data.get('address_line1_check')
        external_account.card_address_line2 = data.get('address_line2')
        external_account.card_address_state = data.get('address_state')
        external_account.card_address_zip = data.get('address_zip')
        external_account.card_address_zip_check = data.get('address_zip_check')

    external_account.save()


""" ACCOUNTS ------------------------------------------------------------------------------------------------------- """


# TESTED - REQUIRED - CONNECT
def webhook_account_updated(event, data):
    """completed"""

    wallets = Wallet.objects.filter(stripe_account_id=data['object']['id'])
    if wallets:
        wallet = wallets[0]
        wallet.stripe_is_active = True if data['object']['details_submitted'] else False
        wallet.stripe_description = data['object']
        wallet.save()


def webhook_external_account_created(event, _data):
    """completed"""

    data = _data['object']
    external_account_id = data["id"]

    external_account = ExternalAccount.objects.filter(id=external_account_id)
    if not external_account:
        external_account = ExternalAccount.objects.create(
            id=data.get("id"),
            account_id=data.get("account"),
            object=data.get("object"),
        )
        external_account.save()
        external_account_update_helper(data, external_account)


def webhook_external_account_updated(event, _data):
    """completed"""
    data = _data['object']
    external_account_id = data["id"]

    external_account = ExternalAccount.objects.filter(id=external_account_id)
    if external_account:
        external_account_update_helper(data, external_account[0])


def webhook_account_external_account_deleted(event, data):
    """completed"""
    id = data['object']['id']
    accounts = ExternalAccount.objects.filter(id=id).update(is_active=False)


""" TRANSFERS AND PAYOUTS ------------------------------------------------------------------------------------------ """


# TESTED - REQUIRED - CONNECT
def webhook_transfer_updated(event, data):
    """completed"""

    transfer_id = data['object']['id']
    transfer = Transfer.objects.filter(id=transfer_id)
    if transfer:
        transfer = transfer[0]
        transfer.full_response = data['object']
        transfer.metadata = data['object']['metadata']
        transfer.save()


# TESTED - REQUIRED - CONNECT
def webhook_payout_created(event, _data):
    """completed"""
    data = _data['object']
    payout_id = data['id']

    payout = Payout(
        id=payout_id,
        amount=int(data.get('amount')) / 100,
        currency=data.get('currency'),

        type=data.get('type'),
        status=data.get('status'),
        source_type=data.get('source_type'),

        description=data.get('description'),
        destination=data.get('destination'),
        statement_descriptor=data.get('statement_descriptor'),

        failure_code=data.get('failure_code'),
        failure_message=data.get('failure_message'),
        failure_balance_transaction=data.get('failure_balance_transaction'),

        arrival_date=get_date_time(data.get('arrival_date')),
        created=get_date_time(data.get('created')),

        full_response=data,
        metadata=data.get('metadata'),
    )
    payout.save()

    # NOTIFY
    notify_payout_created(payout)


# TESTED - REQUIRED - CONNECT
def webhook_payout_updated(event, _data):
    """completed"""
    data = _data['object']
    payout_id = data['id']

    payout = Payout.objects.filter(id=payout_id)
    if payout:
        payout = payout[0]
        payout.currency = data.get('currency')
        payout.source_type = data.get('source_type')
        payout.description = data.get('description')
        payout.destination = data.get('destination')
        payout.failure_code = data.get('failure_code')
        payout.failure_message = data.get('failure_message')
        payout.failure_balance_transaction = data.get('failure_balance_transaction')
        payout.arrival_date = get_date_time(data.get('arrival_date'))
        payout.created = get_date_time(data.get('created'))
        payout.metadata = data.get('metadata')
        payout.save()


# TESTED - REQUIRED - CONNECT
def webhook_payout_status_change(event, _data, status):
    data = _data['object']
    payout_id = data['id']

    payout = Payout.objects.get(id=payout_id)
    payout.description = data.get('description')
    payout.destination = data.get('destination')
    payout.failure_code = data.get('failure_code')
    payout.failure_message = data.get('failure_message')
    payout.failure_balance_transaction = data.get('failure_balance_transaction')
    payout.arrival_date = get_date_time(data.get('arrival_date'))
    payout.created = get_date_time(data.get('created'))
    payout.metadata = data.get('metadata')
    payout.status = data.get('status')

    payout.save()

    # NOTIFY
    notify_payout_status_changed(payout)


""" SUBSCRIPTIONS -------------------------------------------------------------------------------------------------- """


def subscription_local_update_from_webhooks(data):
    """
    update local database from webhooks response
    webhooks > customer.subscription.created > customer.subscription.updated
    """

    data = data['object']
    subscription = StripeCustomer.objects.filter(customer_id=data['customer'])
    subscription_id = data['id']
    price = Price.objects.filter(id=data['items']['data'][0]['price']['id'])

    if subscription:
        subscription = subscription[0]
        subscription.stripe_price = price[0]
        subscription.subscription_id = subscription_id
        subscription.subscription_full_response = data
        subscription.subscription_status = data['status']
        subscription.price_id = data['items']['data'][0]['price']['id']
        subscription.subscription_start = get_date_time(data['current_period_start'])
        subscription.subscription_end = get_date_time(data['current_period_end'])
        subscription.created = get_date_time(data['created'])
        subscription.save()

        # NOTIFY
        notify_subscriptions_updated(subscription)


def webhook_subscription_created(event, data):
    """completed"""
    pass


def webhook_subscription_updated(event, data):
    """completed"""
    subscription_local_update_from_webhooks(data)


def webhook_subscription_deleted(event, data):
    """completed"""

    subscription_id = data['object']['id']
    subscription = StripeCustomer.objects.filter(subscription_id=subscription_id)
    if subscription:
        subscription[0].delete()