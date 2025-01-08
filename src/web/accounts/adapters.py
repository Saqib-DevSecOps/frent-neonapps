import random

from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailConfirmation
from django.shortcuts import resolve_url
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone


class MyAccountAdapter(DefaultAccountAdapter):

    def get_signup_redirect_url(self, request):
        return resolve_url('account_set_password')

    def get_login_redirect_url(self, request):
        # Check if the user has a usable password
        user = request.user
        if user.is_authenticated and user.has_usable_password():
            return resolve_url('/')

        else:
            return resolve_url('account_set_password')

    def respond_user_authenticated(self, request, user):
        """
        Called when a user is authenticated successfully.
        """
        # Redirect based on whether the user has a usable password
        if user.has_usable_password():
            return HttpResponseRedirect(reverse('account_set_password'))
        else:
            return HttpResponseRedirect(reverse('/'))

    def send_sms(self, request, user):
        # Send SMS
        pass

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        # Generate the verification key
        verification_key = str(random.randint(100000, 999999))

        # Get or create EmailConfirmation
        emailconfirmation, created = EmailConfirmation.objects.get_or_create(
            email_address=emailconfirmation.email_address,
            defaults={'key': verification_key}  # Set the key only if the object is created
        )
        emailconfirmation.sent = timezone.now()
        emailconfirmation.save()

        # Prepare the email context
        context = {
            "user": emailconfirmation.email_address.user,
            "key": verification_key,
        }

        # Send the custom email with the verification key
        self.send_mail("account/email/email_verification_key", emailconfirmation.email_address.email, context)

    def get_email_confirmation_url(self, request, emailconfirmation):
        return emailconfirmation.key
