from django.shortcuts import render
from django.views.generic import TemplateView

from src.apps.whisper.main import NotificationService


# Create your views here.
class HomeView(TemplateView):
    template_name = 'website/index.html'


class ServiceView(TemplateView):
    template_name = 'website/services.html'


class AboutUsView(TemplateView):
    template_name = 'website/about_us.html'


class BlogListView(TemplateView):
    template_name = 'website/blog_list.html'


class BlogDetailView(TemplateView):
    template_name = 'website/blog_detail.html'


class ContactUsView(TemplateView):
    template_name = 'website/contact_us.html'


class PrivacyPolicyView(TemplateView):
    template_name = 'website/privacy_policy.html'


class TermsAndConditionView(TemplateView):
    template_name = 'website/terms_and_condition.html'