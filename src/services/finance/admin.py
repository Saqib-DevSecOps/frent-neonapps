from django.contrib import admin

from .models import (
    BankAccount,
    PayPalAccount, Transaction,
    Withdrawal, Wallet, Charge,
)


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'account_holder_name', 'bank_name', 'iban', 'currency', 'status', 'is_active', 'created_at'
    ]


@admin.register(PayPalAccount)
class PayPalAccountAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'account_holder_name', 'email', 'status', 'is_active', 'created_at'
    ]


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'amount', 'status', 'created_at'
    ]


@admin.register(Transaction)
class Transaction(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'amount', 'status', 'created_at'
    ]


@admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'fee_amount', 'fee_type', 'currency', 'status', 'created_at'
    ]


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'total_amounts', 'total_deposits', 'total_earnings', 'total_withdrawals',
        'balance_available', 'balance_pending', 'outstanding_charges', 'connect_pending_balance',
        'connect_available_balance', 'connect_available_balance_currency', 'connect_pending_balance_currency'
    ]
