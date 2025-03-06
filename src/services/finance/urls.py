from django.urls import path, include

from .views import (
    FinanceDashboard, PayoutMethodView,
    BankAccountCreateView, BankAccountDeleteView,
    PaypalAccountCreateView, PaypalAccountDeleteView,
    WithdrawalCreateView, WithdrawalListView,

    BankAccountUpdateView, PaypalAccountUpdateView, WithdrawalUpdateView,
    PaypalAccountListView, BankAccountListView,

    ConnectAccountView
)
from .views import _WithdrawalListView

app_name = 'finance'
urlpatterns = [

    # path('', FinanceDashboard.as_view(), name='withdrawals'),
    # path('payout-methods/', PayoutMethodView.as_view(), name='payout-method'),
    # path('connect-account/', ConnectAccountView.as_view(), name='connect-account'),
    #
    # path('bank-account/create/', BankAccountCreateView.as_view(), name='bank-account-create'),
    # path('bank-account/delete/<int:pk>/', BankAccountDeleteView.as_view(), name='bank-account-delete'),
    #
    # path('paypal-account/create/', PaypalAccountCreateView.as_view(), name='paypal-account-create'),
    # path('paypal-account/delete/<int:pk>/', PaypalAccountDeleteView.as_view(), name='paypal-account-delete'),
    #
    # path('withdrawal/', WithdrawalListView.as_view(), name='withdrawal-list'),
    # path('withdrawal/create/', WithdrawalCreateView.as_view(), name='withdrawal-create'),

]

urlpatterns += [
#     path('paypal-account/<int:pk>/change/', PaypalAccountUpdateView.as_view(), name='paypal-account-update'),
#     path('bank-account/<int:pk>/change/', BankAccountUpdateView.as_view(), name='bank-account-update'),
#     path('withdrawal/<int:pk>/change/', WithdrawalUpdateView.as_view(), name='withdrawal-update'),
#
#     path('bank-account/', BankAccountListView.as_view(), name='bank-account-list'),
#     path('paypal-account/', PaypalAccountListView.as_view(), name='paypal-account-list')

    path('finance/api/', include('src.services.finance.api.urls', namespace='finance-api')),
]


urlpatterns += [
    path('withdrawal-list/', _WithdrawalListView.as_view(), name='_withdrawal-list'),
]