from django.contrib.auth.models import User
from django.http import HttpResponse
import requests
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from Crypto.Hash import SHA1
from shop.models import BillModel
from shop.serializers import *
from users.serializers import UserSerializerCustom
from django.conf import settings


def activation_view(request, uid, token):
    """
    this is a workaround for user activation, because we have no frontend.
    auth/users/ creates a user and sends an activation link (defined by DJOSER['ACTIVATION_URL']) to user's email.
    Then documentation(https://djoser.readthedocs.io/en/latest/base_endpoints.html#user-activate) says:
    you should provide site in your frontend application (configured by ACTIVATION_URL)
    which will send POST request to activate endpoint.
    """
    activation_endpoint = 'auth/users/activation/'
    port = ':' + settings.SELF_PORT if settings.SELF_PORT else ''
    url = settings.SELF_HOST + port + '/' + activation_endpoint
    requests.post(url, data={'uid': uid, 'token': token})
    return HttpResponse('successfully activated account!')


class GetSelfInfoAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializerCustom(instance=user)
        return Response(serializer.data)


class DepositAPIView(APIView):
    def post(self, request, *args, **kwargs):
        if any(['signature' not in request.data,
                'transaction_id' not in request.data,
                'user_id' not in request.data,
                'bill_id' not in request.data,
                'amount' not in request.data,
                ]):
            return Response('some fields are missing')
        signature_post,  transaction_id, user_id, bill_id, amount = \
            request.data['signature'], request.data['transaction_id'], request.data['user_id'],\
            request.data['bill_id'], int(request.data['amount'])

        signature = SHA1.new()
        signature.update(f'{settings.PRIVATE_KEY}:{transaction_id}:{user_id}:{bill_id}:{amount}'.encode())
        if signature.hexdigest() != signature_post:
            return Response('signatures did not match', status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response('user does not exist', status=status.HTTP_400_BAD_REQUEST)
        try:
            bill = BillModel.objects.get(bill_id=bill_id)
            if bill.owner.id != user.id:
                return Response('invalid data provided', status=status.HTTP_400_BAD_REQUEST)
        except BillModel.DoesNotExist:
            bill = BillModel.objects.create(bill_id=bill_id, balance=0, owner=user)
        bill.balance += amount
        bill.save()
        TransactionModel.objects.create(bill=bill, summ=amount)
        return Response(f'success. Current bill balance is {bill.balance}')