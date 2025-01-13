import uuid
from django.db import models
from src.services.services.models import Service
from src.services.users.models import ServiceProvider, User


class Advertisement(models.Model):
    """Stores advertisements for services"""
    SERVICE_TYPES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES, default='online')
    service = models.CharField(max_length=255, help_text="Service Name or Category")
    start_datetime = models.DateTimeField(
        help_text="The starting date and time for the service.",
        null=True, blank=True
    )
    end_datetime = models.DateTimeField(
        help_text="The ending date and time for the service.",
        null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.service} for {self.service.title}"

    def get_total_requests(self):
        return AdvertisementRequest.objects.filter(advertisement=self).count()

    class Meta:
        ordering = ['service']


class AdvertisementRequest(models.Model):
    """Stores requests for services"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.advertisement.service} - {self.service_provider}"

    def get_service_name(self):
        return self.advertisement.service


class ServiceBookingRequest(models.Model):
    """Tracks requests made for services"""
    REQUEST_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_requests')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='requests')
    start_datetime = models.DateTimeField(
        help_text="The starting date and time for the service.",
        null=True, blank=True
    )
    end_datetime = models.DateTimeField(
        help_text="The ending date and time for the service.",
        null=True, blank=True
    )
    message = models.TextField(blank=True, null=True, help_text="Additional notes for the request.")

    status = models.CharField(max_length=20, choices=REQUEST_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s request for {self.service.title}"


class Order(models.Model):
    """Tracks Orders made for services"""
    PAYMENT_TYPE_CHOICES = [
        ('full', 'Full Payment'),
        ('partial', 'Partial Payment'),
    ]
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_payments')

    service_booking_request = models.ForeignKey(ServiceBookingRequest, on_delete=models.SET_NULL, null=True, blank=True,
                                                related_name='service_booking_request')
    service_advertisement_request = models.ForeignKey(AdvertisementRequest, on_delete=models.SET_NULL, null=True,
                                                      blank=True, related_name='service_advertisement_request')

    payment_type = models.CharField(max_length=50, choices=PAYMENT_TYPE_CHOICES, default='full',
                                    help_text="Payment type for the service payment.")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    paid_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tip = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s order for {self.get_service}"

    def remaining_price(self):
        return self.total_price - self.paid_price

    @property
    def get_service(self):
        return self.service_booking_request.service if self.service_booking_request else self.service_advertisement_request.service


class Payment(models.Model):
    payment_methods = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('by_cash', 'By Cash'),
    ]
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    service_charges = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    payment_method = models.CharField(max_length=20, choices=payment_methods, default='credit_card')

    billing_first_name = models.CharField(max_length=255, blank=True, null=True)
    billing_last_name = models.CharField(max_length=255, blank=True, null=True)
    billing_address = models.TextField(blank=True, null=True)
    billing_city = models.CharField(max_length=255, blank=True, null=True)
    billing_state = models.CharField(max_length=255, blank=True, null=True)
    billing_zip = models.CharField(max_length=255, blank=True, null=True)
    billing_country = models.CharField(max_length=255, blank=True, null=True)
    billing_phone = models.CharField(max_length=20, blank=True, null=True)
    billing_email = models.EmailField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.order} - {self.amount}"

    class Meta:
        ordering = ['-created_at']
