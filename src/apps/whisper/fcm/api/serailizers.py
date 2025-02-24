from fcm_django.models import FCMDevice
from rest_framework import serializers


class FCMDeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = FCMDevice
        fields = ['id', 'type', 'device_id', 'registration_id', 'name', 'active', 'user', 'date_created']
        read_only_fields = ['id', 'device_id', 'name', 'active', 'user', 'date_created']


class FCMDeviceRegisterOrUpdateSerializer(serializers.ModelSerializer):
    REGISTRATION_TYPE_CHOICES = [
        ('web', 'Web'),
        ('android', 'Android'),
        ('ios', 'iOS'),
    ]

    registration_id = serializers.CharField(required=True, write_only=True, allow_blank=False, allow_null=False, )
    type = serializers.ChoiceField(
        required=True, write_only=True, allow_blank=False, allow_null=False, choices=REGISTRATION_TYPE_CHOICES
    )

    class Meta:
        model = FCMDevice
        fields = ['registration_id', 'type']
        read_only_fields = ['registration_id', 'type']

    # VALIDATE
    def validate(self, data):
        registration_id = data.get('registration_id')
        _type = data.get('type')

        if not registration_id or not _type:
            raise serializers.ValidationError('registration_id and type is required')

        if not _type or _type not in ['web', 'android', 'ios']:
            raise serializers.ValidationError('Invalid device type')

        return data


class FCMDeviceActivationSerializer(serializers.ModelSerializer):

    class Meta:
        model = FCMDevice
        fields = ['id', 'type', 'device_id', 'registration_id', 'name', 'active', 'user', 'date_created']
        read_only_fields = ['id', 'device_id', 'name', 'registration_id', 'type', 'user', 'date_created']
