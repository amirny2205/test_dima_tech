import djoser.views
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
import requests
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from Crypto.Hash import SHA1
from shop_main.models import *
from shop_main.serializers import *
import shop.settings
from djoser import signals
from djoser.conf import settings
from djoser.compat import get_user_email
from shop_main.serializers import UserSerializerCustom
import shop.settings

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


class Buy(APIView):
    permission_classes = (IsAuthenticated,)


    def post(self, request):
        product_id = int(request.data['product_id'])
        product = get_object_or_404(Product.objects.all(), id=product_id)
        user_bills = [b.bill_id for b in request.user.bills.all()]
        bill_id = int(request.data['bill_id'])
        if bill_id in user_bills:
            bill = Bill.objects.get(bill_id=bill_id)
            if bill.balance >= product.price:
                transaction = Transaction.objects.create(bill=bill, summ=product.price)
                bill.balance -= product.price
                bill.save()
                return Response('success')
            else:
                return Response('insufficent money')
        else:
            return Response('wrong bill_id')


class Deposit(APIView):
    def post(self, request, *args, **kwargs):
        if any(['signature' not in request.data, \
                'transaction_id' not in request.data, \
                'user_id' not in request.data, \
                'bill_id' not in request.data, \
                'amount' not in request.data, \
                ]):
            return Response('some fields are missing')
        signature_post,  transaction_id, user_id, bill_id, amount = \
            request.data['signature'], request.data['transaction_id'], request.data['user_id'],\
            request.data['bill_id'], request.data['amount']
        signature = SHA1.new()
        signature.update(f'{shop.settings.PRIVATE_KEY}:{transaction_id}:{user_id}:{bill_id}:{amount}'.encode())
        if signature.hexdigest() != signature_post:
            return Response('signatures did not match')

        return Response('success')

