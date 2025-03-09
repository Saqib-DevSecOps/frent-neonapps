from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView
from rest_framework.generics import get_object_or_404
from src.services.order.filters import AdvertisementFilter, OrderFilter, AdvertisementRequestFilter, \
    ServiceBookingRequestFilter, SpecialOfferFilter, PaymentFilter
from src.services.order.models import Advertisement, Order, AdvertisementRequest, ServiceBookingRequest, SpecialOffer, \
    Payment
from src.services.services.models import Service
from src.web.accounts.decorators import staff_required_decorator


@method_decorator(staff_required_decorator, name='dispatch')
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


@method_decorator(staff_required_decorator, name='dispatch')
class AdvertisementRequestsListView(ListView):
    model = AdvertisementRequest

    def get_queryset(self):
        return AdvertisementRequest.objects.filter(advertisement_id=self.kwargs['advertisement_id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdvertisementRequestsListView, self).get_context_data(**kwargs)
        advertisement_request_filter = AdvertisementRequestFilter(self.request.GET, queryset=self.get_queryset())
        paginator = Paginator(advertisement_request_filter.qs, 30)
        page_number = self.request.GET.get('page')
        advertisement_request_page_object = paginator.get_page(page_number)
        context['filter_form'] = advertisement_request_filter.form
        context['object_list'] = advertisement_request_page_object
        return context


@method_decorator(staff_required_decorator, name='dispatch')
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


@method_decorator(staff_required_decorator, name='dispatch')
class OrderDetailView(DetailView):
    model = Order

    def get_object(self, queryset=None):
        return get_object_or_404(Order, pk=self.kwargs['pk'])

@method_decorator(staff_required_decorator, name='dispatch')
class ServiceBookingRequestListView(ListView):
    model = ServiceBookingRequest

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ServiceBookingRequestListView, self).get_context_data(**kwargs)
        service_booking_request_filter = ServiceBookingRequestFilter(self.request.GET, queryset=self.get_queryset())
        paginator = Paginator(service_booking_request_filter.qs, 30)
        page_number = self.request.GET.get('page')
        service_booking_request_page_object = paginator.get_page(page_number)
        context['filter_form'] = service_booking_request_filter.form
        context['object_list'] = service_booking_request_page_object
        return context


from django.core.paginator import Paginator
from django.utils.decorators import method_decorator


@method_decorator(staff_required_decorator, name='dispatch')
class ServiceBookingRequestView(ListView):
    model = ServiceBookingRequest

    def get_queryset(self):
        queryset = ServiceBookingRequest.objects.filter(service=self.kwargs['pk'])
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator = Paginator(self.get_queryset(), 30)
        page_number = self.request.GET.get('page')
        service_booking_request_page_object = paginator.get_page(page_number)
        context['object_list'] = service_booking_request_page_object
        context['object'] = get_object_or_404(Service, pk=self.kwargs['pk'])
        return context


@method_decorator(staff_required_decorator, name='dispatch')
class SpecialOfferListView(ListView):
    model = SpecialOffer

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SpecialOfferListView, self).get_context_data(**kwargs)
        special_offer_filter = SpecialOfferFilter(self.request.GET, queryset=self.get_queryset())
        paginator = Paginator(special_offer_filter.qs, 30)
        page_number = self.request.GET.get('page')
        special_offer_page_object = paginator.get_page(page_number)
        context['filter_form'] = special_offer_filter.form
        context['object_list'] = special_offer_page_object
        return context

@method_decorator(staff_required_decorator, name='dispatch')
class PaymentsListView(ListView):
    model = Payment

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PaymentsListView, self).get_context_data(**kwargs)
        payment_filter = PaymentFilter(self.request.GET, queryset=self.get_queryset())
        paginator = Paginator(payment_filter.qs, 30)
        page_number = self.request.GET.get('page')
        payment_page_object = paginator.get_page(page_number)
        context['filter_form'] = payment_filter.form
        context['object_list'] = payment_page_object
        return context