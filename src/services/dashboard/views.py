from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from src.services.finance.models import Withdrawal, Charge
from src.services.order.models import ServiceBookingRequest
from src.services.users.models import User, ServiceProvider
from src.web.accounts.decorators import staff_required_decorator
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Count
from decimal import Decimal

# @method_decorator(staff_required_decorator, name='dispatch')
def dashboard_view(request):
    # Get today's and yesterday's dates
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)

    # Total Earnings
    today_earnings = Charge.objects.filter(
        created_at__date=today,
        status='completed'
    ).aggregate(total=Sum('fee_amount'))['total'] or Decimal('0.00')

    yesterday_earnings = Charge.objects.filter(
        created_at__date=yesterday,
        status='completed'
    ).aggregate(total=Sum('fee_amount'))['total'] or Decimal('0.00')

    earnings_change = calculate_percentage_change(today_earnings, yesterday_earnings)

    # Service Bookings
    today_bookings = ServiceBookingRequest.objects.filter(
        created_at__date=today
    ).count()

    yesterday_bookings = ServiceBookingRequest.objects.filter(
        created_at__date=yesterday
    ).count()

    bookings_change = calculate_percentage_change(today_bookings, yesterday_bookings)


    today_providers = ServiceProvider.objects.filter(verified=True).count()
    yesterday_providers = ServiceProvider.objects.filter(
        verified=True,
        created_at__date__lte=yesterday
    ).count()


    providers_change = calculate_percentage_change(today_providers, yesterday_providers)

    # Pending Withdrawals
    today_pending = Withdrawal.objects.filter(
        status='pending',
        created_at__date__lte=today
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    yesterday_pending = Withdrawal.objects.filter(
        status='pending',
        created_at__date__lte=yesterday
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    pending_change = calculate_percentage_change(today_pending, yesterday_pending)

    context = {
        'total_earnings': today_earnings,
        'earnings_change': earnings_change,
        'service_bookings': today_bookings,
        'bookings_change': bookings_change,
        'active_providers': today_providers,
        'providers_change': providers_change,
        'pending_withdrawals': today_pending,
        'pending_change': pending_change,
    }

    return render(request, 'dashboard/dashboard.html', context)


def calculate_percentage_change(current, previous):
    if previous == 0:
        return 0.0 if current == 0 else 100.0 if current > 0 else -100.0
    return round(((current - previous) / previous) * 100, 1)