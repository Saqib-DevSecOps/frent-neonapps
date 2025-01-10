from django.contrib import admin
from .models import (
    ServiceCategory, Service, ServiceImage,
    ServiceAvailability, ServiceReview, FavoriteService, ServiceBookingRequest, ServiceOrder, ServicePayment,
    ServiceCurrency, ServiceLocation
)


class ServiceImageInline(admin.TabularInline):
    """Inline for displaying Service Images in a tabular format."""
    model = ServiceImage
    extra = 1
    fields = ('image', 'is_active', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


class ServiceAvailabilityInline(admin.TabularInline):
    """Inline for displaying Service Availability Slots."""
    model = ServiceAvailability
    extra = 1
    fields = ('day_of_week', 'start_time', 'end_time', 'timezone', 'is_active', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


class ServiceLocationInline(admin.TabularInline):
    """Inline for displaying Service Locations."""
    model = ServiceLocation
    extra = 1
    fields = ('address', 'city', 'region', 'country', 'latitude', 'longitude', 'is_active')


class ServiceReviewInline(admin.TabularInline):
    """Inline for displaying Service Reviews."""
    model = ServiceReview
    extra = 1
    fields = ('reviewer', 'rating', 'comment', 'is_active', 'created_at')
    readonly_fields = ('created_at',)


class ServiceCategoryAdmin(admin.ModelAdmin):
    """Admin interface for ServiceCategory"""
    list_display = ('name', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('is_active',)


class ServiceCurrencyAdmin(admin.ModelAdmin):
    """Admin interface for ServiceCurrency"""
    list_display = ('name', 'code', 'symbol', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'code', 'symbol')
    list_filter = ('is_active',)


class ServiceAdmin(admin.ModelAdmin):
    """Admin interface for Service"""
    list_display = ('title', 'provider', 'category', 'price', 'currency', 'is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'provider__username', 'category__name', 'price', 'currency__name')
    list_filter = ('is_active', 'category', 'currency')
    inlines = [ServiceImageInline, ServiceAvailabilityInline, ServiceLocationInline, ServiceReviewInline]


class ServiceImageAdmin(admin.ModelAdmin):
    """Admin interface for ServiceImage"""
    list_display = ('service', 'image', 'is_active', 'created_at', 'updated_at')
    search_fields = ('service__title',)
    list_filter = ('is_active',)


class ServiceAvailabilityAdmin(admin.ModelAdmin):
    """Admin interface for ServiceAvailability"""
    list_display = (
        'service', 'day_of_week', 'start_time', 'end_time', 'timezone', 'is_active', 'created_at', 'updated_at')
    search_fields = ('service__title', 'day_of_week')
    list_filter = ('is_active', 'day_of_week')


class ServiceLocationAdmin(admin.ModelAdmin):
    """Admin interface for ServiceLocation"""
    list_display = ('service', 'address', 'city', 'region', 'country', 'latitude', 'longitude', 'is_active')
    search_fields = ('service__title', 'address', 'city__name', 'region__name', 'country__name')
    list_filter = ('is_active', 'city', 'region', 'country')


class ServiceReviewAdmin(admin.ModelAdmin):
    """Admin interface for ServiceReview"""
    list_display = ('service', 'reviewer', 'rating', 'is_active', 'created_at')
    search_fields = ('service__title', 'reviewer__username')
    list_filter = ('rating', 'is_active')


class ServiceBookingRequestAdmin(admin.ModelAdmin):
    """Admin panel for managing service booking requests."""
    list_display = ('user', 'service',  'start_datetime', 'end_datetime','status')
    list_filter = ('status',  'start_datetime', 'end_datetime',)
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


class FavoriteServiceAdmin(admin.ModelAdmin):
    """Admin interface for FavoriteService"""
    list_display = ('user', 'service', 'created_at')
    search_fields = ('user__username', 'service__title')
    list_filter = ('created_at',)


class ServiceAdvertisementAdmin(admin.ModelAdmin):
    list_display = ('service', 'user', 'service_type', 'start_datetime', 'end_datetime', 'created_at', 'updated_at')
    list_filter = ('service_type', 'created_at', 'updated_at')
    search_fields = ('service', 'user__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

class ServiceAdvertisementRequestAdmin(admin.ModelAdmin):
    list_display = ('advert', 'service_provider', 'service', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('advert__service', 'service_provider__name', 'service__name')
    ordering = ('-created_at',)

admin.site.register(ServiceCategory, ServiceCategoryAdmin)
admin.site.register(ServiceCurrency, ServiceCurrencyAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceImage, ServiceImageAdmin)
admin.site.register(ServiceAvailability, ServiceAvailabilityAdmin)
admin.site.register(ServiceLocation, ServiceLocationAdmin)
admin.site.register(ServiceReview, ServiceReviewAdmin)
admin.site.register(FavoriteService, FavoriteServiceAdmin)
admin.site.register(ServiceBookingRequest, ServiceBookingRequestAdmin)
admin.site.register(ServiceOrder, ServiceOrderAdmin)
admin.site.register(ServicePayment, ServicePaymentAdmin)
