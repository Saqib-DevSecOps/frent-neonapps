# src/services/views.py
from django.shortcuts import render
from django.utils import timezone
from .utils import (
    get_total_earnings,
    get_total_bookings,
    get_active_providers,
    get_pending_withdrawals,
    get_cumulative_bookings,
    get_cumulative_earnings,
    get_monthly_revenue,
    get_monthly_bookings,
)

# @method_decorator(staff_required_decorator, name='dispatch')
def dashboard_view(request):
    total_earnings, earnings_change = get_total_earnings()
    total_bookings, bookings_change = get_total_bookings()
    active_providers, providers_change = get_active_providers()
    pending_withdrawals, pending_change = get_pending_withdrawals()
    cumulative_bookings = get_cumulative_bookings()
    cumulative_earnings = get_cumulative_earnings()
    monthly_revenue = get_monthly_revenue()
    monthly_bookings = get_monthly_bookings()

    context = {
        'total_earnings': total_earnings,
        'earnings_change': earnings_change,
        'service_bookings': total_bookings,
        'bookings_change': bookings_change,
        'active_providers': active_providers,
        'providers_change': providers_change,
        'pending_withdrawals': pending_withdrawals,
        'pending_change': pending_change,
        'cumulative_bookings': cumulative_bookings,
        'cumulative_earnings': cumulative_earnings,
        'monthly_revenue': monthly_revenue,
        'monthly_bookings': monthly_bookings,
        'today': timezone.now().date(),
    }

    return render(request, 'dashboard/dashboard.html', context)