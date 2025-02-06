from django.contrib import admin

from src.services.order.models import AdvertisementRequest, Advertisement, Payment, ServiceBookingRequest, SpecialOffer, \
    Order


class ServiceAdvertisementAdmin(admin.ModelAdmin):
    list_display = ('service', 'user', 'service_type', 'start_datetime', 'end_datetime', 'created_at', 'updated_at')
    list_filter = ('service_type', 'created_at', 'updated_at')
    search_fields = ('service', 'user__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


class ServiceAdvertisementRequestAdmin(admin.ModelAdmin):
    list_display = ('advertisement', 'service_provider', 'service', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('advertisement__service',)
    ordering = ('-created_at',)


class ServiceBookingRequestAdmin(admin.ModelAdmin):
    """Admin panel for managing service booking requests."""
    list_display = ('user', 'service', 'start_datetime', 'end_datetime', 'status')
    list_filter = ('status', 'start_datetime', 'end_datetime',)
    search_fields = ('user__username', 'service__title')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


class ServiceOrderAdmin(admin.ModelAdmin):
    """Admin panel for managing service orders."""
    list_display = (
        'user', 'payment_type', 'total_price', 'paid_price', 'order_status', 'payment_status')
    list_filter = ('order_status', 'payment_status', 'payment_type')
    search_fields = ('user__username',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


class ServicePaymentAdmin(admin.ModelAdmin):
    """Admin panel for managing service payments."""
    list_display = ('user', 'order', 'amount', 'payment_method', 'created_at')
    list_filter = ('payment_method', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


class SpecialOfferAdmin(admin.ModelAdmin):
    """Admin panel for managing special offers."""
    list_display = (
        'user', 'service', 'service_day', 'start_time', 'end_time', 'service_fee', 'currency', 'status')
    list_filter = ('status', 'service_day', 'currency')
    search_fields = ('user__username', 'service__title')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(Order, ServiceOrderAdmin)
admin.site.register(Payment, ServicePaymentAdmin)
admin.site.register(Advertisement, ServiceAdvertisementAdmin)
admin.site.register(AdvertisementRequest, ServiceAdvertisementRequestAdmin)
admin.site.register(ServiceBookingRequest, ServiceBookingRequestAdmin)
admin.site.register(SpecialOffer, SpecialOfferAdmin)
