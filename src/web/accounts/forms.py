import re

from allauth.account.forms import SignupForm, LoginForm
from django import forms
from django.db import models
from django.forms import ModelForm

from src.services.users.models import User


class UserProfileForm(ModelForm):
    """Form for updating user profile details."""

    class Meta:
        model = User
        fields = ['profile_image', 'first_name', 'last_name', 'phone_number']


class CustomFormMixin:
    """Mixin to provide reusable validation for phone numbers and emails."""

    phone_regex = r'^\+?[0-9]{10,15}$'
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    def is_valid_phone(self, phone_number):
        """Validate the phone number format."""
        return re.match(self.phone_regex, phone_number) is not None

    def is_valid_email(self, email):
        """Validate the email format."""
        return re.match(self.email_regex, email) is not None


class CustomSignUpForm(SignupForm, CustomFormMixin):
    """Custom form for user registration."""

    email = forms.EmailField(
        max_length=254,
        help_text=' Please provide a valid email address.',
        required=True
    )
    phone_number = forms.CharField(
        max_length=15,
        required=True,
        help_text='Please provide a valid phone number.'
    )

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'password1', 'password2']

    def clean_phone_number(self):
        """Validate and clean the phone number field."""
        phone_number = self.cleaned_data.get('phone_number')
        if not self.is_valid_phone(phone_number):
            raise forms.ValidationError("Invalid phone number format.")
        return phone_number


class CustomLoginForm(forms.ModelForm,CustomFormMixin):
    """Custom login form that allows login via email or phone number."""

    email = forms.CharField(
        max_length=254,
        label="Email or Phone Number"
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Password"
    )

    class Meta:
        model = User
        fields = ['email', 'password']

    def clean(self):
        """Custom validation for login credentials."""
        cleaned_data = super().clean()
        email_or_phone = cleaned_data.get('email_or_phone')
        password = cleaned_data.get('password')

        user = User.objects.filter(
            models.Q(email=email_or_phone) | models.Q(phone_number=email_or_phone)
        ).first()

        if not user:
            raise forms.ValidationError("No account found with the provided email/phone number.")

        if not user.check_password(password):
            raise forms.ValidationError("Incorrect password. Please try again.")

        return cleaned_data
