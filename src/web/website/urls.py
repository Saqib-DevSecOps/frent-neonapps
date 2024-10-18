from django.urls import path
from django.views.generic import TemplateView

from .views import (
    HomeView, ServiceView, AboutUsView, ContactUsView, BlogListView, BlogDetailView, PrivacyPolicyView,
    TermsAndConditionView
)

app_name = "website"
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('services/', ServiceView.as_view(), name='services'),
    path('about-us/', AboutUsView.as_view(), name='about'),
    path('become-a-provider/', TemplateView.as_view(template_name='website/become_a_provider.html'), name='become-a-provider'),
    path('blog-list/', BlogListView.as_view(), name='blog-list'),

    path('blog-detail/', BlogDetailView.as_view(), name='blog-detail'),
    path('contact-us/', ContactUsView.as_view(), name='contact-us'),

    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('terns-and-condition/', TermsAndConditionView.as_view(), name='terms-and-condition'),
]
