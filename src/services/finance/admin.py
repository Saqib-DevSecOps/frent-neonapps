from django.contrib import admin

from .models import (
    BankAccount,
    PayPalAccount,
    Withdrawal
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