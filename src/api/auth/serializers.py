import re

from dj_rest_auth.registration.serializers import RegisterSerializer
from django.db import models
from rest_framework import serializers

from src.services.users.models import User


class ValidationMixin:
    """Mixin to provide reusable email and phone number validation."""

    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    phone_regex = r'^\+?[0-9]{10,15}$'

    def is_valid_email(self, email):
        """Validate email format."""
        return re.match(self.email_regex, email) is not None

    def is_valid_phone(self, phone):
        """Validate phone number format."""
        return re.match(self.phone_regex, phone) is not None


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user details."""

    class Meta:
        model = User
        fields = ['pk', 'email', 'username', 'first_name', 'last_name']
        read_only_fields = ['pk', 'email']


class CustomLoginSerializer(serializers.Serializer, ValidationMixin):
    """Custom serializer for login with email or phone number."""

    email = serializers.CharField(label='Email/Phone Number', max_length=50)
    password = serializers.CharField(label='Password', write_only=True)

    def validate_email(self, value):
        """Validate email or phone number field."""
        if not self.is_valid_email(value) and not self.is_valid_phone(value):
            raise serializers.ValidationError("Email or Phone Number is not valid.")
        return value

    def validate(self, attrs):
        """Validate login credentials."""
        email = attrs.get('email')
        password = attrs.get('password')

        # Check if the input is an email or phone number
        user = User.objects.filter(
            models.Q(email=email) | models.Q(phone_number=email)
        ).first()

        if user is None:
            raise serializers.ValidationError("Unable to log in with provided credentials.")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials")

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        attrs['user'] = user
        return attrs


class CustomRegisterSerializer(RegisterSerializer):
    """Custom serializer for user registration."""

    phone_number = serializers.CharField(max_length=15, required=True)

    def validate_email(self, email):
        """Validate unique email."""
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email is already registered.")
        return email

    def validate_phone_number(self, value):
        """Validate unique phone number and phone number format."""
        # Check for uniqueness
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("This phone number is already registered.")

        # Validate phone number format (only digits, 10-15 characters)
        if not value.isdigit() or not (10 <= len(value) <= 15):
            raise serializers.ValidationError(
                "Phone number is not valid. It should contain only digits and be 10 to 15 characters long."
            )
        return value


class PasswordSerializer(serializers.Serializer):
    """Serializer for password input."""

    password = serializers.CharField(required=True, write_only=True)
