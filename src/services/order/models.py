from django.db import models

from src.services.services.models import Service


# Create your models here.

class Advert(models.Model):
    SERVICE_TYPES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES, default='online')
    service = models.CharField(max_length=255, help_text="Service Name or Category")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.service


STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
]


class BookingRequest(models.Model):
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE)
    service_provider = models.ForeignKey('users.ServiceProvider', on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    date_time = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.advert.service} - {self.service_provider}"

    def get_service_name(self):
        return self.advert.service


class Order(models.Model):
    PAYMENT_TYPES = [
        ('full', 'Full Payment'),
        ('partial', 'Partial Payment'),
    ]

    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    service_provider = models.ForeignKey('users.ServiceProvider', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    paid_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    tax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    service_charge = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tip = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES, default='full')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def discounted_price(self):
        return self.total_price - (self.total_price * self.discount / 100)

    def remaining_price(self):
        return self.discounted_price() - self.paid_price

    def __str__(self):
        return f"{self.user} - {self.service_provider} - {self.service}"


class Payment(models.Model):
    payment_methods = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('by_cash', 'By Cash'),
    ]
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payment_type = models.CharField(max_length=20, choices=Order.PAYMENT_TYPES, default='full')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    payment_method = models.CharField(max_length=20, choices=payment_methods, default='credit_card')
    status = models.CharField(max_length=20, choices=Order.PAYMENT_STATUS, default='pending')

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

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.order} - {self.amount}"
