import json

from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from fcm_django.models import FCMDevice

from src.apps.whisper.fcm.utils import FireBaseMessage

""" FCM DEVICE VIEWS """


class FCMDeviceListView(ListView):
    template_name = 'fcm/device_list.html'

    def get_queryset(self):
        return FCMDevice.objects.filter(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FCMDeviceListView, self).get_context_data(**kwargs)
        return context


class FCMDeviceCreateView(View):
    template_name = 'fcm/device_create.html'

    def get(self, request):
        # device = FCMDevice.objects.filter(user=self.request.user).first()
        #
        # firebase_message = FireBaseMessage(
        #     "SeedsWild",
        #     "This is the first push notification from Seeds wild"
        # )
        # firebase_message.sent_message_single(device)
        
        return render(request, self.template_name)


class FCMNotificationCreateAdminView(View):
    template_name = 'fcm/device_create_admin.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        title = request.POST.get('title')
        body = request.POST.get('body')
        token = request.POST.get('token')

        if title and body and token:
            device = FCMDevice.objects.filter(registration_id=token)
            if device:
                firebase_message = FireBaseMessage(title, body)
                firebase_message.sent_message_single(device.first())
                print("Message sent")
            else:
                print("Device not found")
        else:
            print("Some of the required details are missing")

        return render(request, self.template_name)


""" JSON VIEWS (not used now) """


class FCMDeviceCreateJsonView(View):

    def post(self, request):
        message_type = messages.ERROR

        try:
            data = json.loads(request.body)
            token = data.get('token')
            device_type = data.get('device_type')
        except json.JSONDecodeError:
            return JsonResponse({
                'message': 'Invalid JSON',
                'message_type': message_type
            }, status=400)

        if token and device_type:
            device, created = FCMDevice.objects.update_or_create(
                registration_id=token, type=device_type, user=request.user
            )
            if created:
                message = "Device created successfully"
                message_type = messages.SUCCESS
            else:
                device.active = True
                device.save()

                message = "Device already exists"
                message_type = messages.WARNING
        else:
            message = "Some of required details are missing"
            message_type = messages.ERROR

        return JsonResponse({
            'message': message,
            'message_type': message_type
        })


""" REQUIRED VERY MUCH """


def showFirebaseJS(request):
    data = 'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-app.js");' \
           'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-messaging.js"); ' \
           'var firebaseConfig = {' \
           '        apiKey: "AIzaSyDhroU-kOGwLW3MMY9vEPQFACijK_99_9g",' \
           '        authDomain: "seedswild.firebaseapp.com",' \
           '        projectId: "seedswild",' \
           '        storageBucket: "seedswild.appspot.com",' \
           '        messagingSenderId: "831708978986",' \
           '        appId: "1:831708978986:web:a1db9613a0b3f902344853",' \
           '        measurementId: "G-PYH0QN18GK"' \
           ' };' \
           'firebase.initializeApp(firebaseConfig);' \
           'const messaging=firebase.messaging();' \
           'messaging.setBackgroundMessageHandler(function (payload) {' \
           '    console.log(payload);' \
           '    const notification=JSON.parse(payload);' \
           '    const notificationOption={' \
           '        body:notification.body,' \
           '        icon:notification.icon' \
           '    };' \
           '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
           '});'

    return HttpResponse(data, content_type="text/javascript")
