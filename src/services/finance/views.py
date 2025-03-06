from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, UpdateView

from .filters import WithdrawalFilter, BankAccountFilter, PaypalAccountFilter, TransactionFilter, ChargeFilter
from .forms import (
    WithdrawalForm, BankAccountForm, PaypalAccountForm
)
from .models import (
    PayPalAccount, BankAccount, Withdrawal, Transaction, Charge
)
from ...apps.stripe.models import ExternalAccount


class FinanceDashboard(TemplateView):
    template_name = 'finance/dashboard.html'


class PayoutMethodView(TemplateView):
    template_name = 'finance/payout-methods.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paypal_account = PayPalAccount.objects.filter(user=self.request.user)
        bank_account = BankAccount.objects.filter(user=self.request.user)
        user = self.request.user

        paypal_account = paypal_account[0] if paypal_account.exists() else None
        bank_account = bank_account[0] if bank_account.exists() else None

        wallet = user.get_user_wallet()
        context['wallet'] = wallet
        context['paypal_account'] = paypal_account
        context['bank_account'] = bank_account

        return context


""" FINANCE ACCOUNTS """


class ConnectAccountView(TemplateView):
    template_name = 'finance/connect_account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wallet = self.request.user.get_user_wallet()

        if wallet.is_stripe_connected():
            external_accounts = ExternalAccount.objects.filter(user=self.request.user)

            context['external_accounts'] = external_accounts
            context['connect_available_balance'] = wallet.connect_available_balance
            context['connect_pending_balance'] = wallet.connect_pending_balance
            context['connect_available_balance_currency'] = wallet.connect_available_balance_currency
            context['connect_pending_balance_currency'] = wallet.connect_pending_balance_currency

        return context


class BankAccountCreateView(CreateView):
    model = BankAccount
    form_class = BankAccountForm
    success_url = reverse_lazy("finance:payout-method")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the user to the form
        return kwargs


class BankAccountDeleteView(DeleteView):
    model = BankAccount
    success_url = reverse_lazy("finance:payout-method")


class PaypalAccountCreateView(CreateView):
    model = PayPalAccount
    form_class = PaypalAccountForm
    success_url = reverse_lazy("finance:payout-method")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the user to the form
        return kwargs


class PaypalAccountDeleteView(DeleteView):
    model = PayPalAccount
    success_url = reverse_lazy("finance:payout-method")


""" WITHDRAWALS """


class WithdrawalCreateView(CreateView):
    model = Withdrawal
    form_class = WithdrawalForm
    template_name = 'finance/withdrawal_form.html'  # specify your template
    success_url = reverse_lazy("finance:withdrawal-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the user to the form
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user  # Attach the user before validation
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wallet'] = self.request.user.get_user_wallet()
        return context


class WithdrawalListView(ListView):
    model = Withdrawal
    paginate_by = 50

    def get_template_names(self):
        if self.request.user.is_vendor:
            return "finance/withdrawal_list.html"
        return "finance/admins/withdrawal_list.html"

    def get_queryset(self):
        if self.request.user.is_vendor:
            return Withdrawal.objects.filter(user=self.request.user)
        return Withdrawal.objects.all()

    def get_context_data(self, **kwargs):
        context = super(WithdrawalListView, self).get_context_data(**kwargs)
        _filter = WithdrawalFilter(self.request.GET, queryset=self.get_queryset())
        context['filter_form'] = _filter.form

        paginator = Paginator(_filter.qs, self.paginate_by)
        page_number = self.request.GET.get('page')
        user_page_object = paginator.get_page(page_number)

        context['object_list'] = user_page_object
        return context


""" ADMIN VIEWS """


class BankAccountUpdateView(UpdateView):
    model = BankAccount
    fields = [
        'description', 'status'
    ]
    success_url = reverse_lazy("finance:payout-method")


class BankAccountUpdateView(UpdateView):
    template_name = 'finance/admins/bankaccount_form.html'
    model = BankAccount
    fields = [
        'description', 'status'
    ]
    success_url = reverse_lazy("finance:bank-account-list")


class PaypalAccountUpdateView(UpdateView):
    template_name = 'finance/admins/paypalaccount_form.html'
    model = PayPalAccount
    fields = [
        'description', 'status'
    ]
    success_url = reverse_lazy("finance:paypal-account-list")


class WithdrawalUpdateView(UpdateView):
    template_name = 'finance/admins/withdrawal_form.html'
    model = Withdrawal
    fields = [
        'description', 'status'
    ]
    success_url = reverse_lazy("finance:withdrawal-list")


class BankAccountListView(ListView):
    queryset = BankAccount.objects.all()

    def get_context_data(self, **kwargs):
        context = super(BankAccountListView, self).get_context_data(**kwargs)
        _filter = BankAccountFilter(self.request.GET, queryset=self.get_queryset())
        context['filter_form'] = _filter.form

        paginator = Paginator(_filter.qs, 50)
        page_number = self.request.GET.get('page')
        user_page_object = paginator.get_page(page_number)

        context['object_list'] = user_page_object
        return context


class PaypalAccountListView(ListView):
    queryset = PayPalAccount.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PaypalAccountListView, self).get_context_data(**kwargs)
        _filter = PaypalAccountFilter(self.request.GET, queryset=self.queryset)
        context['filter_form'] = _filter.form

        paginator = Paginator(_filter.qs, 50)
        page_number = self.request.GET.get('page')
        user_page_object = paginator.get_page(page_number)

        context['object_list'] = user_page_object
        return context


""" HESHAM """
class _WithdrawalListView(ListView):
    model = Withdrawal

    def get_template_names(self):
        return 'finance/_withdrawal_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(_WithdrawalListView, self).get_context_data(**kwargs)
        withdrawal_filter = WithdrawalFilter(self.request.GET, queryset=self.get_queryset())
        paginator = Paginator(withdrawal_filter.qs, 30)
        page_number = self.request.GET.get('page')
        withdrawal_page_object = paginator.get_page(page_number)
        context['filter_form'] = withdrawal_filter.form
        context['object_list'] = withdrawal_page_object
        return context

class TransactionListView(ListView):
    model = Transaction

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TransactionListView, self).get_context_data(**kwargs)
        transaction_filter = TransactionFilter(self.request.GET, queryset=self.get_queryset())
        paginator = Paginator(transaction_filter.qs, 30)
        page_number = self.request.GET.get('page')
        transaction_page_object = paginator.get_page(page_number)
        context['filter_form'] = transaction_filter.form
        context['object_list'] = transaction_page_object
        return context

class ChargeListView(ListView):
    model = Charge

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ChargeListView, self).get_context_data(**kwargs)
        charge_filter = ChargeFilter(self.request.GET, queryset=self.get_queryset())
        paginator = Paginator(charge_filter.qs, 30)
        page_number = self.request.GET.get('page')
        charge_page_object = paginator.get_page(page_number)
        context['filter_form'] = charge_filter.form
        context['object_list'] = charge_page_object
        return context

