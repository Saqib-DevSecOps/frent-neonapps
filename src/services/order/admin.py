from django.contrib import admin
from .models import Advert, BookingRequest, Order, Payment


@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    list_display = ('user', 'service_type', 'service', 'created_at')
    list_filter = ('service_type', 'created_at')
    search_fields = ('service', 'user__username')
    ordering = ('-created_at',)


@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ('advert', 'service_provider', 'status', 'date_time', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('advert__service', 'service_provider__user__username')
    ordering = ('-created_at',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'service_provider', 'service', 'total_price', 'status', 'payment_status', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at')
    search_fields = ('user__username', 'service_provider__user__username')
    ordering = ('-created_at',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'order', 'amount', 'payment_method',
        'status', 'created_at'
    )
    list_filter = ('status', 'payment_method')
    search_fields = ('user__username', 'billing_email')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Payment Info', {
            'fields': ('user', 'order', 'amount', 'tax', 'total_price', 'payment_type', 'payment_method', 'status')
        }),
        ('Billing Details', {'fields': (
            'billing_first_name', 'billing_last_name', 'billing_address', 'billing_city',
            'billing_state', 'billing_zip', 'billing_country', 'billing_phone', 'billing_email'
        )}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),)
