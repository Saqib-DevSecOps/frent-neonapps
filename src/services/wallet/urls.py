from django.urls import path
from src.services.wallet.views import UserWalletView, TransactionListView

app_name = "wallet"
urlpatterns = [
    path('user-wallet/<int:pk>/', UserWalletView.as_view(), name='user-wallet'),
    path('wallet/list/', TransactionListView.as_view(), name='wallet-list'),

]