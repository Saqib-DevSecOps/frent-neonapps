from django.contrib import admin
from .models import Wallet, Transaction, Charge


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance_available', 'balance_pending', 'total_amounts', 'created_on', 'updated_on')
    search_fields = ('user__username', 'user__email')
    readonly_fields = (
    'created_on', 'updated_on', 'balance_available', 'balance_pending', 'total_amounts', 'total_deposits',
    'total_earnings', 'total_withdrawals', 'outstanding_charges')
    list_filter = ('created_on',)

    def get_readonly_fields(self, request, obj=None):
        """
        Make all fields read-only when editing an existing object.
        """
        if obj:
            return self.readonly_fields + ('user',)
        return self.readonly_fields


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
