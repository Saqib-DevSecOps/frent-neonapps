from .models import Wallet, Transaction, Charge
from django.contrib import admin

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'stripe_account_id', 'stripe_account_email',
        'stripe_is_active', 'total_amounts', 'total_earnings',
        'balance_available', 'connect_available_balance', 'created_on'
    )
    list_filter = ('stripe_is_active', 'stripe_account_country')
    search_fields = ('user__username', 'stripe_account_email', 'stripe_account_id')
    readonly_fields = ('created_on', 'updated_on')
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
            'fields': ('created_on', 'updated_on')
        }),
    )
    ordering = ('-created_on',)



@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'transaction_type', 'amount', 'status', 'payment_type', 'created_on', 'updated_on')
    list_filter = ('transaction_type', 'status', 'payment_type', 'created_on')
    search_fields = ('user__username', 'description', 'transaction_type')
    readonly_fields = ('created_on', 'updated_on')

    fieldsets = (
        (None, {
            'fields': ('user', 'wallet', 'transaction_type', 'amount', 'fee', 'description')
        }),
        ('Payment Details', {
            'fields': ('payment_type', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_on', 'updated_on')
        }),
    )

    def has_change_permission(self, request, obj=None):
        if obj and obj.status == 'completed':
            return False
        return super().has_change_permission(request, obj)


@admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):
    list_display = ('user', 'fee_amount', 'fee_type', 'status', 'is_active', 'created_on', 'updated_on')
    search_fields = ('user__username', 'user__email', 'fee_type')
    list_filter = ('fee_type', 'status', 'is_active', 'created_on')
    readonly_fields = ('created_on', 'updated_on')

    def get_readonly_fields(self, request, obj=None):
        """
        Prevent modification of the status if the charge is completed.
        """
        if obj:
            previous_status = obj.status
            if previous_status == 'completed':
                return self.readonly_fields + ('status', 'user', 'fee_amount', 'fee_type', 'currency')
        return self.readonly_fields
