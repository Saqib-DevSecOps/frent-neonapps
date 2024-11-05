from cities_light.models import City, Region, Country,SubRegion
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_otp.models import Device
from django_resized import ResizedImageField
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    """Custom User Model"""
    USER_TYPES = [
        ('admin', 'Admin'),
        ('service_provider', 'Service Provider'),
        ('service_seeker', 'Service Seeker'),
    ]

    email = models.EmailField(unique=True, max_length=200)
    profile_image = ResizedImageField(
        upload_to='users/images/profiles/', null=True, blank=True, size=[250, 250], quality=75, force_format='PNG',
        help_text='size of logo must be 250*250 and format must be png image file', crop=['middle', 'center']
    )
    bio = models.TextField(blank=True, null=True, help_text="Short description about the user.")
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='service_seeker')
    phone_number = PhoneNumberField(null=True, blank=True, unique=True)

    REQUIRED_FIELDS = ["username"]
    USERNAME_FIELD = "email"

    class Meta:
        ordering = ['-id']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def delete(self, *args, **kwargs):
        self.profile_image.delete(save=True)
        super(User, self).delete(*args, **kwargs)

    def get_service_provider_profile(self):
        if hasattr(self, 'service_provider_profile'):
            return self.service_provider_profile
        return None

    def save(self, *args, **kwargs):
        if self.is_staff:
            self.user_type = 'admin'
        return super(User, self).save(*args, **kwargs)

    def get_user_wallet(self):
        if hasattr(self, 'user_wallet'):
            return self.user_wallet
        return None



class ServiceProvider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='service_provider_profile',
                                verbose_name="User Account")
    company_name = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Company Name")

    phone_number = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Phone Number"
    )
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="City"
    )
    sub_region = models.ForeignKey(
        SubRegion, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Sub-Region"
    )
    region = models.ForeignKey(
        Region, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Region/State"
    )
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Country"
    )
    address = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Enter Address"
    )
    website = models.URLField(
        blank=True, null=True, verbose_name="Website"
    )

    rating = models.DecimalField(
        max_digits=3, decimal_places=2, default=0.00, verbose_name="Average Rating"
    )
    total_reviews = models.PositiveIntegerField(
        default=0, verbose_name="Total Reviews"
    )
    verified = models.BooleanField(
        default=False, help_text="Indicates whether the service provider is verified.", verbose_name="Verified Status"
    )
    status = models.CharField(
        max_length=20, choices=[
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ('suspended', 'Suspended')
        ], default='active', verbose_name="Account Status"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date Updated")

    def __str__(self):
        return f"{self.user.username} - {self.company_name or 'Independent'}"

    @property
    def average_rating(self):
        """Returns the average rating if available, otherwise indicates no reviews."""
        return self.rating if self.total_reviews > 0 else "No reviews"

    def update_rating(self, new_rating):
        """Update the service provider's rating based on new customer feedback.

        Args:
            new_rating (float): The new rating to add. Must be between 0 and 5.

        Raises:
            ValueError: If new_rating is not within the valid range (0-5).
        """
        if not (0 <= new_rating <= 5):
            raise ValueError("Rating must be between 0 and 5.")

        total_score = self.rating * self.total_reviews
        self.total_reviews += 1
        self.rating = (total_score + new_rating) / self.total_reviews
        self.save()

    class Meta:
        verbose_name = "Service Provider"
        verbose_name_plural = "Service Providers"
        ordering = ['-created_at']


class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True, related_name="user_profiles")
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True, related_name="user_profiles")
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True, related_name="user_profiles")
    zip_code = models.CharField(max_length=20, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ['-created_at']


class BlockedUser(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blocked_users',
        help_text="The user who blocked another user."
    )
    blocked_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blocked_by',
        help_text="The user who is being blocked."
    )
    reason = models.TextField(blank=True, null=True, help_text="Optional reason for blocking the user.")

    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time when the user was blocked.")
    updated_at = models.DateTimeField(auto_now=True, help_text="The date and time when the block was last updated.")

    class Meta:
        unique_together = ['user', 'blocked_user']
        verbose_name = 'Blocked User'
        verbose_name_plural = 'Blocked Users'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} blocked {self.blocked_user.username}"


class UserImages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')
    image = ResizedImageField(
        upload_to='users/images/', size=[800, 800], quality=75, force_format='PNG',
        help_text='size of logo must be 800*800 and format must be png image file', crop=['middle', 'center']
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'User Image'
        verbose_name_plural = 'User Images'
        ordering = ['-created_at']
