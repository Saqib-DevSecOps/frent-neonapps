from django.contrib import messages
from django.core.paginator import Paginator
from django.views import View
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from payments import get_payment_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from src.apps.stripe.bll import (
    stripe_connect_account_create, stripe_connect_account_link,
    update_subscription_record,
    update_price_list
)
from .filters import StripeCustomerFilter
from .models import StripeCustomer, Product as StripeProduct
from .notifier import notify_subscriptions_created
from .webhook_core import hooks_view
from django.urls import reverse
import stripe

Payment = get_payment_model()

""" VENDOR VIEWS FOR STRIPE -------------------------------------------------------------------------------------- """


@method_decorator(login_required, name='dispatch')
class ConnectWalletView(View):

    def get(self, request, *args, **kwargs):
        if not request.user.country:
            messages.error(request, 'You have not provided your country, kindly update your first')
            return redirect("vendor:account_change")

        return render(request, 'stripe/connect_wallet.html')


@method_decorator(login_required, name='dispatch')
class ConnectWalletCreateView(View):

    def get(self, request, *args, **kwargs):
        user = request.user

        # Show warning message if user already connected wallet
        if user.is_stripe_connected():
            messages.warning(request, 'You have already connected your wallet')
            return redirect(request.META.get('HTTP_REFERER'))

        error, account = stripe_connect_account_create(user)

        # Show error message if error occurred
        if error:
            messages.error(request, error)
            return redirect(request.META.get('HTTP_REFERER'))

        # Successfully connected wallet
        messages.success(request, 'Your wallet has been connected successfully')
        return redirect(request.META.get('HTTP_REFERER'))


@method_decorator(login_required, name='dispatch')
class ConnectWalletVisitView(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        wallet = user.get_user_wallet()

        # Show warning message if user ie not connected
        if not user.is_stripe_connected():
            messages.warning(request, 'You have not connected your wallet')
            return redirect(request.META.get('HTTP_REFERER'))

        error, url = stripe_connect_account_link(wallet.stripe_account_id)

        # Show error message if error occurred
        if error:
            messages.error(request, error)
            return redirect(request.META.get('HTTP_REFERER'))

        # Successfully connected wallet
        return redirect(url)


""" CUSTOMER VIEWS FOR STRIPE ------------------------------------------------------------------------------------- """


@method_decorator(login_required, name='dispatch')
class SubscriptionCreateView(View):

    def post(self, request, *args, **kwargs):
        """
        1: get key of package
        2: perform verifications > already subscribed or not > yes: detail > else: checkout
        3: get user model : get price model: get package model
        4: --
        5: --
        """
        # GET KEYS
        key = request.POST.get('key')

        # VERIFICATIONS
        if not key:
            messages.error(request, "Invalid request")
            return redirect("website:packages")

        # CREATE CUSTOMER IF NOT EXISTS
        if StripeCustomer.objects.filter(user=request.user).exists():
            messages.error(request, "you are already subscribed to a package.")
            return redirect("stripe:subscription-detail")

        # CHECKOUT
        success_url = request.build_absolute_uri(
            reverse("payments:subscription-success")
        ) + "?session_id={CHECKOUT_SESSION_ID}"
        failure_url = request.build_absolute_uri(
            reverse("payments:subscription-failure")
        ) + "?session_id={CHECKOUT_SESSION_ID}"

        session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': key,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=success_url,
            cancel_url=failure_url,
        )
        return redirect(session.url, code=303)


@method_decorator(login_required, name='dispatch')
class SubscriptionDetailView(View):
    template_name = 'stripe/subscription.html'

    def get(self, request):
        if not StripeCustomer.objects.filter(user=request.user).exists():
            messages.warning(request, "you didn't subscribed to any package yet.")
            return redirect("stripe:subscription-create")

        customer = StripeCustomer.objects.filter(user=request.user)[0]
        return render(request, self.template_name, {'customer': customer})


@method_decorator(login_required, name='dispatch')
class SubscriptionPortalLinkView(View):
    def get(self, request, *args, **kwargs):
        return_url = request.build_absolute_uri(
            reverse("payments:subscription-detail")
        )

        if not StripeCustomer.objects.filter(user=request.user).exists():
            messages.warning(request, "you didn't subscribed to any package yet.")
            return redirect("stripe:subscription-create")

        customer = StripeCustomer.objects.filter(user=request.user)[0]
        portal_session = stripe.billing_portal.Session.create(
            customer=customer.customer_id,
            return_url=return_url,
        )

        return redirect(portal_session.url, code=303)


@method_decorator(login_required, name='dispatch')
class SubscriptionSuccessView(View):

    def get(self, request):
        stripe_id = request.GET.get('session_id')
        session = stripe.checkout.Session.retrieve(stripe_id)
        customer = StripeCustomer.objects.get_or_create(
            user=request.user, subscription_id=session['subscription'], customer_id=session['customer']
        )
        success, obj = update_subscription_record(session['subscription'])

        # NOTIFY
        notify_subscriptions_created(obj)
        return render(request, 'stripe/subscription_success.html')


@method_decorator(login_required, name='dispatch')
class SubscriptionFailureView(View):
    template_name = 'stripe/subscription_failure.html'

    def get(self, request):
        stripe_id = request.GET.get('session_id')
        # session = stripe.checkout.Session.retrieve(stripe_id)
        return render(request, self.template_name)


""" ADMIN VIEWS --------------------------------------------------------------------------------------------------- """


@method_decorator(login_required, name='dispatch')
class SubscriptionListView(ListView):
    queryset = StripeCustomer.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SubscriptionListView, self).get_context_data(**kwargs)
        filter_form = StripeCustomerFilter(self.request.GET, queryset=self.queryset)
        context['filter_form'] = filter_form.form

        paginator = Paginator(filter_form.qs, 50)
        page_number = self.request.GET.get('page')
        page_object = paginator.get_page(page_number)

        context['object_list'] = page_object
        return context


@method_decorator(login_required, name='dispatch')
class ProductListView(ListView):
    model = StripeProduct


@method_decorator(login_required, name='dispatch')
class ProductRefreshView(View):

    def get(self, request, *args, **kwargs):
        success, message = update_price_list()
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)
        return redirect("stripe:product-list")


""" WEBHOOK VIEWS FOR STRIPE -------------------------------------------------------------------------------------- """


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebHook(View):

    def post(self, request, *args, **kwargs):
        return hooks_view(request)
