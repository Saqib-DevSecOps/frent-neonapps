from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView

from src.services.users.models import User
from src.services.wallet.models import Wallet, Transaction


# Create your views here.
class UserWalletView(DetailView):
    model = Wallet
    template_name = 'wallet/user_wallet.html'

    def get_context_data(self, **kwargs):
        context = super(UserWalletView, self).get_context_data(**kwargs)
        context['object_list'] = Transaction.objects.filter(wallet=self.object)[:7]
        return context

class TransactionListView(ListView):
    model = Transaction
    template_name = 'wallet/transaction_list.html'
    paginate_by = 20


class UserTransactionListView(ListView):
    model = Transaction
    template_name = 'wallet/user_transaction.html'
    context_object_name = 'object_list'
    paginate_by = 20

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return Transaction.objects.filter(user=user)

    def get_context_data(self, **kwargs):
        context = super(UserTransactionListView, self).get_context_data(**kwargs)
        context['wallet_user'] = get_object_or_404(User, pk=self.kwargs['pk'])
        return context