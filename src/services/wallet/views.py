from django.shortcuts import render
from django.views.generic import DetailView, ListView

from src.services.wallet.models import Wallet, Transaction


# Create your views here.
class UserWalletView(DetailView):
    model = Wallet
    template_name = 'wallet/user_wallet.html'

    def get_context_data(self, **kwargs):
        context = super(UserWalletView, self).get_context_data(**kwargs)
        context['object_list'] = Transaction.objects.filter(wallet=self.object)
        return context

class TransactionListView(ListView):
    model = Transaction
    template_name = 'wallet/transaction_list.html'