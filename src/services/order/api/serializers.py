from rest_framework import serializers

from src.services.order.models import Advert, BookingRequest, Order, Payment


class AdvertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advert
        fields = ['id', 'user', 'service_type', 'service', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class BookingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingRequest
        fields = ['id', 'advert', 'service_provider', 'message', 'status', 'date_time', 'created_at']
        read_only_fields = ['id', 'advert', 'service_provider', 'created_at']


class BookingRequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingRequest
        fields = ['id', 'status']
        read_only_fields = ['id']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'service_provider', 'service', 'total_price', 'paid_price', 'discount', 'tax',
                  'service_charge', 'tip', 'status', 'payment_type', 'payment_status', 'date', 'start_time', 'end_time'
                  ]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'order', 'amount', 'tax', 'total_price', 'payment_type', 'payment_method', 'status',
                  'billing_first_name', 'billing_last_name', 'billing_address', 'billing_city', 'billing_state',
                  'billing_zip', 'billing_country', 'billing_phone', 'billing_email', 'created_at', 'updated_at'
                  ]
        read_only_fields = ['id', 'user', 'order', 'created_at', 'updated_at']
