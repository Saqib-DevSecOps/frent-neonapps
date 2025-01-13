from django.core.paginator import Paginator
from django.views.generic import DetailView, ListView
from rest_framework.generics import get_object_or_404

from src.services.order.filters import AdvertisementFilter, OrderFilter, AdvertisementRequestFilter
from src.services.order.models import Advertisement, Order, AdvertisementRequest


class AdvertisementListView(ListView):
    model = Advertisement

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdvertisementListView, self).get_context_data(**kwargs)
        advertisement_filter = AdvertisementFilter(self.request.GET, queryset=self.get_queryset())
        paginator = Paginator(advertisement_filter.qs, 30)
        page_number = self.request.GET.get('page')
        advertisement_page_object = paginator.get_page(page_number)
        context['filter_form'] = advertisement_filter.form
        context['object_list'] = advertisement_page_object
        return context


class AdvertisementRequesterListView(ListView):
    model = AdvertisementRequest

    def get_queryset(self):
        return AdvertisementRequest.objects.filter(advertisement_id=self.kwargs['advertisement_id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdvertisementRequesterListView, self).get_context_data(**kwargs)
        advertisement_request_filter = AdvertisementRequestFilter(self.request.GET, queryset=self.get_queryset())
        paginator = Paginator(advertisement_request_filter.qs, 30)
        page_number = self.request.GET.get('page')
        advertisement_request_page_object = paginator.get_page(page_number)
        context['filter_form'] = advertisement_request_filter.form
        context['object_list'] = advertisement_request_page_object
        return context


class OrderListView(ListView):
    model = Order

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        order_filter = OrderFilter(self.request.GET, queryset=self.get_queryset())
        paginator = Paginator(order_filter.qs, 30)
        page_number = self.request.GET.get('page')
        order_page_object = paginator.get_page(page_number)
        context['filter_form'] = order_filter.form
        context['object_list'] = order_page_object
        return context


class OrderDetailView(DetailView):
    model = Order

    def get_object(self, queryset=None):
        return get_object_or_404(Order, pk=self.kwargs['pk'])
