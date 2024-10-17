from django.contrib import admin
from django.utils import timezone

from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'reported_by', 'report_type', 'reported_user', 'reported_service', 'is_resolved', 'created_at', 'resolved_at')
    list_filter = ('report_type', 'is_resolved', 'created_at')
    search_fields = ('reported_by__username', 'reported_user__username', 'reported_service__title', 'reason')
    readonly_fields = ('created_at', 'resolved_at')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('reported_by', 'report_type', 'reported_user', 'reported_service')
        }),
        ('Details', {
            'fields': ('reason', 'additional_info', 'created_at', 'is_resolved', 'resolved_at')
        }),
    )
    actions = ['mark_as_resolved']

    def mark_as_resolved(self, request, queryset):
        queryset.update(is_resolved=True, resolved_at=timezone.now())
        self.message_user(request, f"{queryset.count()} reports marked as resolved.")
    mark_as_resolved.short_description = "Mark selected reports as resolved"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('reported_by', 'reported_user', 'reported_service')

    def has_change_permission(self, request, obj=None):
        """Customize permissions to restrict changes to resolved reports."""
        if obj and obj.is_resolved:
            return False
        return super().has_change_permission(request, obj)
