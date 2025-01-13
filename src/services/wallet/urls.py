from django.urls import path, include
from src.services.wallet.views import UserWalletView, TransactionListView, UserTransactionListView

app_name = "wallet"
urlpatterns = [
    path('user-wallet/<int:pk>/', UserWalletView.as_view(), name='user-wallet'),
    path('wallet/list/', TransactionListView.as_view(), name='wallet-list'),
    path('user-transaction/<int:pk>/', UserTransactionListView.as_view(), name='user-transaction'),
]

urlpatterns += [
    path('wallet/api/', include('src.services.wallet.api.urls', namespace='wallet-api')),
]
