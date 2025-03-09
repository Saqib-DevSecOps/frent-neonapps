from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import ServiceReview

from src.services.services.filters import ServiceFilter
from src.services.services.models import Service, ServiceAvailability
from ..users.models import User


class ServicesListView(ListView):
    model = Service

    def get_context_data(self, **kwargs):
        context = super(ServicesListView, self).get_context_data(**kwargs)
        service_filter = ServiceFilter(self.request.GET, queryset=self.get_queryset())
        context['service_filter_form'] = service_filter.form
        paginator = Paginator(service_filter.qs, 30)
        page_number = self.request.GET.get('page')
        user_page_object = paginator.get_page(page_number)
        context['object_list'] = user_page_object
        return context

class UserServicesListView(ListView):
    model = Service

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return Service.objects.filter(provider=pk)


class ServiceDetailView(DetailView):
    model = Service

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = self.object
        availability_slots = ServiceAvailability.objects.filter(service=service, is_active=True).order_by('day_of_week', 'start_time')
        context['availability_slots'] = availability_slots
        return context


class ServiceReviewListView(ListView):
    model = ServiceReview
    context_object_name = "reviews"

    def get_queryset(self):
        """Return reviews for a specific service if `pk` is provided, otherwise return all reviews."""
        pk = self.kwargs.get("pk")
        if pk:
            service = get_object_or_404(Service, pk=pk)
            return service.reviews.all()
        return ServiceReview.objects.all()

    def get_context_data(self, **kwargs):
        """Add the service object to context if `pk` is provided."""
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        if pk:
            context["object"] = get_object_or_404(Service, pk=pk)
        return context

class UserServiceReviewListView(ListView):
    model = ServiceReview
    context_object_name = "reviews"

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return ServiceReview.objects.filter(reviewer=pk)
