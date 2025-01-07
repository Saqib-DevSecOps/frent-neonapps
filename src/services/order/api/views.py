from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, get_object_or_404, DestroyAPIView, \
    ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.services.order.api.serializers import AdvertSerializer, BookingRequestSerializer, \
    BookingRequestUpdateSerializer
from src.services.order.models import Advert, BookingRequest


class AdvertListCreateAPIView(ListCreateAPIView):
    """
    API endpoint to create an advert
    SERVICE_TYPES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]
    """
    serializer_class = AdvertSerializer
    permission_classes = [IsAuthenticated]
    queryset = Advert.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Advert.objects.filter(user=self.request.user)


class AdvertDestroyAPIView(DestroyAPIView):
    serializer_class = AdvertSerializer
    permission_classes = [IsAuthenticated]
    queryset = Advert.objects.all()

    def get_object(self):
        advert = get_object_or_404(Advert, id=self.kwargs.get('pk'), user=self.request.user)
        return advert

    def perform_destroy(self, instance):
        instance.delete()
        return Response(status=status.HTTP_200_OK, data={'message': 'Advert successfully Deleted'})


class BookingRequestListCreateAPIView(ListCreateAPIView):
    queryset = BookingRequest.objects.all()
    serializer_class = BookingRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        advert_id = self.kwargs.get('advert_id')
        return BookingRequest.objects.filter(
            advert_id=advert_id,
            service_provider=self.request.user.get_service_provider_profile()
        )

    def perform_create(self, serializer):
        serializer.save(advert_id=self.kwargs.get('advert_id'),
                        service_provider=self.request.user.get_service_provider_profile())


class BookingRequestUpdateAPIView(UpdateAPIView):
    """
      API endpoint to accept a booking request
      STATUS_CHOICES = [
      ('pending', 'Pending'),
      ('accepted', 'Accepted'),
      ('rejected', 'Rejected'),
      ]
      """
    serializer_class = BookingRequestUpdateSerializer
    permission_classes = [IsAuthenticated]
    queryset = BookingRequest.objects.all()

    def get_object(self):
        booking_request = get_object_or_404(BookingRequest, id=self.kwargs.get('pk'), advert__user=self.request.user)
        return booking_request


class BookingRequestDestroyAPIView(DestroyAPIView):
    serializer_class = BookingRequestSerializer
    permission_classes = [IsAuthenticated]
    queryset = BookingRequest.objects.all()

    def get_object(self):
        booking_request = get_object_or_404(BookingRequest, id=self.kwargs.get('pk'), advert__user=self.request.user)
        return booking_request

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK, data={'message': 'Booking Request successfully Deleted'})
