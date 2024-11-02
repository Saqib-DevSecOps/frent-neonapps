from django.urls import path
from .views import (
    ConnectWalletCreateView, ConnectWalletVisitView, ConnectWalletView, StripeWebHook,
    SubscriptionCreateView, SubscriptionPortalLinkView, SubscriptionSuccessView, SubscriptionFailureView,
    SubscriptionDetailView, ProductListView, ProductRefreshView, SubscriptionListView
)

app_name = 'stripe'
urlpatterns = [

    path('subscription/detail/', SubscriptionDetailView.as_view(), name='subscription-detail'),
    path('subscription/create/', SubscriptionCreateView.as_view(), name='subscription-create'),
    path('subscription/portal/', SubscriptionPortalLinkView.as_view(), name='subscription-portal-link'),
    path('subscription/success/', SubscriptionSuccessView.as_view(), name='subscription-success'),
    path('subscription/failure/', SubscriptionFailureView.as_view(), name='subscription-failure'),

]

# VENDOR END POINTS
urlpatterns += [

    path('connect-wallet/', ConnectWalletView.as_view(), name='connect-wallet'),
    path('connect-wallet/create/', ConnectWalletCreateView.as_view(), name='connect-wallet-create'),
    path('connect-wallet/visit/', ConnectWalletVisitView.as_view(), name='connect-wallet-visit'),

]

# SUPER USER
urlpatterns += [

    path('product/', ProductListView.as_view(), name='product-list'),
    path('product/refresh/', ProductRefreshView.as_view(), name='product-refresh'),
    path('subscription/', SubscriptionListView.as_view(), name="subscription-list"),

]

# WEBHOOK END POINT
urlpatterns += [
    path('hook/', StripeWebHook.as_view(), name='stripe-webhook'),
]
