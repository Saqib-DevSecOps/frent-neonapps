import re

from dj_rest_auth.registration.serializers import RegisterSerializer
from django.db import models
from rest_framework import serializers

from src.services.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'pk', 'email', 'username', 'first_name', 'last_name'
        ]
        read_only_fields = ['pk', 'email']


class CustomLoginSerializer(serializers.Serializer):
    email = serializers.CharField(label='Email/Phone Number', max_length=20)
    password = serializers.CharField(label='Password', write_only=True)

    def validate_email(self, value):
        # Check if the value is a valid email or phone number
        if not self.is_valid_email(value) and not self.is_valid_phone(value):
            raise serializers.ValidationError("Email or Phone Number is not valid.")

        return value

    def is_valid_email(self, email):
        # Simple regex for validating email format
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None

    def is_valid_phone(self, phone):
        # Simple regex for validating phone number format (adjust as needed)
        phone_regex = r'^\+?[0-9]{10,15}$'  # Allows optional '+' and 10-15 digits
        return re.match(phone_regex, phone) is not None

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # Check if the username is an email or phone number
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
    phone_number = serializers.CharField(max_length=15, required=True)

    def validate_phone_number(self, value):
        # Validate phone number format
        if not self.is_valid_phone(value):
            raise serializers.ValidationError(
                "Phone number is not valid. It should contain only digits and be 10 to 15 characters long.")
        return value

    def is_valid_phone(self, phone):
        # Simple regex for validating phone number format (adjust as needed)
        phone_regex = r'^\+?[0-9]{10,15}$'  # Allows optional '+' and 10-15 digits
        return re.match(phone_regex, phone) is not None

    def save(self, request):
        user = super().save(request)
        user.phone_number = self.validated_data.get('phone_number')
        user.save()
        return user


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)
