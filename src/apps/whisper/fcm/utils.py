from fcm_django.models import FCMDevice
from firebase_admin.messaging import Notification, Message
from user_agents import parse

""" TOKEN """


class FireBaseMessage:

    def __init__(self, title, body, image=None):
        self.title = title
        self.body = body
        self.image = image

    def sent_message_single(self, devices):
        error_message = None
        try:
            for device in devices:
                if self.image:
                    status = device.send_message(
                        Message(
                            notification=Notification(
                                title=self.title,
                                body=self.body,
                                image=self.image
                            )
                        )
                    )
                else:
                    status = device.send_message(
                        Message(
                            notification=Notification(
                                title=self.title,
                                body=self.body
                            )
                        )
                    )
        except Exception as e:
            error_message = str(e)

        return error_message


class FireBaseDevice:

    def __init__(self, user, token):
        self.user = user
        self.token = token

    def register(self, device_id, device_type):
        device, created = FCMDevice.objects.update_or_create(
            device_id=device_id, registration_id=self.token, type=device_type,
            user=self.user
        )

        return device

    def unregister(self):
        device = FCMDevice.objects.filter(registration_id=self.token).first()
        if device:
            device.delete()
            return True

        return False

    @staticmethod
    def activation(device_id, activation=True):
        device = FCMDevice.objects.filter(device_id=device_id, active=activation).first()
        if device:
            device.active = activation
            device.save()
            return True

        return False


class UserAgent:

    def __init__(self, request):
        self.request = request
        self.__user_agent = parse(request.META.get('HTTP_USER_AGENT', ''))

    def get_device_info(self):
        return self.__user_agent.device.family, self.__user_agent.device.brand, self.__user_agent.device.model

    def get_os_info(self):
        return self.__user_agent.os.family, self.__user_agent.os.version_string

    def get_browser_info(self):
        return self.__user_agent.browser.family, self.__user_agent.browser.version_string

    def get_device_type(self):
        if self.__user_agent.is_mobile:
            return 'mobile'
        elif self.__user_agent.is_tablet:
            return 'tablet'
        elif self.__user_agent.is_pc:
            return 'pc'
        else:
            return 'bot'
