from rest_framework import serializers

from src.services.order.models import ServiceBookingRequest, Advertisement, AdvertisementRequest, Order, SpecialOffer
from src.services.services.api.serializers import UserProfileSerializer, ServiceSerializer


class ServiceBookingRequestSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = ServiceBookingRequest
        fields = ['id', 'user', 'service', 'start_datetime', 'end_datetime', 'status', 'message', 'created_at',
                  'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def validate(self, data):
        if data['start_datetime'] > data['end_datetime']:
            raise serializers.ValidationError("End date should be greater than start date.")
        return data


class ServiceBookingRequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceBookingRequest
        fields = ['id', 'status']
        read_only_fields = ['id']


class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ['id', 'user', 'service_type', 'service', 'start_datetime', 'end_datetime', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class AdvertisementRequestSerializer(serializers.ModelSerializer):
    advertisement = AdvertisementSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = AdvertisementRequest
        fields = ['id', 'advertisement', 'service_provider', 'service', 'status', 'created_at']
        read_only_fields = ['id', 'advertisement', 'service_provider', 'service', 'created_at']


class AdvertisementRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementRequest
        fields = ['id', 'service', 'message']


class AdvertisementRequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementRequest
        fields = ['id', 'status']
        read_only_fields = ['id']


class SpecialOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialOffer
        fields = ['id', 'service', 'user', 'service_day', 'start_time', 'end_time', 'service_fee', 'currency', 'status',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class SpecialOfferUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialOffer
        fields = ['id', 'status']
        read_only_fields = ['id']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'service_booking_request', 'service_advertisement_request', 'payment_type',
                  'total_price', 'paid_price', 'tip',
                  'order_status', 'payment_status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class OrderDetailSerializer(serializers.ModelSerializer):
    service_booking_request = ServiceBookingRequestSerializer(read_only=True)
    service_advertisement_request = AdvertisementRequestSerializer(read_only=True)
    user = UserProfileSerializer(read_only=True)
    service = ServiceSerializer(read_only=True, source='get_service')

    class Meta:
        model = Order
        fields = ['id', 'user', 'service', 'service_booking_request', 'service_advertisement_request', 'payment_type',
                  'total_price', 'paid_price', 'tip',
                  'order_status', 'payment_status', 'created_at', 'updated_at']


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['total_price', 'paid_price', 'tip', 'order_status', 'payment_status']
