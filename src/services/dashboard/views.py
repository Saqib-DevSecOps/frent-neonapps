from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from .utils import (
    get_total_earnings,
    get_total_bookings,
    get_active_providers,
    get_pending_withdrawals,
    get_cumulative_bookings,
    get_cumulative_earnings,
    get_monthly_revenue,
    get_monthly_bookings,
    get_radius_data,
)
from ..order.models import Order
from ...web.accounts.decorators import staff_required_decorator


@method_decorator(staff_required_decorator, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        i, d = get_radius_data()
        now = timezone.now()
        context.update({
            'total_earnings': get_total_earnings()[0],
            'earnings_change': get_total_earnings()[1],
            'service_bookings': get_total_bookings()[0],
            'bookings_change': get_total_bookings()[1],
            'active_providers': get_active_providers()[0],
            'providers_change': get_active_providers()[1],
            'pending_withdrawals': get_pending_withdrawals()[0],
            'pending_change': get_pending_withdrawals()[1],
            'cumulative_bookings': get_cumulative_bookings(),
            'cumulative_earnings': get_cumulative_earnings(),
            'monthly_revenue': get_monthly_revenue(),
            'monthly_bookings': get_monthly_bookings(),
            'today': timezone.now().date(),
            'rad_data' : d,
            'indexes': i,
            'month': now.strftime("%B"),
            'object_list': Order.objects.order_by("-created_at")[:9]
        })

        return context
