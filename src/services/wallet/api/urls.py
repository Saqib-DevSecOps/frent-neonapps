from django.urls import path

# from .views import WalletRetrieveAPIVIew, TransactionListCreateAPIView, BankListAPIView, BankAccountListCreateAPIView

app_name = "wallet-api"
urlpatterns = [
    # path('v1/wallet/', WalletRetrieveAPIVIew.as_view(), name='wallet'),
    # path('v1/transaction/', TransactionListCreateAPIView.as_view(), name='transaction'),
]

urlpatterns += [
    # path('v1/banks/', BankListAPIView.as_view(), name='bank-list'),
    # path('v1/bank-accounts/', BankAccountListCreateAPIView.as_view(), name='bank-account-list-create'),
]