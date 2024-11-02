from django.contrib import admin
from .models import StripeCustomer, ExternalAccount, Transfer, Payout, Price, Product


@admin.register(ExternalAccount)
class ExternalAccountAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'account_id', 'user', 'object', 'country', 'last4', 'is_active'
    ]


@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'destination', 'amount', 'currency', 'failure_code', 'status', 'created', 'status'
    ]


@admin.register(StripeCustomer)
class StripeCustomerAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'customer_id', 'subscription_id', 'price_id',
        'subscription_start', 'subscription_end', 'subscription_status'
    ]


admin.site.register(Transfer)
admin.site.register(Price)
admin.site.register(Product)
