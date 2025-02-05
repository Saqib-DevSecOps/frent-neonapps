from django.urls import path

from src.services.finance.api.views import WalletRetrieveAPIVIew, BankAccountListCreateView, BankAccountDeleteAPIView, \
    WithdrawalListCreateAPIView, TransactionListAPIView, ChargeListAPIView

app_name = "finance-api"

urlpatterns = [
    path('wallet/', WalletRetrieveAPIVIew.as_view(), name='wallet'),
    path('bank-account/', BankAccountListCreateView.as_view(), name='bank-account'),
    path('bank-account/<int:pk>/', BankAccountDeleteAPIView.as_view(), name='bank-account-delete'),
    path('withdrawal/', WithdrawalListCreateAPIView.as_view(), name='withdrawal'),
    path('transaction/', TransactionListAPIView.as_view(), name='transaction'),

]
