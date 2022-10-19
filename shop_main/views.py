import djoser.views
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
import requests
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from shop_main.models import *
from shop_main.serializers import *
import shop.settings
from djoser import signals
from djoser.conf import settings
from djoser.compat import get_user_email
from shop_main.serializers import UserSerializerCustom


# def send_mail_endpoint(request):
#     print('sending email')
#     x = send_mail(
#         'Subject here',
#         'Here is the message.',
#         'amirny2205@yandex.ru',
#         ['amirny2205@yandex.ru'],
#         fail_silently=False,
#     )
#     print(x)
#     print('test')
#     return HttpResponse(x)


def activation(request, uid, token):
    '''
    this is a workaround for user activation, because we have no frontend.
    auth/users/ creates a user and sends an activation link (defined by DJOSER['ACTIVATION_URL']) to user's email.
    Then documentation(https://djoser.readthedocs.io/en/latest/base_endpoints.html#user-activate) says:
    you should provide site in your frontend application (configured by ACTIVATION_URL)
    which will send POST request to activate endpoint.
    '''
    activation_endpoint = 'auth/users/activation/'
    port = ':' + shop.settings.SELF_PORT if shop.settings.SELF_PORT else ''
    url = shop.settings.SELF_HOST + port + '/' + activation_endpoint
    print(url)
    print(type(url))
    response = requests.post(url, data={'uid':uid,'token':token})
    print(response.text)
    return HttpResponse('successfully activated account!')


class SecuredView01(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)


    def get(self, request, *args, **kwargs):
        print(request.user)
        content = {'message': 'Hello, GeeksforGeeks'}
        return Response(content)


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated,]


class GetSelfInfo(APIView):
    permission_classes = (IsAuthenticated,)


    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializerCustom(instance=user)
        return Response(serializer.data)

