from django.views.generic import DeleteView
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView, UpdateAPIView, RetrieveUpdateAPIView, \
    get_object_or_404, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.services.order.api.serializers import AdvertisementSerializer, AdvertisementRequestSerializer, \
    AdvertisementRequestCreateSerializer, AdvertisementRequestUpdateSerializer, ServiceBookingRequestSerializer, \
    ServiceBookingRequestUpdateSerializer, OrderSerializer, OrderDetailSerializer, OrderUpdateSerializer, \
    SpecialOfferSerializer, SpecialOfferUpdateSerializer
from src.services.order.models import Advertisement, AdvertisementRequest, ServiceBookingRequest, Order, SpecialOffer
from src.services.users.models import User


class AdvertisementListCreateAPIView(ListCreateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Advertisement.objects.filter(user=self.request.user)


class AdvertisementDeleteAPIView(DestroyAPIView):
    queryset = Advertisement.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Advertisement, user=self.request.user, pk=self.kwargs.get('pk'))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK, data={'message': 'Advertisement deleted successfully'})


class AdvertisementRequestListAPIView(ListAPIView):
    queryset = AdvertisementRequest.objects.all()
    serializer_class = AdvertisementRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AdvertisementRequest.objects.filter(advertisement__user=self.request.user,
                                                   advertisement_id=self.kwargs.get('advertisement_id'))


class AdvertisementRequestUpdateAPIView(UpdateAPIView):
    """STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]"""
    queryset = AdvertisementRequest.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AdvertisementRequestUpdateSerializer

    def get_object(self):
        return get_object_or_404(AdvertisementRequest, advertisement__user=self.request.user,
                                 pk=self.kwargs.get('pk'))


class BaseAdvertisementRequestDeleteAPIView(DestroyAPIView):
    queryset = AdvertisementRequest.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AdvertisementRequestSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK, data={'message': 'Advertisement Request deleted successfully'})


class AdvertisementRequestDeleteAPIView(BaseAdvertisementRequestDeleteAPIView):
    def get_object(self):
        return get_object_or_404(AdvertisementRequest, advertisement__user=self.request.user,
                                 pk=self.kwargs.get('pk'))


class ProviderAdvertisementRequestCreateAPIView(CreateAPIView):
    queryset = AdvertisementRequest.objects.all()
    serializer_class = AdvertisementRequestCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        advertisement = get_object_or_404(Advertisement,
                                          pk=self.kwargs.get('advertisement_id')
                                          )
        serializer.save(advertisement=advertisement, service_provider=self.request.user.service_provider_profile)


class ProviderAdvertisementRequestListAPIView(ListAPIView):
    queryset = AdvertisementRequest.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AdvertisementRequestSerializer

    def get_queryset(self):
        return AdvertisementRequest.objects.filter(service_provider__user=self.request.user)


class ProviderAdvertisementRequestDeleteAPIView(BaseAdvertisementRequestDeleteAPIView):

    def get_object(self):
        return get_object_or_404(AdvertisementRequest, service_provider__user=self.request.user,
                                 pk=self.kwargs.get('pk'))


class ServiceBookingRequestListCreateAPIView(ListCreateAPIView):
    """
    List and create booking requests for the service provider.
    Remove The User from the CreateApi Request
    """
    queryset = ServiceBookingRequest.objects.all()
    serializer_class = ServiceBookingRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return ServiceBookingRequest.objects.filter(service__provider=self.request.user)


class ServiceBookingRequestUpdateAPIView(UpdateAPIView):
    """
    Update the status of the booking request.
      REQUEST_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    """
    queryset = ServiceBookingRequest.objects.all()
    serializer_class = ServiceBookingRequestUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(ServiceBookingRequest, service__provider=self.request.user, pk=self.kwargs.get('pk'))


class ServiceBookingRequestDeleteAPIView(DestroyAPIView):
    queryset = ServiceBookingRequest.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceBookingRequestSerializer

    def get_object(self):
        return get_object_or_404(ServiceBookingRequest, service__provider=self.request.user, pk=self.kwargs.get('pk'))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK, data={'message': 'Service Booking Request deleted successfully'})


class ProviderSpecialOfferCreateAPIView(CreateAPIView):
    queryset = SpecialOffer.objects.all()
    serializer_class = SpecialOfferSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        serializer.save(user=user)


class ServiceSpecialOfferListAPIView(ListAPIView):
    queryset = SpecialOffer.objects.all()
    serializer_class = SpecialOfferSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        provider_id = self.kwargs.get('provider_user_id')
        return SpecialOffer.objects.filter(user_id=user_id, service__provider_id=provider_id)


class ServiceSpecialOfferUpdateAPIView(UpdateAPIView):
    """
    Update the status of the booking request.
      REQUEST_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    """
    queryset = SpecialOffer.objects.all()
    serializer_class = SpecialOfferUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(SpecialOffer, user=self.request.user, pk=self.kwargs.get('pk'))


class OrderListCreateAPIView(ListCreateAPIView):
    """
    Tracks Orders made for services

    If You user buy service using booking request then you can use service_booking_request field , if user buy service
    through advertisement then you can use service_advertisement_request field and if the user want to buy it from
    special offer then you can use special_offer field.
    .
        PAYMENT_TYPE_CHOICES = [
        ('full', 'Full Payment'),
        ('partial', 'Partial Payment'),
        ]
        ORDER_STATUS_CHOICES = [
            ('pending', 'Pending'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ]
        PAYMENT_STATUS_CHOICES = [
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
            ('refunded', 'Refunded'),
        ]
    """
    model = Order
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    model = Order
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderDetailSerializer
        return OrderUpdateSerializer

    def get_object(self):
        return get_object_or_404(Order, user=self.request.user, pk=self.kwargs.get('pk'))
