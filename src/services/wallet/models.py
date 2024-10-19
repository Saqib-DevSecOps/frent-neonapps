from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models

from src.services.users.models import User


# Create your models here.
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_wallet')
    description = models.TextField(null=True, blank=True)

    # OVERALL REPORT
    total_amounts = models.FloatField(default=0)
    total_deposits = models.FloatField(default=0)
    total_earnings = models.FloatField(default=0)
    total_withdrawals = models.FloatField(default=0)

    # BALANCE REPORT
    balance_available = models.FloatField(default=0)
    balance_pending = models.FloatField(default=0)
    outstanding_charges = models.FloatField(default=0)

    # DATES
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = 'Wallets'

    def __str__(self):
        return str(self.pk)

    def get_available_balance(self):
        return self.balance_available

    def get_pending_balance(self):
        return self.balance_pending


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
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    PAYMENT_TYPE = (
        ('connect', 'Connect'),
        ('paypal', 'Paypal'),
        ('bank_account', 'Bank Account'),
    )

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='financial_transactions'
    )
    wallet = models.ForeignKey(
        'Wallet', on_delete=models.CASCADE, null=True, blank=True, related_name='financial_transactions'
    )
    amount = models.FloatField(default=0, verbose_name='Amount')
    fee = models.FloatField(default=0, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    transaction_type = models.CharField(
        max_length=50, choices=TRANSACTION_TYPE, default='deposit'
    )
    status = models.CharField(max_length=50, choices=STATUS_TYPE, default='pending')
    payment_type = models.CharField(
        max_length=50, choices=PAYMENT_TYPE, null=True, blank=True
    )

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f"{self.transaction_type} - {self.pk}"

    def clean(self):
        # AMOUNT CHECK
        if self.amount <= 0:
            raise ValidationError('Amount must be greater than 0')

        # USER MUST HAVE WALLET
        if self.transaction_type in ['withdrawal', 'charge']:
            if not self.wallet:
                raise ValidationError('Wallet is required for withdrawals or charges')
            if self.wallet.balance_available < self.amount:
                raise ValidationError('Insufficient balance to perform this transaction')

        # IF ALREADY EXISTS THEN DON'T ALLOW TO CHANGE STATUS TO ANOTHER
        if self.pk:
            previous_status = Transaction.objects.get(pk=self.pk).status
            if previous_status == 'completed' and self.status != 'completed':
                raise ValidationError("Completed transactions cannot be modified")

    def process_transaction(self):
        # Handle transaction processing
        if self.transaction_type == 'withdrawal':
            self._handle_withdrawal()
        elif self.transaction_type == 'deposit':
            self._handle_deposit()

        # Save the updated status
        self.status = 'completed'
        self.save()

    def _handle_withdrawal(self):
        # Deduct the amount from the wallet's available balance
        if self.wallet and self.wallet.balance_available >= self.amount:
            self.wallet.balance_available -= self.amount
            self.wallet.save()

    def _handle_deposit(self):
        # Add the amount to the wallet's available balance
        if self.wallet:
            self.wallet.balance_available += self.amount
            self.wallet.save()


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
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Charge'
        verbose_name_plural = 'Charges'
        ordering = ['-created_on']

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
