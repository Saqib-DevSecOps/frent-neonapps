from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView, UpdateAPIView, RetrieveUpdateAPIView, \
    get_object_or_404
from rest_framework.permissions import IsAuthenticated

from src.services.order.api.serializers import AdvertisementSerializer, AdvertisementRequestSerializer, \
    AdvertisementRequestCreateSerializer, AdvertisementRequestUpdateSerializer, ServiceBookingRequestSerializer, \
    ServiceBookingRequestUpdateSerializer, OrderSerializer, OrderDetailSerializer, OrderUpdateSerializer
from src.services.order.models import Advertisement, AdvertisementRequest, ServiceBookingRequest, Order


class AdvertisementListCreateAPIView(ListCreateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Advertisement.objects.filter(user=self.request.user)


class AdvertisementRequestListAPIView(ListAPIView):
    queryset = AdvertisementRequest.objects.all()
    serializer_class = AdvertisementRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AdvertisementRequest.objects.filter(advertisement__user=self.request.user,
                                                          advertisement_id=self.kwargs.get('advertisement_id'))


class AdvertisementRequestCreateAPIView(CreateAPIView):
    queryset = AdvertisementRequest.objects.all()
    serializer_class = AdvertisementRequestCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        advertisement = get_object_or_404(Advertisement,
                                          pk=self.kwargs.get('advertisement_id')
                                          )
        serializer.save(advertisement=advertisement, service_provider=self.request.user.service_provider_profile)


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


class OrderListCreateAPIView(ListCreateAPIView):
    """
    Tracks Orders made for services

    If You user buy service using booking request then you can use service_booking_request field , if user buy service
    through advertisement then you can use service_advertisement_request field.
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
