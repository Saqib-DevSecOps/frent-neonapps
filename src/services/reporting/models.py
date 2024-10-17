from django.db import models
from django.utils import timezone

from src.services.services.models import Service
from src.services.users.models import User


class Report(models.Model):
    REPORT_TYPE_CHOICES = [
        ('user', 'User'),
        ('service', 'Service'),
    ]

    reported_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reports_made',
        help_text="The user who submitted the report."
    )
    report_type = models.CharField(
        max_length=20, choices=REPORT_TYPE_CHOICES, default='user',
        help_text="The type of report: either 'User' or 'Service'."
    )
    reported_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reports_received',
        null=True, blank=True,
        help_text="The user being reported, if applicable."
    )
    reported_service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name='service_reports',
        null=True, blank=True,
        help_text="The service being reported, if applicable."
    )
    reason = models.TextField(
        help_text="The reason for reporting. Provide as much detail as possible."
    )
    additional_info = models.TextField(
        blank=True, null=True,
        help_text="Optional additional information about the report."
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="The date and time when the report was created."
    )
    is_resolved = models.BooleanField(
        default=False,
        help_text="Indicates whether the report has been resolved."
    )
    resolved_at = models.DateTimeField(
        null=True, blank=True,
        help_text="The date and time when the report was resolved."
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'
        constraints = [
            models.CheckConstraint(
                check=models.Q(reported_user__isnull=False) | models.Q(reported_service__isnull=False),
                name='report_user_or_service_not_null'
            ),
            models.UniqueConstraint(
                fields=['reported_by', 'reported_user', 'reported_service'],
                name='unique_report_per_user_and_service'
            ),
        ]

    def __str__(self):
        if self.report_type == 'user' and self.reported_user:
            return f"Report by {self.reported_by.username} on User {self.reported_user.username}"
        elif self.report_type == 'service' and self.reported_service:
            return f"Report by {self.reported_by.username} on Service {self.reported_service.title}"
        return f"Report by {self.reported_by.username}"

    def resolve(self):
        """Mark the report as resolved and set the resolved_at timestamp."""
        self.is_resolved = True
        self.resolved_at = timezone.now()
        self.save()
