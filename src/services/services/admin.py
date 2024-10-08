from django.contrib import admin
from .models import (
    ServiceCategory, Service, ServiceImage,
    ServiceAvailability, ServiceReview, ServiceRequest
)

# Admin for ServiceCategory
@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['name']

# Admin for Service
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'provider', 'category', 'price', 'is_active', 'created_at', 'updated_at']
    search_fields = ['title', 'provider__username']
    list_filter = ['is_active', 'category', 'provider']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['title']

# Inline model for ServiceImage in ServiceAdmin
class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 1

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
