from django.urls import path

from src.apps.stripe.api.views import ConnectWalletCreateAPIView, ConnectWalletActivateAPIView

app_name = 'stripe-api'
urlpatterns = [
    path('connect-wallet/', ConnectWalletCreateAPIView.as_view(), name='connect_wallet'),
    path('connect-wallet/activate/', ConnectWalletActivateAPIView.as_view(), name='connect_wallet_activate'),

]
