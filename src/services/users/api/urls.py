from django.urls import path

from src.services.users.api.views import UserRetrieveUpdateAPIView, UserImageCreateAPIView, UserImageDestroyAPIView, \
    UserAddressRetrieveUpdateAPIView, ServiceProviderRetrieveUpdateAPIView, ServiceProviderInterestCreateAPIView, \
    ServiceProviderSocialMediaUpdateAPIView, ServiceProviderCertificateDestroyAPIView, \
    ServiceProviderCertificationCreateAPIView, ServiceProviderLanguageCreateAPIView, \
    ServiceProviderLanguageDestroyAPIView, FavoriteServiceDestroyAPIView, FavoriteServiceListCreateAPIView

app_name = "users-api"

"""SERVICE SEEKER URLS"""
urlpatterns = [
    path('v1/profile/', UserRetrieveUpdateAPIView.as_view(), name='user-update'),
    path('v1/image/', UserImageCreateAPIView.as_view(), name='image-update'),
    path('v1/image/<str:pk>/', UserImageDestroyAPIView.as_view(), name='image-delete'),
    path('v1/address/', UserAddressRetrieveUpdateAPIView.as_view(), name='address-update'),

]

urlpatterns += [
    path('v1/favorite-service/', FavoriteServiceListCreateAPIView.as_view(), name='favorite-service'),
    path('v1/favorite-service/<str:pk>/', FavoriteServiceDestroyAPIView.as_view(), name='favorite-service-delete'),
]

"""SERVICE PROVIDER URLS"""
urlpatterns += [
    path('v1/service-provider/', ServiceProviderRetrieveUpdateAPIView.as_view(), name='service-provider-update'),
    path('v1/service-provider/interest/', ServiceProviderInterestCreateAPIView.as_view(),
         name='service-provider-interest'),
    path('v1/service-provider/interest/<str:pk>/', ServiceProviderLanguageDestroyAPIView.as_view(),
         name='service-provider-language-destroy'),
    path('v1/service-provider/language/', ServiceProviderLanguageCreateAPIView.as_view(),
         name='service-provider-language'),
    path('v1/service-provider/social-media/', ServiceProviderSocialMediaUpdateAPIView.as_view(),
         name='service-provider-social-media'),
    path('v1/service-provider/certificate/', ServiceProviderCertificationCreateAPIView.as_view(),
         name='service-provider-certificate'),
    path('v1/service-provider/certificate/<str:pk>/', ServiceProviderCertificateDestroyAPIView.as_view(),
         name='service-provider-certificate-delete'),

]
