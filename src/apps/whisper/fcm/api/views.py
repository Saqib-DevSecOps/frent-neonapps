from fcm_django.models import FCMDevice
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, get_object_or_404, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serailizers import (
    FCMDeviceSerializer, FCMDeviceActivationSerializer, FCMDeviceRegisterOrUpdateSerializer
)
from ..utils import UserAgent


class FCMDeviceRegistrationAPIView(CreateAPIView):
    serializer_class = FCMDeviceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user_agent = UserAgent(request=self.request)

        machine_type = user_agent.get_device_type()
        os_family, os_version = user_agent.get_os_info()
        browser_family, browser_version = user_agent.get_browser_info()
        device_family, device_brand, device_model = user_agent.get_device_info()

        serializer.save(user=self.request.user, name=f"{os_family} {os_version}")


class FCMDeviceRegisterOrUpdateAPIView(APIView):
    serializer_class = FCMDeviceRegisterOrUpdateSerializer

    def get_user_agent(self):
        return UserAgent(request=self.request)

    def get_os_info(self):
        user_agent = self.get_user_agent()
        return user_agent.get_os_info()

    def post(self, request, *args, **kwargs):
        os_family, os_version = self.get_os_info()
        user = request.user if request.user.is_authenticated else None

        registration_id = request.data.get('registration_id')
        _type = request.data.get('type')
        device = FCMDevice.objects.filter(registration_id=registration_id)

        # VALIDATE SERIALIZER HERE
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not device.exists():
            FCMDevice.objects.create(
                user=user,
                registration_id=registration_id,
                name=f"{os_family} {os_version}",
                type=_type

            )
            return Response({'detail': 'Device registered successfully'}, status=status.HTTP_201_CREATED)

        else:
            device = device.first()
            if device.user:
                return Response(
                    {'detail': 'Device already registered with user'}, status=status.HTTP_200_OK
                )
            else:
                device.user = user
                device.type = _type
                device.name = f"{os_family} {os_version}"
                device.save()
                return Response(
                    {'detail': f'Device updated successfully with user as {user}'}, status=status.HTTP_200_OK
                )


class FCMDeviceActivationAPIView(RetrieveUpdateAPIView):
    serializer_class = FCMDeviceActivationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(
            FCMDevice.objects.filter(user=self.request.user, registration_id=self.kwargs['registration_id'])
        )


class FCMDeviceDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(
            FCMDevice.objects.filter(user=self.request.user, registration_id=self.kwargs['registration_id'])
        )
