from django.shortcuts import render
from django.views.generic import DetailView, ListView

from src.services.wallet.models import Wallet


# Create your views here.
class UserWalletView(DetailView):
    model = Wallet
    template_name = 'wallet/user_wallet.html'

class WalletListView(ListView):
    model = Wallet
    template_name = 'wallet/wallet_list.html'