# src/services/utils.py
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Count
from decimal import Decimal
from src.services.finance.models import Withdrawal, Charge
from src.services.order.models import ServiceBookingRequest
from src.services.users.models import ServiceProvider
from dateutil.relativedelta import relativedelta  # Requires python-dateutil

def calculate_percentage_change(current, previous):
    """Calculates percentage change between current and previous values."""
    if previous == 0:
        return 0.0 if current == 0 else 100.0 if current > 0 else -100.0
    return round(((current - previous) / previous) * 100, 1)

def get_total_earnings():
    """Fetches total earnings from completed charges for today vs. yesterday."""
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    today_earnings = Charge.objects.filter(
        created_at__date=today,
        status='completed'
    ).aggregate(total=Sum('fee_amount'))['total'] or Decimal('0.00')
    yesterday_earnings = Charge.objects.filter(
        created_at__date=yesterday,
        status='completed'
    ).aggregate(total=Sum('fee_amount'))['total'] or Decimal('0.00')
    change = calculate_percentage_change(today_earnings, yesterday_earnings)
    return today_earnings, change

def get_total_bookings():
    """Fetches total service bookings for today vs. yesterday."""
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    today_bookings = ServiceBookingRequest.objects.filter(
        created_at__date=today
    ).count()
    yesterday_bookings = ServiceBookingRequest.objects.filter(
        created_at__date=yesterday
    ).count()
    change = calculate_percentage_change(today_bookings, yesterday_bookings)
    return today_bookings, change

def get_active_providers():
    """Fetches count of verified service providers for today vs. yesterday."""
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    today_providers = ServiceProvider.objects.filter(
        verified=True
    ).count()
    yesterday_providers = ServiceProvider.objects.filter(
        verified=True,
        created_at__date__lte=yesterday
    ).count()
    change = calculate_percentage_change(today_providers, yesterday_providers)
    return today_providers, change

def get_pending_withdrawals():
    """Fetches total pending withdrawals for today vs. yesterday."""
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    today_pending = Withdrawal.objects.filter(
        status='pending',
        created_at__date__lte=today
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    yesterday_pending = Withdrawal.objects.filter(
        status='pending',
        created_at__date__lte=yesterday
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    change = calculate_percentage_change(today_pending, yesterday_pending)
    return today_pending, change

def get_cumulative_bookings(start_date=None):
    """Fetches cumulative total bookings, optionally filtered by start date."""
    qs = ServiceBookingRequest.objects.all()
    if start_date:
        qs = qs.filter(created_at__date__gte=start_date)
    return qs.count()

def get_cumulative_earnings(start_date=None):
    """Fetches cumulative total earnings from completed charges, optionally filtered by start date."""
    qs = Charge.objects.filter(status='completed')
    if start_date:
        qs = qs.filter(created_at__date__gte=start_date)
    total = qs.aggregate(total=Sum('fee_amount'))['total'] or Decimal('0.00')
    return Decimal(total)

def get_monthly_revenue():
    """Returns a list of revenue totals (as Decimals) for the last 12 months."""
    today = timezone.now().date()
    revenue_list = []
    for i in range(11, -1, -1):
        month_start = today - relativedelta(months=i, day=1)
        month_end = month_start + relativedelta(months=1, days=-1)
        monthly_revenue = Charge.objects.filter(
            created_at__date__gte=month_start,
            created_at__date__lte=month_end,
            status='completed'
        ).aggregate(total=Sum('fee_amount'))['total'] or Decimal('0.00')
        mr = int(monthly_revenue)
        revenue_list.append(mr)
    return revenue_list

def get_monthly_bookings():
    """Returns a list of booking counts (as integers) for the last 12 months."""
    today = timezone.now().date()
    bookings_list = []
    for i in range(11, -1, -1):
        month_start = today - relativedelta(months=i, day=1)
        month_end = month_start + relativedelta(months=1, days=-1)
        monthly_bookings = ServiceBookingRequest.objects.filter(
            created_at__date__gte=month_start,
            created_at__date__lte=month_end
        ).count()
        bookings_list.append(monthly_bookings)
    return bookings_list