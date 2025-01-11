from .models import Wallet, Transaction, Bank, BankAccount
from django.contrib import admin


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'stripe_account_id', 'stripe_account_email',
        'stripe_is_active', 'total_amounts', 'total_earnings',
        'balance_available', 'connect_available_balance', 'created_at'
    )
    list_filter = ('stripe_is_active', 'stripe_account_country')
    search_fields = ('user__username', 'stripe_account_email', 'stripe_account_id')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'description')
        }),
        ('Stripe Details', {
            'fields': (
                'stripe_account_id', 'stripe_account_type',
                'stripe_account_country', 'stripe_account_email',
                'stripe_description', 'stripe_is_active'
            )
        }),
        ('Overall Report', {
            'fields': (
                'total_amounts', 'total_deposits', 'total_earnings',
                'total_withdrawals'
            )
        }),
        ('Balance Report', {
            'fields': (
                'balance_available', 'balance_pending',
                'outstanding_charges'
            )
        }),
        ('Connect Report', {
            'fields': (
                'connect_available_balance',
                'connect_available_balance_currency',
                'connect_pending_balance',
                'connect_pending_balance_currency'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    ordering = ('-created_at',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'transaction_type', 'amount', 'status', 'payment_type', 'created_at', 'updated_at')
    list_filter = ('transaction_type', 'status', 'payment_type', 'created_at')
    search_fields = ('user__username', 'description', 'transaction_type')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('user', 'wallet', 'transaction_type', 'amount', 'fee', 'description')
        }),
        ('Payment Details', {
            'fields': ('payment_type', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def has_change_permission(self, request, obj=None):
        if obj and obj.status == 'completed':
            return False
        return super().has_change_permission(request, obj)


class BankAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('created_at',)
    date_hierarchy = 'created_at'


class BankAccountAdmin(admin.ModelAdmin):
    list_display = (
        'account_holder_name', 'account_number', 'bank',
        'account_type', 'account_currency', 'is_active', 'created_at'
    )
    list_filter = ('account_type', 'is_active', 'account_currency')
    search_fields = ('account_holder_name', 'account_number', 'bank__name')
    ordering = ('created_at',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Account Information', {
            'fields': (
                'user', 'account_holder_name', 'account_number',
                'account_iban', 'account_type', 'account_currency',
                'swift_code', 'routing_number'
            )
        }),
        ('Bank Details', {
            'fields': (
                'bank', 'country', 'bank_city', 'bank_address',
                'bank_postal_code'
            )
        }),
        ('Status', {
            'fields': ('is_active', 'created_at')
        }),
    )


admin.site.register(Bank, BankAdmin)
admin.site.register(BankAccount, BankAccountAdmin)
