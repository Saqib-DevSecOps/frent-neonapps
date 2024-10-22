from django.contrib import admin
from .models import (
    ServiceCategory, Service, ServiceImage,
    ServiceAvailability, ServiceReview, ServiceRequest, FavoriteService
)


class ServiceImageInline(admin.TabularInline):
    """Inline for displaying Service Images in a tabular format."""
    model = ServiceImage
    extra = 1
    fields = ('image', 'is_active', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


class ServiceAvailabilityInline(admin.TabularInline):
    """Inline for displaying Service Availabilities."""
    model = ServiceAvailability
    extra = 1
    fields = ('day_of_week', 'start_time', 'end_time', 'timezone', 'is_active')
    ordering = ['day_of_week', 'start_time']


class ServiceReviewInline(admin.TabularInline):
    """Inline for displaying Service Reviews."""
    model = ServiceReview
    extra = 1
    fields = ('reviewer', 'rating', 'comment', 'is_active', 'created_at')
    readonly_fields = ('created_at',)


class ServiceRequestInline(admin.TabularInline):
    """Inline for displaying Service Requests."""
    model = ServiceRequest
    extra = 1
    fields = ('seeker', 'status', 'requested_at', 'is_paid')
    readonly_fields = ('requested_at',)


class FavoriteServiceInline(admin.TabularInline):
    """Inline for displaying Favorite Services."""
    model = FavoriteService
    extra = 1
    fields = ('user', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


# Admin for ServiceCategory
@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['name']


# Add the inline to ServiceAdmin
@admin.register(ServiceImage)
class ServiceImageAdmin(admin.ModelAdmin):
    list_display = ['service', 'is_active']
    search_fields = ['service__title']
    list_filter = ['is_active']
    readonly_fields = ['created_at', 'updated_at']


# Admin for ServiceAvailability
@admin.register(ServiceAvailability)
class ServiceAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['service', 'day_of_week', 'start_time', 'end_time', 'timezone', 'is_active']
    search_fields = ['service__title', 'day_of_week']
    list_filter = ['day_of_week', 'is_active']
    readonly_fields = ['created_at', 'updated_at']


# Admin for ServiceReview
@admin.register(ServiceReview)
class ServiceReviewAdmin(admin.ModelAdmin):
    list_display = ['service', 'reviewer', 'rating', 'is_active', 'created_at']
    search_fields = ['service__title', 'reviewer__username']
    list_filter = ['rating', 'is_active']
    readonly_fields = ['created_at']
    ordering = ['-created_at']


# Admin for ServiceRequest
@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ['seeker', 'service', 'status', 'requested_at', 'completed_at', 'cancelled_at', 'is_paid']
    search_fields = ['seeker__username', 'service__title']
    list_filter = ['status', 'is_paid']
    readonly_fields = ['requested_at', 'completed_at', 'cancelled_at']
    ordering = ['-requested_at']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Admin for managing Services with related inlines."""
    list_display = ('title', 'provider', 'category', 'is_active', 'price')
    search_fields = ('title', 'provider__username', 'category__name')
    inlines = [
        ServiceImageInline,
        ServiceAvailabilityInline,
        ServiceReviewInline,
        ServiceRequestInline,
        FavoriteServiceInline,
    ]
