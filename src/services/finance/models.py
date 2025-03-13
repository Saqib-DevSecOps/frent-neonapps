from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from src.apps.stripe.bll import stripe_transfer_to_connect_account
from src.services.users.models import User

BANK_ACCOUNT_TYPES = (
    ('personal', 'Personal'),
    ('business', 'Business')
)
FINANCE_ACCOUNT_STATUS = (
    ('pending', 'Pending'),
    ('verified', 'Verified'),
    ('cancelled', 'Cancelled')
)
WITHDRAWAL_TYPES = (
    ('bank', 'Bank'),
    ('connect', 'Connect')
)
WITHDRAWAL_STATUS = (
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('cancelled', 'Cancelled')
)


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    description = models.TextField(null=True, blank=True)

    # STRIPE
    stripe_account_id = models.CharField(max_length=255, null=True, blank=True)
    stripe_account_type = models.CharField(max_length=255, null=True, blank=True)
    stripe_account_country = models.CharField(max_length=255, null=True, blank=True)
    stripe_account_email = models.EmailField(null=True, blank=False)
    stripe_description = models.JSONField(null=True, blank=True)
    stripe_is_active = models.BooleanField(default=False)

    # OVERALL REPORT
    total_amounts = models.FloatField(default=0)
    total_deposits = models.FloatField(default=0)
    total_earnings = models.FloatField(default=0)
    total_withdrawals = models.FloatField(default=0)

    # BALANCE REPORT
    balance_available = models.FloatField(default=0)
    balance_pending = models.FloatField(default=0)
    outstanding_charges = models.FloatField(default=0)

    # CONNECT REPORT
    connect_available_balance = models.FloatField(default=0)
    connect_available_balance_currency = models.CharField(max_length=3, null=True, blank=True)
    connect_pending_balance = models.FloatField(default=0)
    connect_pending_balance_currency = models.CharField(max_length=3, null=True, blank=True)

    # DATES
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = 'Wallets'

    def __str__(self):
        return str(self.pk)

    def is_stripe_connected(self):
        return self.stripe_account_id is not None

    def is_stripe_account_active(self):
        if not self.is_stripe_connected() or not self.stripe_is_active:
            return False
        return True

    def get_available_balance(self):
        return self.balance_available

    def get_pending_balance(self):
        return self.balance_pending

    def get_connect_balance(self):
        return self.connect_available_balance


class FinanceAccount(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_finance_account', blank=True
    )
    account_holder_name = models.CharField(max_length=100)
    description = models.TextField(
        blank=True, null=True, help_text='You have applied for account please wait for verification process'
    )

    status = models.CharField(
        max_length=20, choices=FINANCE_ACCOUNT_STATUS, default=FINANCE_ACCOUNT_STATUS[0][0],
        help_text='Status of account'
    )
    is_active = models.BooleanField(
        default=True, help_text='Is this bank active? only active accounts will be available for withdrawal.'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.account_holder_name}'

    def clean(self):
        # user is required here.
        try:
            user = self.user
        except Exception as e:
            raise ValidationError('User is required for account')


        # First time status must be pending
        if not self.pk:
            if self.status != 'pending':
                raise ValidationError({'status': 'Status must be pending at start'})

            previous_accounts = None
            if self.__class__ == BankAccount:
                previous_accounts = BankAccount.objects.filter(user=self.user)
            elif self.__class__ == PayPalAccount:
                previous_accounts = PayPalAccount.objects.filter(user=self.user)

            if previous_accounts.exists():
                raise ValidationError(f'Seeds wild only allows 1 {self.__class__.__name__} per vendor')

        return super().clean()


class BankAccount(FinanceAccount):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bank_accounts', blank=True
    )
    account_type = models.CharField(max_length=20, choices=BANK_ACCOUNT_TYPES, default=BANK_ACCOUNT_TYPES[0][0])
    bank_name = models.CharField(max_length=100)
    iban = models.CharField(max_length=50, unique=True)
    currency = models.CharField(max_length=3, default='USD', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Bank Accounts'
        ordering = ('-created_at',)

    def last_4_digits(self):
        return " * * * * " + self.iban[-4:]


class PayPalAccount(FinanceAccount):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paypal_accounts', blank=True)
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name_plural = 'Paypal Accounts'
        ordering = ('-created_at',)


class Withdrawal(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='withdrawals', blank=True
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False)
    withdrawal_type = models.CharField(max_length=20, choices=WITHDRAWAL_TYPES, default=WITHDRAWAL_TYPES[0][0])

    description = models.TextField(
        blank=True, null=True, help_text='You have applied for account please wait for verification process'
    )
    status = models.CharField(
        max_length=20, choices=WITHDRAWAL_STATUS, default=WITHDRAWAL_STATUS[0][0], help_text='Status of withdrawal'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Withdrawals'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} - {self.amount} - {self.status}'

    def handle_connect_withdrawal(self, obj):
        success = False

        try:
            amount = int(self.amount)
        except ValueError:
            return success, "Please enter a valid integer amount"

        success, obj = stripe_transfer_to_connect_account(user=self.user, amount=self.amount)
        return success, obj

    def clean(self):

        # user is required here.
        try:
            user = self.user
        except Exception as e:
            raise ValidationError('User is required for withdrawal')

        # get vendor and wallet
        wallet = self.user.get_user_wallet()

        # user must be vendor


        # balance check
        if self.amount > wallet.balance_available:
            raise ValidationError({'amount': 'Insufficient balance in wallet'})

        # withdrawal type check and validation
        if self.withdrawal_type == 'bank':
            if not user.bank_account_active():
                raise ValidationError({'withdrawal_type': 'User does not have an active bank account'})
        # elif self.withdrawal_type == 'paypal':
        #     if not user.paypal_account_active():
        #         raise ValidationError({'withdrawal_type': 'User does not have an active PayPal account'})

        elif self.withdrawal_type == 'connect':
            if not self.user.is_stripe_account_active():
                raise ValidationError({'withdrawal_type': 'user connect account is not active'})
        else:
            raise ValidationError({'withdrawal_type': 'Invalid withdrawal type'})

        # First time status must be pending
        if not self.pk:

            previous_withdrawals = Withdrawal.objects.filter(user=self.user, status__in=['pending'])
            if previous_withdrawals.exists():
                raise ValidationError(f'Your previous withdrawal request is still pending.')

            if self.status != 'pending':
                raise ValidationError({'status': 'Status must be pending at start'})

        else:
            previous_status = Withdrawal.objects.get(pk=self.pk).status
            if previous_status in ['accepted', 'cancelled']:
                raise ValidationError({'status': 'Cancelled or accepted requests cannot be updated'})

        if self.withdrawal_type == 'connect' and self.status == 'accepted':
            success, obj = self.handle_connect_withdrawal(self)
            if not success:
                raise ValidationError(obj)


class Transaction(models.Model):
    TRANSACTION_TYPE = (
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('charge', 'Charge'),
        ('refund', 'Refund'),
    )
    STATUS_TYPE = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_transaction'
    )
    amount = models.FloatField(default=0)
    transaction_type = models.CharField(
        max_length=50, choices=TRANSACTION_TYPE, default='deposit'
    )
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_TYPE, default="completed")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Transactions"

    def __str__(self):
        return str(self.pk)

    def get_wallet(self):
        return self.user.get_user_wallet()

    def clean(self):

        # AMOUNT CHECK
        if self.amount <= 0:
            raise ValidationError('Amount must be greater than 0')

        # USER MUST HAVE WALLET
        wallet = Wallet.objects.filter(user=self.user)
        if wallet:
            wallet = wallet[0]
        else:
            raise ValidationError('User must have wallet to perform transaction')

        # WALLET MUST HAVE GREATER AMOUNT OF MONEY THAN
        if self.transaction_type in ['withdrawal', 'charge']:
            if wallet.balance_available < self.amount:
                raise ValidationError('Insufficient balance to perform this transaction')

        # IF ALREADY EXISTS THEN DON'T ALLOW TO CHANGE
        if self.pk:
            previous_status = Transaction.objects.get(pk=self.pk).status
            if previous_status:
                raise ValidationError("You aren't allowed to change status of transaction")


class Charge(models.Model):
    CHARGE_TYPE_CHOICES = [
        ('product_listing_fee', 'Product Listing Fee'),
        ('transaction_fee', 'Transaction Fee'),
        ('payment_processing', 'Payment Processing Fee'),
        ('deposit_fee', 'Deposit Fee'),
        ('currency_conversion', 'Currency Conversion Fee'),
        ('vat_processing', 'VAT on Processing Fees'),
        ('vat_seller_services', 'VAT on Seller Services'),
    ]
    STATUS_TYPE = [
        ('init', 'Initialized'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    # Using GenericForeignKey
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fee_amount = models.FloatField(default=0)
    fee_type = models.CharField(choices=CHARGE_TYPE_CHOICES, max_length=30)
    currency = models.CharField(max_length=3, default='USD')
    description = models.TextField()
    status = models.CharField(max_length=30, choices=STATUS_TYPE, default=STATUS_TYPE[0][0])

    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Charge'
        verbose_name_plural = 'Charges'
        ordering = ['-created_at']

    def __str__(self):
        return self.fee_type

    def clean(self):

        # AMOUNT CHECK
        if self.fee_amount <= 0:
            raise ValidationError('Fee amount must be greater than 0')

        # IF PREVIOUS STATUS IS COMPLETED DON"T ALLOW TO CHANGE
        if self.pk:
            previous_status = Charge.objects.get(pk=self.pk).status

            if previous_status == self.status:
                raise ValidationError('Cannot change status to same status')

            if previous_status == 'completed':
                raise ValidationError('Cannot change status of completed charge')

        # IF STATUS IS COMPLETED

        if self.status == 'completed':
            wallet = self.user.get_user_wallet()
            available_balance = wallet.balance_available

            if available_balance < self.fee_amount:
                self.status = 'pending'
                raise ValidationError('Insufficient balance')

    def charge_wallet(self):
        wallet = self.user.get_user_wallet()
        self.status = 'completed'
        self.save()